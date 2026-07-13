from datetime import date

SEED = 46
N_EQUIPOS = 2000
FECHA_INICIO = date(2023, 1, 1)
FECHA_CORTE = date(2026, 6, 30)
FECHA_FIN_PLAN = date(2026, 12, 31)

FECHA_MIN_ADQUISICION = date(2010, 1, 1)

PCT_CON_GARANTIA = 0.50
# Porcentaje de equipos que no están en el plan de mantenimiento
PCT_EQUIPOS_SIN_PLAN = 0.30
# Porcentaje de equipos con mantenciones planificadas que no se ejecutaron
PCT_INCUMPLIMIENTO_PLAN = 0.12

PCT_EQUIPO_PRESTADO = 0.05
DESVIACION_DIAS_PLAN = (-3, 5)
DURACION_DIAS_PREVENTIVA: tuple[int, int] = (1, 3)
HORAS_DETENCION_PREVENTIVA: tuple[float, float] = (1.0, 8.0)
FRACCION_MANO_OBRA_PREVENTIVA: tuple[float, float] = (0.005, 0.02)

DIST_ESTADO_ACTUAL: dict[str, float] = {
    "Bueno": 0.87,
    "Regular": 0.10,
    "Malo": 0.01,
    "Baja": 0.02,
}

DIST_ESTRATEGIA: dict[str, float] = {
    "Interno": 0.50,
    "Externo": 0.20,
    "Contrato": 0.30,
}

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

FRECUENCIA_PLAN_POR_CRITICIDAD: dict[str, tuple[int, int]] = {
    "Alta": (2, 3),
    "Media": (1, 2),
    "Baja": (1, 1),
}

TASA_BASE_POR_EQUIPO: dict[str, float] = {
    # Soporte Vital
    "Ventilador mecánico": 1.8,
    "Máquina de anestesia": 1.5,
    "Desfibrilador": 0.4,
    "Bomba de infusión": 0.8,
    "Bomba PCA": 0.6,
    # Monitoreo
    "Monitor multiparámetro": 1.2,
    "Electrocardiógrafo": 0.6,
    "Oxímetro central": 0.5,
    "Holter": 0.9,
    "Monitor signos vitales": 1.0,
    # Imagenología
    "Ecógrafo": 1.1,
    "Rayos X portátil": 1.8,
    "Arco C": 1.4,
    "Mamógrafo": 0.9,
    "Tomógrafo CT": 2.0,
    "Resonador magnético": 2.0,
    # Esterilización
    "Autoclave": 2.5,
    "Lavadora desinfectora": 1.6,
    "Selladora térmica": 0.5,
    "Mesa de inspección": 0.05,
    "Carro de transporte estéril": 0.1,
    # Laboratorio
    "Centrífuga": 0.5,
    "Analizador hematológico": 2.2,
    "Microscopio": 0.15,
    "Baño termorregulado": 0.3,
    "Refrigerador clínico": 0.7,
    "Analizador bioquímico": 2.0,
    # Neonatología
    "Incubadora": 1.4,
    "Cuna radiante": 0.7,
    "Fototerapia": 0.3,
    "Ventilador neonatal": 1.7,
    # Odontología
    "Sillón dental": 0.4,
    "Compresor dental": 0.8,
    "Lámpara de fotocurado": 0.3,
    "Motor endodoncia": 0.4,
    "TAC dental": 1.2,
    "Unidad dental": 1.1,
    # Oftalmología
    "Lámpara de hendidura": 0.2,
    "Tonómetro": 0.5,
    "Autorrefractómetro": 0.3,
    "Retinógrafo": 0.4,
    "Campímetro": 0.4,
    "OCT": 0.8,
    "Lensómetro": 0.2,
    "Microscopio quirúrgico oftalmológico": 0.7,
    # Apoyo a diagnóstico
    "Esfigmomanómetro": 0.6,
    "Bioimpedanciómetro": 0.3,
    "Termómetro clínico": 0.4,
    "Otoscopio": 0.2,
    "Oftalmoscopio": 0.2,
    "Doppler fetal": 0.3,
    "Doppler vascular": 0.3,
    "Glucómetro": 0.15,
    "Espirómetro": 0.5,
    "Audiómetro": 0.4,
    "Balanza clínica": 0.25,
    "Tallímetro": 0.02,
    "Camilla de transporte": 0.4,
    # Rehabilitación
    "Trotadora": 1.3,
    "Camilla de fisioterapia": 0.2,
    "Bicicleta ergométrica": 0.6,
    "Electroestimulador": 0.4,
}


