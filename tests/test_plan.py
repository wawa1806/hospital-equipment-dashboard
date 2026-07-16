import pandas as pd
from data_generator import config


def test_fechas_dentro_de_la_ventana(tablas):
    fechas = pd.to_datetime(tablas["fact_plan"]["fecha_planificada"])
    assert (fechas >= pd.Timestamp(config.FECHA_INICIO)).all()
    assert (fechas <= pd.Timestamp(config.FECHA_FIN_PLAN)).all()


def test_ninguna_planificada_antes_de_adquisicion(tablas):
    m = tablas["fact_plan"].merge(
        tablas["dim_equipo"][["equipo_id", "fecha_adquisicion"]], on="equipo_id"
    )
    violaciones = (
        pd.to_datetime(m["fecha_planificada"]) < pd.to_datetime(m["fecha_adquisicion"])
    ).sum()
    assert violaciones == 0


def test_unicidad_equipo_fecha_tipo(tablas):
    dup = (
        tablas["fact_plan"]
        .duplicated(subset=["equipo_id", "fecha_planificada", "tipo_mantenimiento_id"])
        .sum()
    )
    assert dup == 0
