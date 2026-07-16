import numpy as np
import pandas as pd
import pytest
from faker import Faker
from data_generator import config
from data_generator.dimensiones import generar_dim_equipo
from data_generator.dimensiones import generar_dim_ubicacion
from data_generator.dimensiones import generar_dim_tecnico
from data_generator.dimensiones import generar_dim_tipo_mantenimiento
from data_generator.plan import generar_fact_plan
from data_generator.ordenes import generar_fact_ordenes


@pytest.fixture(scope="session")
def tablas() -> dict[str, pd.DataFrame]:
    """Pipeline completo en el orden de main — una generación por sesión de tests."""
    rng = np.random.default_rng(config.SEED)
    Faker.seed(config.SEED)
    faker = Faker("es_CL")

    dim_equipo = generar_dim_equipo(rng)
    dim_ubicacion = generar_dim_ubicacion()
    dim_tecnico = generar_dim_tecnico(faker)
    dim_tipo_mantenimiento = generar_dim_tipo_mantenimiento()
    fact_plan = generar_fact_plan(rng, dim_equipo)
    fact_ordenes = generar_fact_ordenes(
        rng, dim_equipo, dim_ubicacion, dim_tecnico, fact_plan
    )

    return {
        "dim_equipo": dim_equipo,
        "dim_ubicacion": dim_ubicacion,
        "dim_tecnico": dim_tecnico,
        "dim_tipo_mantenimiento": dim_tipo_mantenimiento,
        "fact_plan": fact_plan,
        "fact_ordenes": fact_ordenes,
    }
