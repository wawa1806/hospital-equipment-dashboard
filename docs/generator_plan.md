src/data_generator/
├── __init__.py
├── config.py          ← parámetros: N_EQUIPOS, fechas, corte, seed, proporciones
├── catalog.py       ← las listas: clases, equipos, marcas, fallas, servicios...
├── dimensiones.py     ← genera las 4 dims (funciones puras: params → DataFrame)
├── plan.py            ← genera fact_plan_mantenimiento
├── ordenes.py         ← genera fact_ordenes_trabajo (el módulo difícil)
└── main.py            ← orquestador: llama todo en orden, valida, exporta CSVs