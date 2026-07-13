import numpy as np
import pandas as pd
from datetime import date

from data_generator import catalog, config, dimensiones, plan

def generar_fact_ordenes(rng: np.random.Generator , dim_equipo: pd.DataFrame, dim_ubicacion: pd.DataFrame, dim_tecnico: pd.DataFrame, fact_plan: pd.DataFrame) -> pd.DataFrame:

    ubicacion_id_por_servicio = dict(zip(dim_ubicacion["servicio_clinico"], dim_ubicacion["ubicacion_id"]))
    ubicacion_habitual: dict[int,int] = {}
    for equipo_id, nombre in zip(dim_equipo["equipo_id"], dim_equipo["nombre_equipo"]):
        clase = catalog.CLASE_POR_EQUIPO[nombre]
        servicio = rng.choice(catalog.SERVICIOS_POR_CLASE[clase])
        ubicacion_habitual[equipo_id] = ubicacion_id_por_servicio[servicio]

    tecnicos_por_especialidad = (dim_tecnico.groupby("especialidad")["tecnico_id"].apply(list).to_dict())

    ejecutables = fact_plan[fact_plan["fecha_planificada"] <= config.FECHA_CORTE]
    se_ejecuta = rng.random(len(ejecutables)) < (1- config.PCT_INCUMPLIMIENTO_PLAN)
    ejecutadas = ejecutables[se_ejecuta].copy()
    ejecutadas = ejecutadas.merge(dim_equipo[["equipo_id", "costo_adquisicion", "clase_funcional", "estrategia_mantenimiento"]], on="equipo_id",)

    n= len(ejecutadas)

    fechas_np = np.array(ejecutadas["fecha_planificada"], dtype="datetime64[D]")
    desv = rng.integers(config.DESVIACION_DIAS_PLAN[0], config.DESVIACION_DIAS_PLAN[1] + 1, size=n)
    ejecutadas["fecha_solicitud"] = np.busday_offset(fechas_np, desv, roll="forward")

    espera = rng.integers(0, 3, size=n).astype("timedelta64[D]")       
    ejecutadas["fecha_inicio"] = ejecutadas["fecha_solicitud"] + espera
    duracion = rng.integers(
        config.DURACION_DIAS_PREVENTIVA[0], config.DURACION_DIAS_PREVENTIVA[1] + 1, size=n
    ).astype("timedelta64[D]")
    ejecutadas["fecha_cierre"] = ejecutadas["fecha_inicio"] + duracion

    fracciones = np.array([
        rng.uniform(*config.FRACCION_COSTO_PREVENTIVA[nombre])
        for nombre in ejecutadas["nombre_equipo"]
    ])
    ejecutadas["costo_repuestos"] = (fracciones * ejecutadas["costo_adquisicion"]).round(-3)

    frac_mo = rng.uniform(*config.FRACCION_MANO_OBRA_PREVENTIVA, size=n)
    mano_obra_base = frac_mo * ejecutadas["costo_adquisicion"]
    es_gratis = ejecutadas["estrategia_mantenimiento"].isin(["Interno", "Contrato"])
    ejecutadas["costo_mano_obra"] = np.where(es_gratis, 0, mano_obra_base).round(-3)

    ejecutadas["horas_detencion"] = rng.uniform(
        *config.HORAS_DETENCION_PREVENTIVA, size=n                     
    ).round(1)
    ejecutadas["falla_reportada"] = None

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

    df = pd.DataFrame({
        "orden_id": ,
        "equipo_id": ,
        "ubicacion_id": ,
        "tecnico_id": ,
        "tipo_mantenimiento_id": ,
        "fecha_solicitud": ,
        "fecha_inicio": ,
        "fecha_cierre": ,
        "costo_repuestos": ,
        "costo_mano_obra": ,
        "horas_detencion": ,
        "falla_reportada": ,
    })
    return df[[
        "orden_id",
        "equipo_id",
        "ubicacion_id",
        "tecnico_id",
        "tipo_mantenimiento_id",
        "fecha_solicitud",
        "fecha_inicio",
        "fecha_cierre",
        "costo_repuestos",
        "costo_mano_obra",
        "horas_detencion",
        "falla_reportada",
    ]]




"""

def generar_fact_ordenes(rng: np.random:Generator , dim_equipo: pd.DataFrame, dim_ubicacion: pd.DataFrame, dim_tecnico: pd.DataFrame, fact_plan: pd.DataFrame) -> pd.DataFrame:


    
    df = pd.DataFrame({
        "orden_id": ,
        "equipo_id": ,
        "ubicacion_id": ,
        "tecnico_id": ,
        "tipo_mantenimiento_id": ,
        "fecha_solicitud": ,
        "fecha_inicio": ,
        "fecha_cierre": ,
        "costo_repuestos": ,
        "costo_mano_obra": ,
        "horas_detencion": ,
        "falla_reportada": ,
    })
    return df[[
        "orden_id",
        "equipo_id",
        "ubicacion_id",
        "tecnico_id",
        "tipo_mantenimiento_id",
        "fecha_solicitud",
        "fecha_inicio",
        "fecha_cierre",
        "costo_repuestos",
        "costo_mano_obra",
        "horas_detencion",
        "falla_reportada",
    ]]

"""