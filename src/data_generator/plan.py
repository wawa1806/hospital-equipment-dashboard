import numpy as np
import pandas as pd
from datetime import date

from data_generator import catalog, config, dimensiones

"""
Filtrar: equipos con bajo_plan_mantenimiento == True (boolean 
mask, la conoces).

Expandir a filas: por cada equipo del plan × cada año (2023-2026) × su frecuencia → una fila con fecha.
Distribuye las N mantenciones del año espaciadas
(frecuencia 2 → ~enero y ~julio; técnica simple: mes base = 12/freq * k + jitter de días con rng)
o meses sorteados sin reemplazo si prefieres. Tu diseño; el requisito es que no caigan todas en el mismo mes.
Unicidad equipo+fecha+tipo garantizada por construcción (fechas distintas por diseño).
tipo_mantenimiento_id: siempre el de Preventiva (=1 según tu dim — puedes hardcodearlo 
con comentario o buscarlo del DataFrame de tipos; a tu criterio, defendido).
"""

"""
| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| equipo_id | int | FK | Identificador único del equipo | >= 1, autoincremental |
| fecha_planificada | date | FK | Fecha planificada para realizar la mantención | Fechas entre 01/01/2023 y 31/12/2026 |
| tipo_mantenimiento_id | int | FK | Identificador único del tipo de mantenimiento | >= 1, autoincremental |

"""


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
                mes = (offset + int(12 / freq*k)) % 12 + 1
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
