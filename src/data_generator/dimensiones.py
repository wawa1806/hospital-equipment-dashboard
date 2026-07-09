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


4. dim_equipo — el plato fuerte. Pipeline por columna:

nombre_equipo: sorteo ponderado — aquí entra tu ABUNDANCIA_POR_EQUIPO:

python  equipos = list(catalogos.ABUNDANCIA_POR_EQUIPO)
  pesos = np.array([...], dtype=float)
  p = pesos / pesos.sum()          # normalizar: rng.choice exige que sume 1
  nombres = rng.choice(equipos, size=config.N_EQUIPOS, p=p)

- clase_funcional: derivada del nombre — necesitas el mapeo inverso equipo→clase. No lo escribas a mano 
(60 entradas, ya existe la info en EQUIPOS_POR_CLASE): constrúyelo por comprensión al inicio del módulo o en 

- catalogos.py. Piensa cómo — es un ejercicio clásico de dict comprehension con doble loop.

- marca: sorteo desde MARCAS_POR_EQUIPO[nombre] — fila a fila (una list comprehension con rng.choice está bien
a esta escala).

- modelo: sintético — patrón tipo 2-3 letras + guion + 2-3 dígitos (ej. derivado de la marca + números aleatorios).
Inventa tu formato.

- numero_serie: faker.bothify o combinación de letras/dígitos con rng. Único (verifícalo o usa el índice
como componente).

- codigo_inventario: EQ-{i:05d} desde el índice. Sin azar.

- fecha_adquisicion: fechas aleatorias entre 2010 y la fecha de corte. Técnica: sortea días como enteros y súmalos
a la fecha base (date + timedelta(days=int(x))). Distribución uniforme está bien para empezar.

- costo_adquisicion: ojo, trampa de realismo — el costo depende brutalmente del tipo (un termómetro: $30 mil;
un tomógrafo: decenas/cientos de millones). Un rango global uniforme genera termómetros de $50M. 
Necesitas rangos por equipo o por clase: nueva estructura en catalogos.py (sugerencia pragmática: 
RANGO_COSTO_POR_CLASE: dict[str, tuple[int, int]] — 10 entradas, no 60). Y dentro del rango,
distribución lognormal o triangular, no uniforme (muchos baratos, pocos caros).
De paso: tu diccionario de datos dice tope $80M — con Tomógrafo y Resonador dentro, ese tope quedó corto; actualízalo.

- vida_util_anios: por clase también sería lo fino (equipos de imagen duran más que termómetros), pero 
uniforme 5-15 es aceptable v1. Tu llamada.
modalidad_propiedad, estado_actual, bajo_plan_mantenimiento: sorteos con rng.choice(..., p=...) desde tus 
dicts de config (list(d.keys()) / list(d.values())).

- criticidad y clase_riesgo: NO uniformes al azar — dependen del tipo de equipo (un ventilador nunca es 
criticidad Baja ni clase I). Decisión: o mapeos por equipo/clase en catálogo (fino) o probabilidades 
condicionadas por clase funcional (intermedio). Elige y defiende.

- fecha_vencimiento_garantia: coherencia temporal — la garantía vence típicamente 1-3 años DESPUÉS de 
fecha_adquisicion, y solo una fracción de equipos la tiene registrada (constante nueva, ej. 70%).
NULL (usa pd.NaT) para el resto.

