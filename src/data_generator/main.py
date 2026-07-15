import numpy as np
import pandas as pd
from pathlib import Path
from faker import Faker
from data_generator import config
from data_generator.dimensiones import generar_dim_equipo
from data_generator.dimensiones import generar_dim_ubicacion
from data_generator.dimensiones import generar_dim_tecnico
from data_generator.dimensiones import generar_dim_tipo_mantenimiento
from data_generator.plan import generar_fact_plan
from data_generator.ordenes import generar_fact_ordenes



def main() -> None:
    Path("data").mkdir(exist_ok=True)
    rng = np.random.default_rng(config.SEED)
    Faker.seed(config.SEED)
    faker = Faker("es_CL")

    dim_equipo = generar_dim_equipo(rng)
    dim_ubicacion = generar_dim_ubicacion()
    dim_tecnico = generar_dim_tecnico(faker)
    dim_tipo_mantenimiento = generar_dim_tipo_mantenimiento()
    fact_plan = generar_fact_plan(rng, dim_equipo)
    fact_ordenes = generar_fact_ordenes(rng, dim_equipo, dim_ubicacion, dim_tecnico, fact_plan)

    for col in ["fecha_adquisicion", "fecha_vencimiento_garantia"]:
        dim_equipo[col] = pd.to_datetime(dim_equipo[col])
    fact_plan["fecha_planificada"] = pd.to_datetime(fact_plan["fecha_planificada"])

    tablas = {"dim_equipo": dim_equipo, "dim_ubicacion": dim_ubicacion, "dim_tecnico": dim_tecnico, "dim_tipo_mantenimiento": dim_tipo_mantenimiento, "fact_plan": fact_plan, "fact_ordenes": fact_ordenes }
    for nombre, df in tablas.items():
        df.to_csv(f"data/{nombre}.csv", index=False, encoding="utf-8-sig")
        print(f"{nombre}: {len(df)} filas")

if __name__ == "__main__":
    main()