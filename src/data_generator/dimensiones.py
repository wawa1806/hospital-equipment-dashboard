import numpy as np
import pandas as pd
from faker import Faker

from data_generator import catalog, config


"""
np.arange(1, n+1) → IDs autoincrementales.
rng.choice(lista, size=n) → sorteo uniforme; agrega p=probabilidades para ponderado (deben sumar 1).
rng.integers(lo, hi, size=n) → enteros aleatorios (hi excluido).
[algo_por_fila(x) for x in columna] → cuando cada fila depende de otra columna (ej. marca según equipo).
pd.NaT → el NULL de fechas; None o np.nan para el resto.
df["col"].value_counts() → tu herramienta de inspección número uno.
"""

"""
| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| tipo_mantenimiento_id | int | PK | Identificador único del tipo de mantenimiento a realizar | >= 1, autoincremental |
| nombre_tipo | string | - |Tipo de mantención | Preventiva/Correctiva |
"""
def generar_dim_tipo_mantenimiento() -> pd.DataFrame:

    df = pd.DataFrame({

        "tipo_mantenimiento_id": [1,2],
        "nombre_tipo": ["Preventiva", "Correctiva"],
        
        })
    return df[[
        "tipo_mantenimiento_id",
        "nombre_tipo",
    ]]

"""
| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| ubicacion_id | int | PK | Identificador único de una ubicación física del recinto | >= 1, autoincremental |
| servicio_clinico | string | - | Servicio clínico de la ubicación (UCI,UTI,etc) | Definidos en el catálogo |
| piso | string | - | Piso del edificio en el que se encuentra el equipo | Edificios(A-B) con 7 pisos, Edificios(C-D) con 4 pisos |
| edificio | string | - | Edificio en el que se encuentra el equipo | Edificios A-D |

dim_ubicacion — decisión de diseño que tomas tú: ¿cuántas ubicaciones? Lo natural: una fila por servicio clínico (24), asignando a cada uno 
edificio y piso. Sugerencia de realismo barato: asigna con criterio, no al azar puro (Urgencia en piso 1, Pabellón/Esterilización juntos,
servicios ambulatorios en edificios C-D...). Puedes hacerlo con un dict literal en catalogos.py 
(UBICACION_POR_SERVICIO: dict[str, tuple[edificio, piso]]) — para 24 servicios, un mapeo escrito a mano es MÁS defendible que azar 
("las ubicaciones las definí yo, coherentes con la lógica hospitalaria"). Azar aquí no aporta nada.

"""
def generar_dim_ubicacion() -> pd.DataFrame:

    servicios = list(catalog.UBICACION_POR_SERVICIO.keys())
    edificios = [catalog.UBICACION_POR_SERVICIO[s][0] for s in servicios]
    pisos = [catalog.UBICACION_POR_SERVICIO[s][1] for s in servicios]

    df = pd.DataFrame({
        "ubicacion_id": np.arange(1, len(servicios) + 1),
        "servicio_clinico": servicios,
        "piso": pisos,
        "edificio": edificios,
    })    

    return df[[
        "ubicacion_id",
        "servicio_clinico",
        "piso",
        "edificio",
    ]]

"""
decide N (¿12-20?). nombre con faker.name() (crea Faker("es_CL") en main y pásalo — nombres chilenos, detalle bonito). 
tipo: proporción interno/externo (nueva constante en config, ej. 60/40). especialidad: sorteada de las 4 (¿uniforme o pesada? 
los biomédicos suelen ser más — tu llamada).

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| tecnico_id | int | PK | Identificador único del técnico a cargo de la orden | >= 1, autoincremental | 
| nombre | string | - | Nombre del técnico a cargo de la orden | Definidos en el catálogo |
| tipo | string | - | Tipo de técnico | Interno/Externo |
| especialidad | string | - | Especialidad del técnico | Definidos en el catálogo |

"""
def generar_dim_tecnico(faker: Faker) -> pd.DataFrame:
    especialidades = []
    tipos = []
    for esp, (n_int, n_ext) in config.DOTACION_TECNICOS.items():
        especialidades.extend([esp] * n_int)
        tipos.extend(["Interno"] * n_int)         
        especialidades.extend([esp]* n_ext)
        tipos.extend(["Externo"] * n_ext)

    n = len(especialidades)
    nombres = [faker.name() for _ in range(n)]   

    
    df = pd.DataFrame({
        "tecnico_id": np.arange(1, n + 1),   # 1, 2, ..., n
        "nombre": nombres,
        "tipo": tipos,
        "especialidad": especialidades,
    })

    return df[[
        "tecnico_id",
        "nombre",
        "tipo",
        "especialidad",
    ]]

