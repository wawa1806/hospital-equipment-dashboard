import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

from data_generator import catalog, config

def generar_dim_tipo_mantenimiento() -> pd.DataFrame:

    df = pd.DataFrame(
        {
            "tipo_mantenimiento_id": [1, 2],
            "nombre_tipo": ["Preventiva", "Correctiva"],
        }
    )
    return df[
        [
            "tipo_mantenimiento_id",
            "nombre_tipo",
        ]
    ]

def generar_dim_ubicacion() -> pd.DataFrame:

    servicios = list(catalog.UBICACION_POR_SERVICIO.keys())
    edificios = [catalog.UBICACION_POR_SERVICIO[s][0] for s in servicios]
    pisos = [catalog.UBICACION_POR_SERVICIO[s][1] for s in servicios]

    df = pd.DataFrame(
        {
            "ubicacion_id": np.arange(1, len(servicios) + 1),
            "servicio_clinico": servicios,
            "piso": pisos,
            "edificio": edificios,
        }
    )

    return df[
        [
            "ubicacion_id",
            "servicio_clinico",
            "piso",
            "edificio",
        ]
    ]


def generar_dim_tecnico(faker: Faker) -> pd.DataFrame:
    especialidades = []
    tipos = []
    for esp, (n_int, n_ext) in config.DOTACION_TECNICOS.items():
        especialidades.extend([esp] * n_int)
        tipos.extend(["Interno"] * n_int)
        especialidades.extend([esp] * n_ext)
        tipos.extend(["Externo"] * n_ext)

    n = len(especialidades)
    nombres = [faker.name() for _ in range(n)]

    df = pd.DataFrame(
        {
            "tecnico_id": np.arange(1, n + 1),
            "nombre": nombres,
            "tipo": tipos,
            "especialidad": especialidades,
        }
    )

    return df[
        [
            "tecnico_id",
            "nombre",
            "tipo",
            "especialidad",
        ]
    ]


def generar_dim_equipo(rng: np.random.Generator) -> pd.DataFrame:

    equipos = list(catalog.ABUNDANCIA_POR_EQUIPO)
    pesos = np.array(list(catalog.ABUNDANCIA_POR_EQUIPO.values()), dtype=float)
    p = pesos / pesos.sum()
    nombres = rng.choice(equipos, size=config.N_EQUIPOS, p=p)
    codigos = [f"EQ-{i:05d}" for i in range(1, config.N_EQUIPOS + 1)]
    clases = [catalog.CLASE_POR_EQUIPO[nombre] for nombre in nombres]
    marcas = [rng.choice(catalog.MARCAS_POR_EQUIPO[nombre]) for nombre in nombres]

    costos = [
        rng.triangular(lo, lo + (hi - lo) * 0.5, hi)
        for lo, hi in (catalog.RANGO_COSTO_POR_EQUIPO[nombre] for nombre in nombres)
    ]
    costos = np.round(costos, -3)
    vida_util = rng.triangular(5, 13, 15.5, size=config.N_EQUIPOS).round().astype(int)

    clase_riesgo = [catalog.CLASE_RIESGO_POR_EQUIPO[nombre] for nombre in nombres]
    criticidades = [
        rng.choice(list(d), p=list(d.values()))
        for d in (config.DIST_CRITICIDAD_POR_CLASE[clase] for clase in clases)
    ]

    base = config.FECHA_MIN_ADQUISICION
    max_dias = (config.FECHA_CORTE - base).days          # restar dates da un timedelta; .days lo hace int
    dias = rng.integers(0, max_dias + 1, size=config.N_EQUIPOS)
    fechas_adq = [base + timedelta(days=int(d)) for d in dias]

    fechas_gar = []
    for fecha in fechas_adq:
        if rng.random() < config.PCT_CON_GARANTIA: #tiene garantía?
            dias_garantia = int(rng.integers(365, 365 * 3 + 1)) # 1 a 3 años (en días)
            fechas_gar.append(fecha + timedelta(days=dias_garantia))
        else:
            fechas_gar.append(pd.NaT)


    modalidad = rng.choice(list(config.DIST_MODALIDAD), size=config.N_EQUIPOS, p=list(config.DIST_MODALIDAD.values()))
    
    estado = rng.choice(list(config.DIST_ESTADO_ACTUAL), size=config.N_EQUIPOS, p=list(config.DIST_ESTADO_ACTUAL.values()))

    bajo_plan = rng.random(config.N_EQUIPOS) < (1 - config.PCT_EQUIPOS_SIN_PLAN)

    estrategias = rng.choice(list(config.DIST_ESTRATEGIA), size=config.N_EQUIPOS, p=list(config.DIST_ESTRATEGIA.values()))

    serie = [f"SN-{i:04d}-{rng.integers(10**7, 10**8)}" for i in range(1, config.N_EQUIPOS + 1)]

    modelo = [
        f"{''.join(c for c in marca if c.isalpha())[:2].upper()}-{rng.integers(100, 1000)}"
        for marca in marcas
    ] 
    df = pd.DataFrame(
        {
            "equipo_id": np.arange(1, config.N_EQUIPOS + 1),
            "codigo_inventario": codigos,
            "numero_serie": serie,
            "nombre_equipo": nombres,
            "clase_funcional": clases,
            "marca": marcas,
            "modelo": modelo,
            "clase_riesgo": clase_riesgo,
            "criticidad": criticidades,
            "fecha_adquisicion": fechas_adq,
            "costo_adquisicion": costos,
            "vida_util_anios": vida_util,
            "modalidad_propiedad": modalidad,
            "fecha_vencimiento_garantia": fechas_gar ,
            "bajo_plan_mantenimiento": bajo_plan,
            "estrategia_mantenimiento":estrategias,
            "estado_actual":estado, 
        }
    )

    return df[
        [
            "equipo_id",
            "codigo_inventario",
            "numero_serie",
            "nombre_equipo",
            "clase_funcional",
            "marca",
            "modelo",
            "clase_riesgo",
            "criticidad",
            "fecha_adquisicion",
            "costo_adquisicion",
            "vida_util_anios",
            "modalidad_propiedad",
            "fecha_vencimiento_garantia",
            "bajo_plan_mantenimiento",
            "estrategia_mantenimiento",
            "estado_actual",
        ]
    ]