from data_generator import catalog, config
import pytest

def _equipos_del_catalogo() -> set[str]:
    return {e for lista in catalog.EQUIPOS_POR_CLASE.values() for e in lista}


@pytest.mark.parametrize("nombre, dict_auditado", [
    ("MARCAS_POR_EQUIPO", catalog.MARCAS_POR_EQUIPO),
    ("FALLAS_POR_EQUIPO", catalog.FALLAS_POR_EQUIPO),
    ("ABUNDANCIA_POR_EQUIPO", catalog.ABUNDANCIA_POR_EQUIPO),
    ("CLASE_RIESGO_POR_EQUIPO", catalog.CLASE_RIESGO_POR_EQUIPO),
    ("TASA_BASE_POR_EQUIPO", config.TASA_BASE_POR_EQUIPO),
    ("FRACCION_COSTO_PREVENTIVA", config.FRACCION_COSTO_PREVENTIVA),
])
def test_cobertura_total_del_catalogo(nombre, dict_auditado):
    equipos = _equipos_del_catalogo()
    assert equipos == set(dict_auditado), (
        f"{nombre} — faltan: {equipos - set(dict_auditado)}, sobran: {set(dict_auditado) - equipos}"
    )

# ── Subconjunto (⊆): dicts parciales solo pueden referir equipos/servicios existentes ──

def test_invierno_solo_contiene_equipos_existentes():
    fantasmas = set(config.TASA_EXTRA_FALLA_INVIERNO) - _equipos_del_catalogo()
    assert not fantasmas, f"equipos inexistentes en invierno: {fantasmas}"

def test_servicios_usados_existen_en_ubicaciones():
    usados = {s for lista in catalog.SERVICIOS_POR_CLASE.values() for s in lista}
    sin_ubicacion = usados - set(catalog.UBICACION_POR_SERVICIO)
    assert not sin_ubicacion, f"servicios sin ubicación: {sin_ubicacion}"


# ── Cobertura de clases ──

def test_especialidades_cubren_todas_las_clases():
    clases = set(catalog.EQUIPOS_POR_CLASE)
    assert clases == set(catalog.ESPECIALIDAD_POR_CLASE), (
        f"clases sin especialidad: {clases - set(catalog.ESPECIALIDAD_POR_CLASE)}"
    )

def test_servicios_por_clase_cubren_todas_las_clases():
    clases = set(catalog.EQUIPOS_POR_CLASE)
    assert clases == set(catalog.SERVICIOS_POR_CLASE), (
        f"clases sin servicios: {clases - set(catalog.SERVICIOS_POR_CLASE)}"
    )

def test_dist_criticidad_por_clase_cubren_todas_las_clases():
    clases = set(catalog.EQUIPOS_POR_CLASE)
    assert clases == set(config.DIST_CRITICIDAD_POR_CLASE), (
        f"clases sin criticidad por clase: {clases - set(config.DIST_CRITICIDAD_POR_CLASE)}"
    )


# ── Distribuciones ──

def test_distribuciones_simples_suman_uno():
    for nombre, dist in [
        ("DIST_ESTADO_ACTUAL", config.DIST_ESTADO_ACTUAL),
        ("DIST_MODALIDAD", config.DIST_MODALIDAD),
        ("DIST_ESTRATEGIA", config.DIST_ESTRATEGIA),
    ]:
        assert abs(sum(dist.values()) - 1.0) < 1e-9, f"{nombre} suma {sum(dist.values())}"


def test_criticidad_por_clase_suma_uno_en_cada_clase():
    for clase, dist in config.DIST_CRITICIDAD_POR_CLASE.items():
        assert abs(sum(dist.values()) - 1.0) < 1e-9, (
            f"criticidad de '{clase}' suma {sum(dist.values())}"
        )