FRACCION_COSTO_PREVENTIVA: dict[str, tuple[float, float]] = {
    # Soporte Vital
    "Ventilador mecánico": (0.02, 0.05),
    "Máquina de anestesia": (0.03, 0.06),
    "Desfibrilador": (0.04, 0.08),
    "Bomba de infusión": (0.05, 0.10),
    "Bomba PCA": (0.05, 0.10),
    # Monitoreo
    "Monitor multiparámetro": (0.04, 0.08),
    "Electrocardiógrafo": (0.04, 0.08),
    "Oxímetro central": (0.03, 0.06),
    "Holter": (0.05, 0.09),
    "Monitor signos vitales": (0.05, 0.10),
    # Imagenología
    "Ecógrafo": (0.02, 0.05),
    "Rayos X portátil": (0.02, 0.04),
    "Arco C": (0.02, 0.04),
    "Mamógrafo": (0.02, 0.04),
    "Tomógrafo CT": (0.02, 0.04),
    "Resonador magnético": (0.02, 0.04),
    # Esterilización
    "Autoclave": (0.04, 0.08),
    "Lavadora desinfectora": (0.04, 0.08),
    "Selladora térmica": (0.06, 0.12),
    "Mesa de inspección": (0.02, 0.05),
    "Carro de transporte estéril": (0.03, 0.06),
    # Laboratorio
    "Centrífuga": (0.05, 0.10),
    "Analizador hematológico": (0.04, 0.07),
    "Microscopio": (0.05, 0.10),
    "Baño termorregulado": (0.06, 0.12),
    "Refrigerador clínico": (0.04, 0.08),
    "Analizador bioquímico": (0.04, 0.07),
    # Neonatología
    "Incubadora": (0.03, 0.07),
    "Cuna radiante": (0.04, 0.08),
    "Fototerapia": (0.05, 0.10),
    "Ventilador neonatal": (0.03, 0.06),
    # Odontología
    "Sillón dental": (0.04, 0.08),
    "Compresor dental": (0.05, 0.10),
    "Lámpara de fotocurado": (0.08, 0.15),
    "Motor endodoncia": (0.05, 0.10),
    "TAC dental": (0.02, 0.05),
    "Unidad dental": (0.04, 0.08),
    # Oftalmología
    "Lámpara de hendidura": (0.03, 0.06),
    "Tonómetro": (0.05, 0.10),
    "Autorrefractómetro": (0.03, 0.07),
    "Retinógrafo": (0.03, 0.06),
    "Campímetro": (0.03, 0.06),
    "OCT": (0.02, 0.05),
    "Lensómetro": (0.04, 0.08),
    "Microscopio quirúrgico oftalmológico": (0.02, 0.05),
    # Apoyo a diagnóstico
    "Esfigmomanómetro": (0.15, 0.25),
    "Bioimpedanciómetro": (0.04, 0.08),
    "Termómetro clínico": (0.15, 0.30),
    "Otoscopio": (0.10, 0.20),
    "Oftalmoscopio": (0.10, 0.20),
    "Doppler fetal": (0.06, 0.12),
    "Doppler vascular": (0.06, 0.12),
    "Glucómetro": (0.10, 0.20),
    "Espirómetro": (0.05, 0.10),
    "Audiómetro": (0.05, 0.10),
    "Balanza clínica": (0.08, 0.15),
    "Tallímetro": (0.10, 0.25),
    "Camilla de transporte": (0.04, 0.08),
    # Rehabilitación
    "Trotadora": (0.05, 0.10),
    "Camilla de fisioterapia": (0.04, 0.08),
    "Bicicleta ergométrica": (0.05, 0.10),
    "Electroestimulador": (0.05, 0.12),
}
