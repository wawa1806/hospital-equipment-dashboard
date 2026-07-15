import numpy as np
import pandas as pd
from datetime import date, timedelta

from data_generator import catalog, config


def _sortear_ubicacion(
    rng, equipo_id, nombre, ubicacion_habitual, ubicacion_id_por_servicio
) -> int:
    """Ubicación habitual del equipo, o préstamo (PCT_EQUIPO_PRESTADO) a otro servicio de su clase."""
    if rng.random() < config.PCT_EQUIPO_PRESTADO:
        clase = catalog.CLASE_POR_EQUIPO[nombre]
        servicio = rng.choice(catalog.SERVICIOS_POR_CLASE[clase])
        return ubicacion_id_por_servicio[servicio]
    return ubicacion_habitual[equipo_id]


def generar_fact_ordenes(
    rng: np.random.Generator,
    dim_equipo: pd.DataFrame,
    dim_ubicacion: pd.DataFrame,
    dim_tecnico: pd.DataFrame,
    fact_plan: pd.DataFrame,
) -> pd.DataFrame:

    ubicacion_id_por_servicio = dict(
        zip(dim_ubicacion["servicio_clinico"], dim_ubicacion["ubicacion_id"])
    )
    ubicacion_habitual: dict[int, int] = {}
    for equipo_id, nombre in zip(dim_equipo["equipo_id"], dim_equipo["nombre_equipo"]):
        clase = catalog.CLASE_POR_EQUIPO[nombre]
        servicio = rng.choice(catalog.SERVICIOS_POR_CLASE[clase])
        ubicacion_habitual[equipo_id] = ubicacion_id_por_servicio[servicio]

    tecnicos_por_especialidad = (
        dim_tecnico.groupby("especialidad")["tecnico_id"].apply(list).to_dict()
    )

    ejecutables = fact_plan[fact_plan["fecha_planificada"] <= config.FECHA_CORTE]
    se_ejecuta = rng.random(len(ejecutables)) < (1 - config.PCT_INCUMPLIMIENTO_PLAN)
    ejecutadas = ejecutables[se_ejecuta].copy()

    ejecutadas = ejecutadas.merge(
        dim_equipo[
            [
                "equipo_id",
                "nombre_equipo",
                "costo_adquisicion",
                "clase_funcional",
                "estrategia_mantenimiento",
            ]
        ],
        on="equipo_id",
    )
    n = len(ejecutadas)

    fechas_np = np.array(ejecutadas["fecha_planificada"], dtype="datetime64[D]")
    desv = rng.integers(
        config.DESVIACION_DIAS_PLAN[0], config.DESVIACION_DIAS_PLAN[1] + 1, size=n
    )
    ejecutadas["fecha_solicitud"] = np.busday_offset(fechas_np, desv, roll="forward")
    ejecutadas["fecha_solicitud"] = np.maximum(
        ejecutadas["fecha_solicitud"], np.datetime64(config.FECHA_INICIO)
    )

    ejecutadas = ejecutadas[
        ejecutadas["fecha_solicitud"] <= np.datetime64(config.FECHA_CORTE)
    ].copy()
    n = len(ejecutadas)

    espera = rng.integers(0, 3, size=n).astype("timedelta64[D]")
    ejecutadas["fecha_inicio"] = ejecutadas["fecha_solicitud"] + espera
    duracion = rng.integers(
        config.DURACION_DIAS_PREVENTIVA[0],
        config.DURACION_DIAS_PREVENTIVA[1] + 1,
        size=n,
    ).astype("timedelta64[D]")
    ejecutadas["fecha_cierre"] = ejecutadas["fecha_inicio"] + duracion

    fracciones = np.array(
        [
            rng.uniform(*config.FRACCION_COSTO_PREVENTIVA[nombre])
            for nombre in ejecutadas["nombre_equipo"]
        ]
    )
    ejecutadas["costo_repuestos"] = (
        fracciones * ejecutadas["costo_adquisicion"]
    ).round(-3)

    frac_mo = rng.uniform(*config.FRACCION_MANO_OBRA_PREVENTIVA, size=n)
    mano_obra_base = frac_mo * ejecutadas["costo_adquisicion"]
    es_gratis = ejecutadas["estrategia_mantenimiento"].isin(["Interno", "Contrato"])
    ejecutadas["costo_mano_obra"] = np.where(es_gratis, 0, mano_obra_base).round(-3)

    ejecutadas["horas_detencion"] = rng.uniform(
        *config.HORAS_DETENCION_PREVENTIVA, size=n
    ).round(1)
    ejecutadas["falla_reportada"] = None

    ejecutadas["tecnico_id"] = [
        int(
            rng.choice(tecnicos_por_especialidad[catalog.ESPECIALIDAD_POR_CLASE[clase]])
        )
        for clase in ejecutadas["clase_funcional"]
    ]

    ejecutadas["ubicacion_id"] = [
        _sortear_ubicacion(rng, eq, nom, ubicacion_habitual, ubicacion_id_por_servicio)
        for eq, nom in zip(ejecutadas["equipo_id"], ejecutadas["nombre_equipo"])
    ]

    equipo_ids = []
    anios = []
    fechas_solicitud = []
    fechas_inicio = []
    fechas_cierre = []
    horas = []
    fallas = []
    tecnicos = []
    costos_rep = []
    costos_mo = []
    ubicaciones_corr = []
    for equipo_id, nombre, fecha_adq, estado, garantia, costo_adq, estrategia in zip(
        dim_equipo["equipo_id"],
        dim_equipo["nombre_equipo"],
        dim_equipo["fecha_adquisicion"],
        dim_equipo["estado_actual"],
        dim_equipo["fecha_vencimiento_garantia"],
        dim_equipo["costo_adquisicion"],
        dim_equipo["estrategia_mantenimiento"],
    ):
        if estado in ("Malo", "Baja"):
            dias_hasta_corte = (config.FECHA_CORTE - fecha_adq).days
            if dias_hasta_corte <= 365:
                fecha_baja = config.FECHA_CORTE
            else:
                d = int(rng.integers(365, dias_hasta_corte))
                fecha_baja = fecha_adq + timedelta(days=d)
        else:
            fecha_baja = None

        extra = config.TASA_EXTRA_FALLA_INVIERNO.get(nombre, 0)
        pesos = np.array([1.0] * 12)
        pesos[[5, 6, 7]] += extra
        p_mes = pesos / pesos.sum()

        for anio in range(config.FECHA_INICIO.year, config.FECHA_CORTE.year + 1):
            edad = anio - fecha_adq.year
            if edad < 0:
                continue
            tasa = config.TASA_BASE_POR_EQUIPO[nombre] * max(
                0.1, 1 + (edad - config.EDAD_REFERENCIA) * config.FACTOR_EDAD
            )
            n_fallas = rng.poisson(tasa)
            for _ in range(n_fallas):
                mes = int(rng.choice(range(1, 13), p=p_mes))
                dia = int(rng.integers(1, 29))
                fecha_falla = date(anio, mes, dia)
                if (
                    fecha_falla > config.FECHA_CORTE
                    or fecha_falla < fecha_adq
                    or (fecha_baja is not None and fecha_falla > fecha_baja)
                ):
                    continue

                fechas_solicitud.append(fecha_falla)
                fechas_inicio.append(
                    fecha_falla + timedelta(days=int(rng.integers(0, 4)))
                )
                dur = int(
                    rng.integers(
                        config.DURACION_DIAS_CORRECTIVA[0],
                        config.DURACION_DIAS_CORRECTIVA[1] + 1,
                    )
                )
                fechas_cierre.append(fechas_inicio[-1] + timedelta(days=dur))
                horas.append(round(float(rng.uniform(8, min(300, dur * 24))), 1))
                fallas.append(str(rng.choice(catalog.FALLAS_POR_EQUIPO[nombre])))
                tecnicos.append(
                    int(
                        rng.choice(
                            tecnicos_por_especialidad[
                                catalog.ESPECIALIDAD_POR_CLASE[
                                    catalog.CLASE_POR_EQUIPO[nombre]
                                ]
                            ]
                        )
                    )
                )
                ubicaciones_corr.append(
                    _sortear_ubicacion(
                        rng,
                        equipo_id,
                        nombre,
                        ubicacion_habitual,
                        ubicacion_id_por_servicio,
                    )
                )

                frac = min(
                    rng.uniform(*config.FRACCION_COSTO_PREVENTIVA[nombre])
                    * config.FACTOR_COSTO_CORRECTIVO,
                    config.FRACCION_CORRECTIVA_MAX,
                )
                bajo_garantia = (garantia is not pd.NaT) and (fecha_falla <= garantia)
                costo_rep = (
                    0.0
                    if bajo_garantia
                    else min(round(frac * costo_adq, -3), config.COSTO_CORRECTIVO_MAX)
                )
                mo = (
                    min(
                        rng.uniform(*config.FRACCION_MANO_OBRA_PREVENTIVA)
                        * config.FACTOR_COSTO_CORRECTIVO,
                        config.FRACCION_MO_CORRECTIVA_MAX,
                    )
                    * costo_adq
                )
                costo_mo = (
                    0.0
                    if (bajo_garantia or estrategia in ("Interno", "Contrato"))
                    else round(mo, -3)
                )
                costos_rep.append(costo_rep)
                costos_mo.append(costo_mo)

                equipo_ids.append(equipo_id)
                anios.append(anio)

    correctivas = pd.DataFrame(
        {
            "equipo_id": equipo_ids,
            "ubicacion_id": ubicaciones_corr,
            "tecnico_id": tecnicos,
            "tipo_mantenimiento_id": 2,
            "fecha_solicitud": fechas_solicitud,
            "fecha_inicio": fechas_inicio,
            "fecha_cierre": fechas_cierre,
            "costo_repuestos": costos_rep,
            "costo_mano_obra": costos_mo,
            "horas_detencion": horas,
            "falla_reportada": fallas,
        }
    )

    dias_al_corte = np.array(
        [(config.FECHA_CORTE - f).days for f in correctivas["fecha_solicitud"]]
    )
    abierta = (dias_al_corte <= config.VENTANA_ABIERTAS_DIAS) & (
        rng.random(len(correctivas)) < config.PCT_ABIERTA_SI_RECIENTE
    )
    correctivas.loc[abierta, "fecha_cierre"] = pd.NaT
    correctivas.loc[abierta, "horas_detencion"] = np.nan

    columnas = [
        "equipo_id",
        "ubicacion_id",
        "tecnico_id",
        "tipo_mantenimiento_id",
        "fecha_solicitud",
        "fecha_inicio",
        "fecha_cierre",
        "costo_repuestos",
        "costo_mano_obra",
        "horas_detencion",
        "falla_reportada",
    ]
    df = pd.concat([ejecutadas[columnas], correctivas[columnas]], ignore_index=True)

    for col in ["fecha_solicitud", "fecha_inicio", "fecha_cierre"]:
        df[col] = pd.to_datetime(df[col])
    df = df.sort_values("fecha_solicitud").reset_index(drop=True)
    df["orden_id"] = np.arange(1, len(df) + 1)

    return df[["orden_id"] + columnas]
