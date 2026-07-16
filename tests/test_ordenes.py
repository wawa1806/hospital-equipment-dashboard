import pandas as pd
import pytest
from data_generator import catalog, config


def test_cadena_solicitud_inicio(tablas):
    fo = tablas["fact_ordenes"]
    assert (fo["fecha_solicitud"] <= fo["fecha_inicio"]).all()


def test_cadena_inicio_cierre(tablas):
    fo = tablas["fact_ordenes"].dropna(subset=["fecha_cierre"])
    assert (fo["fecha_inicio"] <= fo["fecha_cierre"]).all()


def test_ninguna_orden_despues_del_corte(tablas):
    m = tablas["fact_ordenes"]
    violaciones = (
        pd.to_datetime(m["fecha_solicitud"]) > pd.to_datetime(config.FECHA_CORTE)
    ).sum()
    assert violaciones == 0


@pytest.mark.parametrize(
    "fk, dim",
    [
        ("equipo_id", "dim_equipo"),
        ("ubicacion_id", "dim_ubicacion"),
        ("tecnico_id", "dim_tecnico"),
        ("tipo_mantenimiento_id", "dim_tipo_mantenimiento"),
    ],
)
def test_integridad_referencial(tablas, fk, dim):
    huerfanas = ~tablas["fact_ordenes"][fk].isin(tablas[dim][fk])
    assert huerfanas.sum() == 0, f"{huerfanas.sum()} órdenes con {fk} inexistente"


def test_tecnico_coherente_con_especialidad(tablas):
    m = tablas["fact_ordenes"]
    eq = tablas["dim_equipo"]
    tec = tablas["dim_tecnico"]
    chk = m.merge(eq[["equipo_id", "nombre_equipo", "clase_funcional"]], on="equipo_id")
    chk = chk.merge(tec[["tecnico_id", "especialidad"]], on="tecnico_id")
    chk["esp_esperada"] = [
        catalog.ESPECIALIDAD_POR_CLASE[c] for c in chk["clase_funcional"]
    ]
    fuera_de_especialidad = (chk["especialidad"] != chk["esp_esperada"]).sum()
    assert fuera_de_especialidad == 0, (
        f"{fuera_de_especialidad} órdenes con técnico fuera de especialidad"
    )


def test_ubicacion_compatible_con_clase(tablas):
    m = tablas["fact_ordenes"]
    eq = tablas["dim_equipo"]
    u = tablas["dim_ubicacion"]
    chk = m.merge(eq[["equipo_id", "nombre_equipo", "clase_funcional"]], on="equipo_id")
    chk = chk.merge(u[["ubicacion_id", "servicio_clinico"]], on="ubicacion_id")
    fuera = sum(
        serv not in catalog.SERVICIOS_POR_CLASE[catalog.CLASE_POR_EQUIPO[nom]]
        for serv, nom in zip(chk["servicio_clinico"], chk["nombre_equipo"])
    )
    assert fuera == 0, f"{fuera} órdenes en servicio incompatible con su clase"


def test_correctiva_cuesta_mas_que_preventiva(tablas):
    medianas = (
        tablas["fact_ordenes"]
        .groupby("tipo_mantenimiento_id")["costo_repuestos"]
        .median()
    )
    assert medianas[2] > medianas[1], (
        f"correctiva {medianas[2]} vs preventiva {medianas[1]}"
    )
