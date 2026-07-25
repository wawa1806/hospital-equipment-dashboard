# Dashboard de Gestión de Mantenimiento de Equipos Médicos Hospitalarios

Dashboard simulado para la gestión de mantenimiento con 2000 equipos médicos en un hospital sobre un pipelne de datos reproducible y testeado.

## Escenario
Hospital chieno de complejidad media-alta con 2000 equipos, en una ventana desde el 1 de Enero de 2023 hasta el 30 de Junio de 2026, generandose un corte, por lo que equipos con ordenes después del corte no son evaluables. Conjunto de datos sintéticos y reproducibles con SEED. Los hospitales y clínicas gestionan cientos de equipos médicos, cuya información suele registrarse en varias planillas. Parte de la complejidad de esto es la dificultad de desglosar costos anuales o mensuales, mantenciones o decisiones sobre ciertos equipos, etc.

## El dashboard
### Página 1 — Resumen Ejecutivo
![...](docs/img/Pag1_Resumen.png)
Monitorea el año en curso vs el año anterior, los costos actuales del año.

### Página 2 — Confiabilidad y Mantenimiento
![...](docs/img/Pag2_Confiabilidad_y_Mantenimiento.png)
MTBF, MTTR por clase, cumplimiento del plan por año, total de ordenes por servicio y por año-mes.

### Página 3 — Costos y Garantía
![...](docs/img/Pag3_Costos_y_Garantia.png)
Gasto en el tiempo, desglose del gasto en clases y tipo de mantención, estado de garantía.

### Página 4 — Detalle Clase Funcional
![...](docs/img/Pag4_Detalle_Clase_Funcional.png)
Drill-through de clase funcional de visualización MTBF por Clase Funcional; informa costos, órdenes, fallas.

## Arquitectura de datos
[Modelo estrella: 4 dims + 2 facts. Drill-across vía dimensiones conformadas.]
```mermaid
erDiagram
    dim_equipo||--o{ fact_ordenes_trabajo :  ""
    dim_ubicacion||--o{ fact_ordenes_trabajo : ""
    dim_tecnico||--o{ fact_ordenes_trabajo : ""
    dim_tipo_mantenimiento||--o{ fact_ordenes_trabajo : ""
    dim_fecha||--o{ fact_ordenes_trabajo : ""
    dim_fecha||--o{ fact_plan_mantenimiento : ""
    dim_equipo||--o{ fact_plan_mantenimiento : ""
    dim_tipo_mantenimiento||--o{ fact_plan_mantenimiento : ""

    
    fact_ordenes_trabajo{
        int orden_id PK
        int equipo_id FK
        int ubicacion_id FK
        int tecnico_id FK
        int tipo_mantenimiento_id FK
        date fecha_solicitud FK
        date fecha_inicio
        date fecha_cierre
        float costo_repuestos
        float costo_mano_obra
        float horas_detencion
        string falla_reportada
    }
    
    fact_plan_mantenimiento{
        int equipo_id FK
        date fecha_planificada FK 
        int tipo_mantenimiento_id FK
    }

    dim_equipo{
        int equipo_id PK
        string codigo_inventario
        string numero_serie
        string nombre_equipo
        string clase_funcional
        string marca
        string modelo
        string clase_riesgo
        string criticidad
        date fecha_adquisicion
        float costo_adquisicion
        int vida_util_anios
        string modalidad_propiedad
        date fecha_vencimiento_garantia
        bool bajo_plan_mantenimiento
        string estrategia_mantenimiento
        string estado_actual
    }

    dim_ubicacion{
        int ubicacion_id PK
        string servicio_clinico
        string piso
        string edificio
    }

    dim_tecnico{
        int tecnico_id PK
        string nombre
        string tipo
        string especialidad
    }

    dim_tipo_mantenimiento{
        int tipo_mantenimiento_id PK
        string nombre_tipo
    }

    dim_fecha{
        date fecha PK
        int anio
        string anio-mes
        string mes_nombre
        int mes_num
        string dia_semana_nombre
        int dia_semana_num
        bool es_fin_de_semana
        bool es_futuro
        string trimestre
    }
```
fact_ordenes transaccional, fact_plan factless, dim_fecha en DAX

## Stack
[Python · Power BI · pytest · ruff · GitHub Actions]

