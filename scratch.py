import numpy as np
import pandas as pd
from data_generator import config, catalog
from data_generator.dimensiones import generar_dim_equipo
from data_generator.dimensiones import generar_dim_ubicacion
from data_generator.dimensiones import generar_dim_tecnico
from data_generator.plan import generar_fact_plan
from faker import Faker


def generar_fact_ordenes(
    rng: np.random.Generator,
    dim_equipo: pd.DataFrame,
    dim_ubicacion: pd.DataFrame,
    dim_tecnico: pd.DataFrame,
    fact_plan: pd.DataFrame,
) -> pd.DataFrame:

    ubicacion_id_por_servicio = dict(zip(dim_ubicacion["servicio_clinico"], dim_ubicacion["ubicacion_id"]))
    ubicacion_habitual: dict[int,int] = {}
    for equipo_id, nombre in zip(dim_equipo["equipo_id"], dim_equipo["nombre_equipo"]):
        clase = catalog.CLASE_POR_EQUIPO[nombre]
        servicio = rng.choice(catalog.SERVICIOS_POR_CLASE[clase])
        ubicacion_habitual[equipo_id] = ubicacion_id_por_servicio[servicio]

    tecnicos_por_especialidad = (dim_tecnico.groupby("especialidad")["tecnico_id"].apply(list).to_dict())

    # --- Paso 1: preventivas que se ejecutaron ---
    ejecutables = fact_plan[fact_plan["fecha_planificada"] <= config.FECHA_CORTE]
    se_ejecuta = rng.random(len(ejecutables)) < (1 - config.PCT_INCUMPLIMIENTO_PLAN)
    ejecutadas = ejecutables[se_ejecuta].copy()

    # --- Paso 2: atributos del equipo (FIX 5: nombre_equipo incluido) ---
    ejecutadas = ejecutadas.merge(
        dim_equipo[["equipo_id", "nombre_equipo", "costo_adquisicion",
                    "clase_funcional", "estrategia_mantenimiento"]],
        on="equipo_id",
    )
    n = len(ejecutadas)

    # --- Paso 3: fechas encadenadas (solicitud hábil; inicio/cierre corridos) ---
    fechas_np = np.array(ejecutadas["fecha_planificada"], dtype="datetime64[D]")
    desv = rng.integers(config.DESVIACION_DIAS_PLAN[0], config.DESVIACION_DIAS_PLAN[1] + 1, size=n)
    ejecutadas["fecha_solicitud"] = np.busday_offset(fechas_np, desv, roll="forward")

    espera = rng.integers(0, 3, size=n).astype("timedelta64[D]")        # FIX 1+2: offsets sumados
    ejecutadas["fecha_inicio"] = ejecutadas["fecha_solicitud"] + espera
    duracion = rng.integers(
        config.DURACION_DIAS_PREVENTIVA[0], config.DURACION_DIAS_PREVENTIVA[1] + 1, size=n
    ).astype("timedelta64[D]")
    ejecutadas["fecha_cierre"] = ejecutadas["fecha_inicio"] + duracion

    # --- Paso 4: costos ---
    fracciones = np.array([
        rng.uniform(*config.FRACCION_COSTO_PREVENTIVA[nombre])
        for nombre in ejecutadas["nombre_equipo"]
    ])
    ejecutadas["costo_repuestos"] = (fracciones * ejecutadas["costo_adquisicion"]).round(-3)

    # FIX 3: mano de obra = fracción sorteada × valor del equipo, anulada según regla
    frac_mo = rng.uniform(*config.FRACCION_MANO_OBRA_PREVENTIVA, size=n)
    mano_obra_base = frac_mo * ejecutadas["costo_adquisicion"]
    es_gratis = ejecutadas["estrategia_mantenimiento"].isin(["Interno", "Contrato"])  # ← TU regla: ¿es esta?
    ejecutadas["costo_mano_obra"] = np.where(es_gratis, 0, mano_obra_base).round(-3)

    # --- Constantes de la orden preventiva ---
    ejecutadas["horas_detencion"] = rng.uniform(
        *config.HORAS_DETENCION_PREVENTIVA, size=n                      # FIX 4: size
    ).round(1)
    ejecutadas["falla_reportada"] = None
    # tipo_mantenimiento_id = 1 ya viene del plan — verifica que la columna sobrevivió al merge

    ejecutadas["tecnico_id"] = [
        int(rng.choice(tecnicos_por_especialidad[catalog.ESPECIALIDAD_POR_CLASE[clase]]))
        for clase in ejecutadas["clase_funcional"]
        ]

    prestado = rng.random(n) < config.PCT_EQUIPO_PRESTADO
    ubicaciones = []
    for equipo_id, nombre, esta_prestado in zip(
        ejecutadas["equipo_id"], ejecutadas["nombre_equipo"], prestado
    ):
        if esta_prestado:
            clase = catalog.CLASE_POR_EQUIPO[nombre]
            servicio = rng.choice(catalog.SERVICIOS_POR_CLASE[clase])
            ubicaciones.append(ubicacion_id_por_servicio[servicio])
        else:
            ubicaciones.append(ubicacion_habitual[equipo_id])
    ejecutadas["ubicacion_id"] = ubicaciones

    return ejecutadas   # parcial: paso 5 (técnico/ubicación) y orden_id pendientes


rng = np.random.default_rng(config.SEED)
Faker.seed(config.SEED)
faker = Faker('es_CL')
dim_equipo = generar_dim_equipo(rng)
dim_ubicacion = generar_dim_ubicacion()
dim_tecnico = generar_dim_tecnico(faker)
fact_plan = generar_fact_plan(rng, dim_equipo)
fact_ordenes = generar_fact_ordenes(rng, dim_equipo, dim_ubicacion, dim_tecnico, fact_plan)


print(fact_ordenes.head(10).to_string())
print()

chequeo = fact_ordenes.merge(dim_tecnico[["tecnico_id", "especialidad"]], on="tecnico_id")
chequeo["especialidad_esperada"] = [
    catalog.ESPECIALIDAD_POR_CLASE[c] for c in chequeo["clase_funcional"]
]
print((chequeo["especialidad"] != chequeo["especialidad_esperada"]).sum())

servicio_por_id = dict(zip(dim_ubicacion["ubicacion_id"], dim_ubicacion["servicio_clinico"]))
fact_ordenes["servicio_real"] = [servicio_por_id[u] for u in fact_ordenes["ubicacion_id"]]

fuera = sum(
    servicio not in catalog.SERVICIOS_POR_CLASE[catalog.CLASE_POR_EQUIPO[nombre]]
    for servicio, nombre in zip(fact_ordenes["servicio_real"], fact_ordenes["nombre_equipo"])
)
print(fuera)   

print(fact_ordenes["ubicacion_id"].value_counts())