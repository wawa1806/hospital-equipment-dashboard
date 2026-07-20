# Tablas

### fact_ordenes_trabajo

Granularidad: una fila = una orden de trabajo.

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| orden_id | int | PK | Identificador único de la orden de trabajo | >= 1, autoincremental |
| equipo_id | int | FK | Identificador único del equipo | >= 1, autoincremental |
| ubicacion_id | int | FK | Identificador único de una ubicación física del recinto | >= 1, autoincremental |
| tecnico_id | int | FK | Identificador único del técnico a cargo de la orden | >= 1, autoincremental |
| tipo_mantenimiento_id | int | FK | Identificador único del tipo de mantenimiento a realizar | >= 1, autoincremental |
| fecha_solicitud | date | FK | Fecha de la solicitud de la orden de trabajo, relación principal con dim_fecha | Fechas entre 01/01/2023 y 30/06/2026|
| fecha_inicio | date | — | Fecha de inicio de la orden | - |
| fecha_cierre | date | — | Fecha de cierre de la orden | NULL si la orden sigue abierta |
| costo_repuestos | float | — | Costo en CLP de repuestos e insumos de la orden; aplica a todo tipo de mantención | Costo 0 CLP si no se usan repuestos |
| costo_mano_obra | float | — | Costo en CLP del trabajo realizado por el técnico; aplica a todo tipo de mantención | Costo 0 CLP si es técnico interno o garantía |
| horas_detencion | float | — | Cantidad de horas en el que el equipo está fuera de servicio | Si orden sigue abierta, horas_detención = NULL |
| falla_reportada | string | — | Falla o problema por el cual se inicio la orden de trabajo | Valores de acuerdo con el catálogo |

---

### fact_plan_mantenimiento

Granularidad: una fila = un equipo + un mes con mantención planificada de un tipo dado 

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| equipo_id | int | FK | Identificador único del equipo | >= 1, autoincremental |
| fecha_planificada | date | FK | Fecha planificada para realizar la mantención | Fechas entre 01/01/2023 y 31/12/2026 |
| tipo_mantenimiento_id | int | FK | Identificador único del tipo de mantenimiento | >= 1, autoincremental |

---

### dim_equipo

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

---


### dim_ubicacion

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| ubicacion_id | int | PK | Identificador único de una ubicación física del recinto | >= 1, autoincremental |
| servicio_clinico | string | - | Servicio clínico de la ubicación (UCI,UTI,etc) | Definidos en el catálogo |
| piso | string | - | Piso del edificio en el que se encuentra el equipo | Edificios(A-B) con 7 pisos, Edificios(C-D) con 4 pisos |
| edificio | string | - | Edificio en el que se encuentra el equipo | Edificios A-D |

---


### dim_tecnico

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| tecnico_id | int | PK | Identificador único del técnico a cargo de la orden | >= 1, autoincremental | 
| nombre | string | - | Nombre del técnico a cargo de la orden | Definidos en el catálogo |
| tipo | string | - | Tipo de técnico | Interno/Externo |
| especialidad | string | - | Especialidad del técnico | Definidos en el catálogo |

---

### dim_tipo_mantenimiento

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| tipo_mantenimiento_id | int | PK | Identificador único del tipo de mantenimiento a realizar | >= 1, autoincremental |
| nombre_tipo | string | - |Tipo de mantención | Preventiva/Correctiva |

---

### dim_fecha

| Columna | Tipo | Llave | Descripción | Valores válidos |
|---------|------|-------|-------------|-----------------|
| fecha | date | PK | Fecha calendario, granularidad día | 01/01/2023 - 31/12/2026 |
| anio | int | - | Año | 2023-2026 |
| mes | int | - | Meses | 1-12 |
| nombre_mes | string | - | Meses en nombre | Enero-Diciembre |
| trimestre | int | - | Empieza en Enero | 1-4 |
| dia_semana | int | - | Empieza lunes | 1-7 |
| es_fin_de_semana | bool | - | Identifica si el evento ocurrió en un fin de semana según fecha  |  True/False |
 
 ---

Limitaciones:
En estado_actual de dim_equipo se escoge SCD Tipo 1, es decir se deja el estado presente y no se tiene en cuenta el histórico.
En dim_ubicación, será la ubicación de la última orden.
Las columnas fecha_inicio y fecha_cierre tienen relaciones inactivas hacia dim_fecha
Unicidad por combinación en fact_plan_mantenimiento (equipo_id + fecha_planificada + tipo_mantenimiento_id)

Power BI:
dim_fecha se crea con CALENDAR
El dataset se congela por diseño , es_futuro hardcodea el corte 2026-06-30
No se incluyen feriados
MTTR mide tiempo promedio de reparación, se mide desde fecha_inicio a fecha_cierre, tomando en cuenta solo correctivas y órdenes cerradas (se excluyen abiertas). Se mide en días.
MTBF mide tiempo operativo total entre fallas, se toma en cuenta la fecha de adquisición para evitar una inflación de la métrica (Al medir 2000 equipos con una fecha de inicio igual), la versión naive sobreestimaba el tiempo operativo en 12%, el numerador refinado por fecha_adquisicion elimina esa sobreestimación. Sin embargo sigue limitado por los equipos que están en Baja (son 34) ya que no se incluye una fecha de baja.

Un plan se considera cumplido si existe al menos una orden preventiva del mismo equipo con fecha de inicio dentro de la fecha planificada con más o menos 7 días de tolerancia.
Por lo que el % Cumplimiento Plan = Planes Cumplidos / Planes Evaluables

Se considera:
Tolerancia/holgura de +- 7 días
La fecha_inicio es cuando se ejecuta la mantención
plan evaluable se refiere a planes cuya ventana completa se cierra antes del corte
Solo órdenes preventivas

% Correctivas Bajo Garantía informa sobre la cantidad de equipos que cuya fecha de solicitud esta antes del vencimiento de la garantía sobre el total de las órdenes correctivas

Disponibilidad informa sobre el % de disponibildad bruta de los equipos, midiendo la diferencia entre el total y el tiempo de detención. 