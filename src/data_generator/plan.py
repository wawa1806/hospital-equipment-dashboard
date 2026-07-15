import numpy as np
import pandas as pd
from datetime import date

from data_generator import config


def generar_fact_plan(
    rng: np.random.Generator, dim_equipo: pd.DataFrame
) -> pd.DataFrame:

    en_plan = dim_equipo[dim_equipo["bajo_plan_mantenimiento"]]

    equipos_ids = []
    fechas = []
    for _, equipo in en_plan.iterrows():
        lo, hi = config.FRECUENCIA_PLAN_POR_CRITICIDAD[equipo["criticidad"]]
        freq = rng.integers(lo, hi + 1)
        offset = int(rng.integers(0, 12))

        for anio in range(config.FECHA_INICIO.year, config.FECHA_FIN_PLAN.year + 1):
            for k in range(freq):
                mes = (offset + int(12 / freq * k)) % 12 + 1
                dia = int(rng.integers(1, 29))
                fecha_plan = date(anio, mes, dia)
                if fecha_plan >= equipo["fecha_adquisicion"]:
                    fechas.append(fecha_plan)
                    equipos_ids.append(equipo["equipo_id"])

    tipo_mantenimiento_id = 1  # preventiva

    df = pd.DataFrame(
        {
            "equipo_id": equipos_ids,
            "fecha_planificada": fechas,
            "tipo_mantenimiento_id": tipo_mantenimiento_id,
        }
    )

    return df[
        [
            "equipo_id",
            "fecha_planificada",
            "tipo_mantenimiento_id",
        ]
    ]
