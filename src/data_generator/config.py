from datetime import date

SEED = 46
N_EQUIPOS = 2000
FECHA_INICIO = date(2023, 1, 1)
FECHA_CORTE = date(2026, 6, 30)
FECHA_FIN_PLAN = date(2026, 12, 31)


DIST_ESTADO_ACTUAL: dict[str, float] = {
    "Bueno": 0.87,
    "Regular": 0.10,
    "Malo": 0.01,
    "Baja": 0.02,
}

# Porcentaje de equipos que no están en el plan de mantenimiento
PCT_EQUIPOS_SIN_PLAN = 0.30
# Porcentaje de equipos con mantenciones planificadas que no se ejecutaron
PCT_INCUMPLIMIENTO_PLAN = 0.12

DIST_MODALIDAD: dict[str, float] = {
    "Propio": 0.80,
    "Comodato": 0.15,
    "Arriendo": 0.05,
}

DOTACION_TECNICOS: dict[str, tuple[int, int]] = {
    # especialidad: (internos, externos)
    "Biomédico": (5, 2),
    "Imagenología y Radiología": (0, 2),
    "Mecatrónica": (2, 0),
    "Laboratorio": (0, 1),
}

DIST_CRITICIDAD_POR_CLASE: dict[str, dict[str, float]] = {
    "Soporte vital": {"Alta": 0.8, "Media": 0.2, "Baja": 0.0},
    "Monitoreo": {"Alta": 0.4, "Media": 0.5, "Baja": 0.1},
    "Imagenología": {"Alta": 0.5, "Media": 0.4, "Baja": 0.1},
    "Esterilización": {"Alta": 0.5, "Media": 0.3, "Baja": 0.2},
    "Laboratorio": {"Alta": 0.3, "Media": 0.5, "Baja": 0.2},
    "Neonatología": {"Alta": 0.7, "Media": 0.3, "Baja": 0.0},
    "Odontología": {"Alta": 0.1, "Media": 0.6, "Baja": 0.3},
    "Oftalmología": {"Alta": 0.15, "Media": 0.35, "Baja": 0.5},
    "Apoyo a diagnóstico": {"Alta": 0.05, "Media": 0.35, "Baja": 0.6},
    "Rehabilitación": {"Alta": 0.0, "Media": 0.15, "Baja": 0.85},
}