Reglas de coherencia (lo que separa esto de datos de juguete)
Mínimas para esta v1: (1) garantía posterior a adquisición; (2) costo según clase; 
(3) criticidad/clase_riesgo según tipo. Anota una que dejamos para después conscientemente: 
estado "Baja" correlacionado con edad (equipos viejos) — se puede sofisticar luego; 
si quieres incluirla ya, bienvenido.
Cómo trabajar
Función por función, ejecutando cada una (uv run python -c "..." o un scratch script) y mirando el 
DataFrame con .head(10) y .value_counts() de las categóricas — mirar los datos generados con ojo crítico ES 
el trabajo. Un commit por función o por par de funciones lógicas
(Add maintenance type and location dimensions, Add technician dimension generator, Add equipment dimension generator). 
Las estructuras nuevas de catálogo (UBICACION_POR_SERVICIO, RANGO_COSTO_POR_CLASE, mapeos de criticidad) 
van en el commit de la función que las consume.
"""

"""
| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| tipo_mantenimiento_id | int | PK | Identificador único del tipo de mantenimiento a realizar | >= 1, autoincremental |
| nombre_tipo | string | - |Tipo de mantención | Preventiva/Correctiva |
"""


def generar_dim_tipo_mantenimiento() -> pd.DataFrame:

    df = pd.DataFrame(
        {
            "tipo_mantenimiento_id": [1, 2],
            "nombre_tipo": ["Preventiva", "Correctiva"],
        }
    )
    return df[
        [
            "tipo_mantenimiento_id",
            "nombre_tipo",
        ]
    ]


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

    df = pd.DataFrame(
        {
            "ubicacion_id": np.arange(1, len(servicios) + 1),
            "servicio_clinico": servicios,
            "piso": pisos,
            "edificio": edificios,
        }
    )

    return df[
        [
            "ubicacion_id",
            "servicio_clinico",
            "piso",
            "edificio",
        ]
    ]


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
        especialidades.extend([esp] * n_ext)
        tipos.extend(["Externo"] * n_ext)

    n = len(especialidades)
    nombres = [faker.name() for _ in range(n)]

    df = pd.DataFrame(
        {
            "tecnico_id": np.arange(1, n + 1),  
            "nombre": nombres,
            "tipo": tipos,
            "especialidad": especialidades,
        }
    )

    return df[
        [
            "tecnico_id",
            "nombre",
            "tipo",
            "especialidad",
        ]
    ]

"""
| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| equipo_id | int | PK | Identificador único del equipo | >= 1, autoincremental |
| codigo_inventario | string | - | Código de inventario establecido por el recinto | EQ-NNNN, >= EQ-0001, autoincremental |
| numero_serie | string | - | Número de serie de fábrica del equipo | Generado por script |
| nombre_equipo | string | - | Nombre del equipo | Definidos en el catálogo |
| clase_funcional | string | - | Clase o tipo de equipo | Definidas en catálogo |
| marca | string | - | Marca del equipo | Definida en el catálogo |
| modelo | string | - | Modelo del equipo médico establecido por el fabricante | Definido en catálogo |
| clase_riesgo | string | - | Clase de riesgo del equipo según normativa | Valores de I/II/III |
| criticidad | string | - | Dependencia del equipo, qué tan grave es que este equipo este fuera de servicio | Alta/Media/Baja |
| fecha_adquisicion | date | - | Fecha de la adquisición de equipo/dispositivo médico | Adquisiciones definidas desde 2010 |
| costo_adquisicion | float | - | Costo en CLP del equipo/dispositivo médico, declarado en la orden de compra | 30.000 CLP - 80.000.000 CLP |
| vida_util_anios | int | - | Vida útil del equipo/dispositivo declarado por el fabricante | 5-15 años |
| modalidad_propiedad | string | - | Identifica la propiedad del equipo | Propio/Arriendo/Comodato |
| fecha_vencimiento_garantia | date | - | Fecha en que la garantía caduca | Sin garantía=null |
| bajo_plan_mantenimiento | bool | - | Equipo se encuentra en el plan de mantenimiento del establecimiento | True/False |
| estrategia_mantenimiento | string | - | Estrategia de mantenimiento establecida para el Equipo | Interno/Externo/Contrato|
| estado_actual | string | -  | Estado actual en el que se encuentra el equipo | Bueno/Regular/Malo/Baja |


Etapa 1 — el esqueleto que ya sabes hacer: equipo_id, codigo_inventario (f-string con {i:05d}), 
nombre_equipo (sorteo ponderado con ABUNDANCIA_POR_EQUIPO — el snippet de normalización está en la spec), 
clase_funcional (mapeo inverso — el ejercicio de dict comprehension),
marca (list comprehension con rng.choice por fila). Con esto ya tienes un DataFrame que puedes mirar.

Etapa 2 — los que requieren estructuras nuevas en catálogo: costo_adquisicion 
(necesitas RANGO_COSTO_POR_CLASE — 10 tuplas (min, max), 
tu criterio de precios; distribución dentro del rango: rng.uniform v1 aceptable, rng.triangular mejor), 
criticidad y clase_riesgo (decide tu mecanismo: mapeo fijo por equipo o probabilidades por clase — cualquiera,
 defendido), vida_util_anios.

