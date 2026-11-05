"""Métricas y gráficos del panel de administración.

Todas las cifras se calculan en MySQL y se devuelven listas para dibujar
barras con CSS en el servidor. Los filtros por fecha y dificultad se aplican
sobre ``intento.fecha_inicio`` e ``intento.dificultad``.
"""

from datetime import date, datetime, time, timedelta

from ..db import get_db
from .configuracion import DIFICULTADES, ETIQUETAS_DIFICULTAD

_ESTADOS = (
    (None, "en_curso", "En curso"),
    ("completo", "completo", "Completos"),
    ("abandono", "abandono", "Abandonos"),
    ("por_tiempo", "por_tiempo", "Por tiempo"),
    ("por_respuestas_incorrectas", "por_fallas", "Por respuestas fallidas"),
)


def _fecha(valor):
    try:
        return date.fromisoformat(str(valor).strip())
    except (TypeError, ValueError):
        return None


def _where(condiciones, extra=None):
    todas = list(condiciones)
    if extra:
        todas.append(extra)
    return (" WHERE " + " AND ".join(todas)) if todas else ""


def _leer_filtros(args):
    desde_texto = (args.get("desde") or "").strip()
    hasta_texto = (args.get("hasta") or "").strip()
    dificultad = (args.get("dificultad") or "").strip()

    if dificultad not in DIFICULTADES:
        dificultad = ""

    desde = _fecha(desde_texto) if desde_texto else None
    hasta = _fecha(hasta_texto) if hasta_texto else None

    if desde_texto and desde is None:
        desde_texto = ""
    if hasta_texto and hasta is None:
        hasta_texto = ""

    rango_invalido = bool(desde and hasta and desde > hasta)

    condiciones = []
    parametros = []

    if rango_invalido:
        condiciones.append("1 = 0")
    else:
        if desde is not None:
            condiciones.append("i.fecha_inicio >= %s")
            parametros.append(datetime.combine(desde, time.min))
        if hasta is not None:
            condiciones.append("i.fecha_inicio < %s")
            parametros.append(datetime.combine(hasta + timedelta(days=1), time.min))

    if dificultad:
        condiciones.append("i.dificultad = %s")
        parametros.append(dificultad)

    return {
        "valores": {
            "desde": desde_texto,
            "hasta": hasta_texto,
            "dificultad": dificultad,
        },
        "condiciones": condiciones,
        "parametros": tuple(parametros),
        "rango_invalido": rango_invalido,
    }


def _porcentaje(parte, total):
    return round(parte * 100 / total, 1) if total else 0.0


