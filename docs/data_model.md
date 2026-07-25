# Modelo de datos

Este diagrama se basa en un escenario simulado de un establaceimiento de salud de mediana-alta complejidad con 4 edificios, 2 edificios de 7 pisos y 2 de 4 pisos. El recinto posee 2000 equipos médicos totales, abarcando distintas clases de riesgo.

En tabla fact_ordenes de trabajo, una fila corresponderá a una orden de trabajo.

En tabla fact_plan_mantenimiento, una fila corresponde un equipo con su mes de mantención planificado.
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