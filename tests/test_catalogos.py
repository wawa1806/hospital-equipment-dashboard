from data_generator import catalog, config


def _equipos_del_catalogo() -> set[str]:
    return {e for lista in catalog.EQUIPOS_POR_CLASE.values() for e in lista}


# ── Cobertura total (==): cada dict por-equipo debe cubrir exactamente el catálogo ──

def test_marcas_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(catalog.MARCAS_POR_EQUIPO), (
        f"faltan: {equipos - set(catalog.MARCAS_POR_EQUIPO)}, "
        f"sobran: {set(catalog.MARCAS_POR_EQUIPO) - equipos}"
    )

def test_fallas_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(catalog.FALLAS_POR_EQUIPO), (
        f"faltan: {equipos - set(catalog.FALLAS_POR_EQUIPO)}, "
        f"sobran: {set(catalog.FALLAS_POR_EQUIPO) - equipos}"
    )

def test_abundancia_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(catalog.ABUNDANCIA_POR_EQUIPO), (
        f"faltan: {equipos - set(catalog.ABUNDANCIA_POR_EQUIPO)}, "
        f"sobran: {set(catalog.ABUNDANCIA_POR_EQUIPO) - equipos}"
    )

def test_clase_riesgo_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(catalog.CLASE_RIESGO_POR_EQUIPO), (
        f"faltan: {equipos - set(catalog.CLASE_RIESGO_POR_EQUIPO)}, "
        f"sobran: {set(catalog.CLASE_RIESGO_POR_EQUIPO) - equipos}"
    )

def test_tasa_base_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(config.TASA_BASE_POR_EQUIPO), (
        f"faltan: {equipos - set(config.TASA_BASE_POR_EQUIPO)}, "
        f"sobran: {set(config.TASA_BASE_POR_EQUIPO) - equipos}"
    )

def test_fraccion_costo_preventiva_cubren_todos_los_equipos():
    equipos = _equipos_del_catalogo()
    assert equipos == set(config.FRACCION_COSTO_PREVENTIVA), (
        f"faltan: {equipos - set(config.FRACCION_COSTO_PREVENTIVA)}, "
        f"sobran: {set(config.FRACCION_COSTO_PREVENTIVA) - equipos}"
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