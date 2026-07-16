def test_equipo_id_es_unico(tablas):
    assert tablas["dim_equipo"]["equipo_id"].is_unique
