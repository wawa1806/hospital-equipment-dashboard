from datetime import date

SEED = 46
N_EQUIPOS = 2000
FECHA_INICIO = date(2023, 1, 1)
FECHA_CORTE = date(2026, 6, 30)
FECHA_FIN_PLAN = date(2026, 12, 31)


DIST_ESTADO_ACTUAL: dict[str, float] = {
    "Bueno": 0.87, "Regular": 0.10, "Malo": 0.01, "Baja": 0.02,
}

# Porcentaje de equipos que no están en el plan de mantenimiento
PCT_EQUIPOS_SIN_PLAN = 0.30
# Porcentaje de equipos con mantenciones planificadas que no se ejecutaron
PCT_INCUMPLIMIENTO_PLAN = 0.12

DIST_MODALIDAD: dict[str, float] = {
    "Propio": 0.80, "Comodato": 0.15, "Arriendo": 0.05,
}

DOTACION_TECNICOS: dict[str, tuple[int, int]] = {
    # especialidad: (internos, externos)
    "Biomédico": (5, 2),
    "Imagenología y Radiología": (0, 2),
    "Mecatrónica": (2, 0),
    "Laboratorio": (0, 1),
}