Etapa 3 — las fechas con coherencia: fecha_adquisicion (base + timedelta de días sorteados), 
fecha_vencimiento_garantia (posterior a adquisición, solo ~70% la tiene, resto pd.NaT), 
modalidad_propiedad / estado_actual / bajo_plan_mantenimiento desde tus dists de config,
numero_serie y modelo (tus formatos inventados).

Trabaja etapa por etapa ejecutando entre cada una (.head(10) + value_counts() de lo nuevo). 
Si una técnica puntual no te sale (el mapeo inverso es el candidato), pregunta directo. 
Entrega esperada: la función completa + output con head(10) + value_counts() de nombre_equipo (top 10), 
clase_funcional, criticidad y estado_actual + commit + ruff
"""
"""
def generar_dim_equipo(rng:np.random.Generator) -> pd.DataFrame:

    equipos = list(catalog.ABUNDANCIA_POR_EQUIPO)
    pesos = np.array([...], dtype=float)
    p = pesos / pesos.sum()          
    nombres = rng.choice(equipos, size=config.N_EQUIPOS, p=p)

    n = len(equipos)

    df = pd.DataFrame({
        "equipo_id": np.arange(1, n + 1),
        "codigo_inventario": ,
        "numero_serie": ,
        "nombre_equipo": ,
        "clase_funcional": ,
        "marca": ,
        "modelo": ,
        "clase_riesgo": ,
        "criticidad": ,
        "fecha_adquisicion": ,
        "costo_adquisicion": ,
        "vida_util_anios": ,
        "modalidad_propiedad": ,
        "fecha_vencimiento_garantia": ,
        "bajo_plan_mantenimiento": ,
        "estrategia_mantenimiento": ,
        "estado_actual": ,        
    })

    return df[[
        "equipo_id",
        "codigo_inventario",
        "numero_serie",
        "nombre_equipo",
        "clase_funcional",
        "marca",
        "modelo",
        "clase_riesgo",
        "criticidad",
        "fecha_adquisicion",
        "costo_adquisicion",
        "vida_util_anios",
        "modalidad_propiedad",
        "fecha_vencimiento_garantia",
        "bajo_plan_mantenimiento",
        "estrategia_mantenimiento",
        "estado_actual",
    ]]

     clase_funcional: derivada del nombre — necesitas el mapeo inverso equipo→clase. No lo escribas a mano 
(60 entradas, ya existe la info en EQUIPOS_POR_CLASE): constrúyelo por comprensión al inicio del módulo o en 

- marca: sorteo desde MARCAS_POR_EQUIPO[nombre] — fila a fila (una list comprehension con rng.choice está bien
a esta escala).

list comprehension
[nueva_expresion for elemento in iterable]
---
numeros = [1, 2, 3, 4]
cuadrados = [n ** 2 for n in numeros]
print(cuadrados)
[1, 4, 9, 16]
---
dict comprehension
{clave: valor for elemento in iterable}
---
numeros = [1, 2, 3, 4]
cuadrados = {n: n ** 2 for n in numeros}
print(cuadrados)
{1: 1, 2: 4, 3: 9, 4: 16}

"""

def generar_dim_equipo(rng: np.random.Generator) -> pd.DataFrame:

    equipos = list(catalog.ABUNDANCIA_POR_EQUIPO)
    pesos = np.array(list(catalog.ABUNDANCIA_POR_EQUIPO.values()), dtype=float)
    p = pesos / pesos.sum()          
    nombres = rng.choice(equipos, size=config.N_EQUIPOS, p=p)
    codigos = [f"EQ-{i:05d}" for i in range(1, config.N_EQUIPOS + 1) ]
    clases = [catalog.CLASE_POR_EQUIPO[nombre] for nombre in nombres]
    marcas = [rng.choice(catalog.MARCAS_POR_EQUIPO[nombre]) for nombre in nombres]

    df = pd.DataFrame({
        "equipo_id": np.arange(1, config.N_EQUIPOS + 1),
        "codigo_inventario": codigos,
        "nombre_equipo": nombres,
        "clase_funcional": clases,
        "marca": marcas,
    })

    return df[[
        "equipo_id",
        "codigo_inventario",
        "nombre_equipo",
        "clase_funcional",
        "marca",
    ]]