def obtener_estadisticas(args):
    """Calcula los agregados del admin para los filtros recibidos."""

    filtros = _leer_filtros(args)
    condiciones = filtros["condiciones"]
    parametros = filtros["parametros"]
    where_base = _where(condiciones)
    where_finalizados = _where(condiciones, "i.finalizado IS NOT NULL")
    where_completos = _where(condiciones, "i.finalizado = 'completo'")

    with get_db().cursor() as cursor:
        cursor.execute(
            f"SELECT COUNT(*) AS total FROM intento i {where_base}",
            parametros,
        )
        intentos_iniciados = int(cursor.fetchone()["total"])

        cursor.execute(
            f"SELECT COUNT(DISTINCT i.equipo_id) AS total "
            f"FROM intento i {where_base}",
            parametros,
        )
        equipos = int(cursor.fetchone()["total"])

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM intento i "
            f"{where_finalizados}",
            parametros,
        )
        intentos_finalizados = int(cursor.fetchone()["total"])

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM intento i "
            f"{where_completos}",
            parametros,
        )
        intentos_completados = int(cursor.fetchone()["total"])

        cursor.execute(
            f"SELECT COALESCE("
            f"  ROUND(AVG(TIMESTAMPDIFF(SECOND, i.fecha_inicio, i.fecha_fin))),"
            f"  0"
            f") AS promedio "
            f"FROM intento i "
            f"{where_completos}",
            parametros,
        )
        promedio_completados = int(cursor.fetchone()["promedio"] or 0)

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM respuesta_elegida re "
            f"JOIN intento i ON i.id = re.intento_id {where_base}",
            parametros,
        )
        respuestas_realizadas = int(cursor.fetchone()["total"])

        cursor.execute(
            f"SELECT COALESCE(SUM(env.respuestas_correctas), 0) AS aciertos "
            f"FROM intento_envio env "
            f"JOIN intento i ON i.id = env.intento_id {where_base}",
            parametros,
        )
        aciertos = int(cursor.fetchone()["aciertos"] or 0)

        cursor.execute(
            f"SELECT i.finalizado, COUNT(*) AS total "
            f"FROM intento i {where_base} "
            f"GROUP BY i.finalizado",
            parametros,
        )
        por_estado = {
            fila["finalizado"]: int(fila["total"]) for fila in cursor.fetchall()
        }

        cursor.execute(
            "SELECT e.id, e.nombre, e.orden, COUNT(ie.id) AS muestras, "
            "       COALESCE(ROUND(AVG(TIMESTAMPDIFF("
            "         SECOND, ie.fecha_inicio, ie.fecha_fin"
            "       ))), 0) AS promedio "
            "FROM estacion e "
            "LEFT JOIN intento_estacion ie "
            "  ON ie.estacion_id = e.id "
            " AND ie.completada = 1 "
            " AND ie.fecha_fin IS NOT NULL "
            f" AND EXISTS (SELECT 1 FROM intento i {where_base}) "
            "GROUP BY e.id, e.nombre, e.orden "
            "ORDER BY e.orden, e.id",
            parametros,
        )
        estaciones = [
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "orden": fila["orden"],
                "muestras": int(fila["muestras"] or 0),
                "promedio": int(fila["promedio"] or 0),
            }
            for fila in cursor.fetchall()
        ]

        cursor.execute(
            "SELECT p.id, p.titulo, p.dificultad, p.activo, "
            "       t.nombre AS tema_nombre, e.nombre AS estacion_nombre, "
            "       e.orden AS estacion_orden, "
            "       COUNT(DISTINCT ip.intento_id) AS usos "
            "FROM pregunta p "
            "JOIN tema t ON t.id = p.tema_id "
            "JOIN estacion e ON e.id = t.estacion_id "
            "LEFT JOIN intento_pregunta ip "
            "  ON ip.pregunta_id = p.id "
            f" AND EXISTS (SELECT 1 FROM intento i {where_base}) "
            "WHERE p.activo = 1 "
            "   OR EXISTS ("
            "     SELECT 1 FROM intento_pregunta ip2 "
            "     WHERE ip2.pregunta_id = p.id"
            "   ) "
            "GROUP BY p.id, p.titulo, p.dificultad, p.activo, t.nombre, "
            "         e.nombre, e.orden "
            "ORDER BY usos DESC, p.id",
            parametros,
        )
        preguntas = [
            {
                "id": fila["id"],
                "titulo": fila["titulo"],
                "dificultad": fila["dificultad"],
                "activo": bool(fila["activo"]),
                "tema_nombre": fila["tema_nombre"],
                "estacion_nombre": fila["estacion_nombre"],
                "estacion_orden": fila["estacion_orden"],
                "usos": int(fila["usos"] or 0),
            }
            for fila in cursor.fetchall()
        ]

    estados = [
        {
            "clave": clave,
            "etiqueta": etiqueta,
            "total": por_estado.get(finalizado, 0),
        }
        for finalizado, clave, etiqueta in _ESTADOS
    ]

    maximo_estado = max((estado["total"] for estado in estados), default=0)
    for estado in estados:
        estado["porcentaje_total"] = _porcentaje(
            estado["total"], intentos_iniciados
        )
        estado["ancho"] = (
            round(estado["total"] * 100 / maximo_estado) if maximo_estado else 0
        )

    maximo_promedio = max(
        (estacion["promedio"] for estacion in estaciones), default=0
    )
    for estacion in estaciones:
        estacion["ancho"] = (
            round(estacion["promedio"] * 100 / maximo_promedio)
            if maximo_promedio
            else 0
        )

    for pregunta in preguntas:
        pregunta["porcentaje"] = _porcentaje(
            pregunta["usos"], intentos_iniciados
        )
        pregunta["ancho"] = min(100, round(pregunta["porcentaje"]))

    return {
        "filtros": filtros["valores"],
        "rango_invalido": filtros["rango_invalido"],
        "opciones_dificultad": [
            {"valor": dificultad, "etiqueta": ETIQUETAS_DIFICULTAD[dificultad]}
            for dificultad in DIFICULTADES
        ],
        "resumen": {
            "equipos": equipos,
            "intentos_iniciados": intentos_iniciados,
            "intentos_finalizados": intentos_finalizados,
            "intentos_completados": intentos_completados,
            "promedio_completados": promedio_completados,
            "respuestas_realizadas": respuestas_realizadas,
            "aciertos": aciertos,
            "porcentaje_aciertos": _porcentaje(aciertos, respuestas_realizadas),
        },
        "estados": estados,
        "estaciones": estaciones,
        "preguntas": preguntas,
    }
