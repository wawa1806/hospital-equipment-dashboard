import numpy as np
import pandas as pd
from datetime import date, timedelta
from data_generator import config, catalog
from data_generator.dimensiones import generar_dim_equipo
from data_generator.dimensiones import generar_dim_ubicacion
from data_generator.dimensiones import generar_dim_tecnico
from data_generator.plan import generar_fact_plan
from data_generator.ordenes import generar_fact_ordenes
from data_generator.ordenes import _sortear_ubicacion
from faker import Faker

rng = np.random.default_rng(config.SEED)
Faker.seed(config.SEED)
faker = Faker('es_CL')
dim_equipo = generar_dim_equipo(rng)
dim_ubicacion = generar_dim_ubicacion()
dim_tecnico = generar_dim_tecnico(faker)
fact_plan = generar_fact_plan(rng, dim_equipo)
fact_ordenes = generar_fact_ordenes(rng, dim_equipo, dim_ubicacion, dim_tecnico, fact_plan)


print(fact_ordenes.head(10).to_string())
print()
print(fact_ordenes["tipo_mantenimiento_id"].value_counts())
print()
print(fact_ordenes["fecha_cierre"].isna().sum())
print()
print(fact_ordenes["costo_repuestos"].describe())

print((fact_ordenes["fecha_solicitud"] > fact_ordenes["fecha_inicio"]).sum())
print((fact_ordenes.dropna(subset=["fecha_cierre"])["fecha_inicio"] >
       fact_ordenes.dropna(subset=["fecha_cierre"])["fecha_cierre"]).sum())

corr = fact_ordenes[fact_ordenes["tipo_mantenimiento_id"] == 2].merge(
    dim_equipo[["equipo_id", "nombre_equipo"]], on="equipo_id"
)
for equipo in ["Ventilador mecánico", "Tallímetro"]:
    print(equipo)
    print(corr[corr["nombre_equipo"] == equipo]["fecha_solicitud"].dt.month
          .value_counts().sort_index())

    
# fuera del loop:
inv = corr[
    corr["nombre_equipo"].isin(config.TASA_EXTRA_FALLA_INVIERNO)
    & (corr["fecha_solicitud"].dt.year < 2026)
]
print(inv["fecha_solicitud"].dt.month.value_counts().sort_index())


print(fact_ordenes.groupby("tipo_mantenimiento_id")["costo_repuestos"].describe())
print()

# --- Verificación técnico-especialidad (esperado: 0) ---
chk = fact_ordenes.merge(dim_equipo[["equipo_id", "nombre_equipo", "clase_funcional"]], on="equipo_id")
chk = chk.merge(dim_tecnico[["tecnico_id", "especialidad"]], on="tecnico_id")
chk["esp_esperada"] = [catalog.ESPECIALIDAD_POR_CLASE[c] for c in chk["clase_funcional"]]
print("Técnico fuera de especialidad:", (chk["especialidad"] != chk["esp_esperada"]).sum())

# --- Verificación ubicación-clase (esperado: 0) ---
chk = chk.merge(dim_ubicacion[["ubicacion_id", "servicio_clinico"]], on="ubicacion_id")
fuera = sum(
    serv not in catalog.SERVICIOS_POR_CLASE[catalog.CLASE_POR_EQUIPO[nom]]
    for serv, nom in zip(chk["servicio_clinico"], chk["nombre_equipo"])
)
print("Órdenes en servicio incompatible:", fuera)

print()

# --- Post-baja: garantizada por construcción (descarte en el loop de fallas);
#     comprobación indirecta: los equipos de Baja no deben concentrar órdenes hasta el corte ---
baja = chk[chk["equipo_id"].isin(dim_equipo[dim_equipo["estado_actual"] == "Baja"]["equipo_id"])]
print("Última orden de equipos de Baja:", baja["fecha_solicitud"].max())

print()

cruzan = fact_ordenes[fact_ordenes["fecha_solicitud"] > pd.Timestamp(config.FECHA_CORTE)]
print(len(cruzan))
print(cruzan["tipo_mantenimiento_id"].value_counts())