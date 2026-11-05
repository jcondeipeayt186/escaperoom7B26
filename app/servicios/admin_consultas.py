"""Consultas de solo lectura para el panel de administración."""

from datetime import date, datetime, time, timedelta
from math import ceil
from urllib.parse import urlencode

from ..db import get_db
from .admin_tablas import TABLAS, normalizar_clave, resolver_filtros

POR_PAGINA = 25


def _escapar_like(texto):
    """Escapa los comodines de ``LIKE`` para buscar el texto literal."""

    return (
        texto.replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def _entero(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _fecha(valor):
    try:
        return date.fromisoformat(str(valor).strip())
    except (TypeError, ValueError):
        return None


def listar(tabla, args):
    """Devuelve las filas filtradas, ordenadas y paginadas de una tabla."""

    meta = TABLAS[tabla]
    filtros = resolver_filtros(meta)
    valores = {}

    condiciones = []
    parametros = []

    busqueda = args.get("q", "").strip()
    if busqueda and meta["busqueda"]:
        patron = f"%{_escapar_like(busqueda)}%"
        condiciones.append(
            "("
            + " OR ".join(
                f"{columna} LIKE %s ESCAPE '\\\\'"
                for columna in meta["busqueda"]
            )
            + ")"
        )
        parametros.extend([patron] * len(meta["busqueda"]))

    for filtro in filtros:
        valor = args.get(filtro["param"], "").strip()
        valores[filtro["param"]] = valor
        if not valor:
            continue

        if filtro["tipo"] == "numero":
            numero = _entero(valor)
            if numero is None:
                valores[filtro["param"]] = ""
                continue
            condiciones.append(f'{filtro["columna"]} = %s')
            parametros.append(numero)
            continue

        validos = {opcion["valor"] for opcion in filtro["opciones"]}
        if valor not in validos:
            valores[filtro["param"]] = ""
            continue
        condiciones.append(f'{filtro["columna"]} = %s')
        parametros.append(valor)

    desde_texto = args.get("desde", "").strip()
    hasta_texto = args.get("hasta", "").strip()
    valores["desde"] = desde_texto
    valores["hasta"] = hasta_texto

    columna_fecha = meta.get("columna_fecha")
    if columna_fecha:
        desde = _fecha(desde_texto) if desde_texto else None
        hasta = _fecha(hasta_texto) if hasta_texto else None
        if desde_texto and desde is None:
            valores["desde"] = ""
        if hasta_texto and hasta is None:
            valores["hasta"] = ""

        if desde is not None:
            condiciones.append(f"{columna_fecha} >= %s")
            parametros.append(datetime.combine(desde, time.min))
        if hasta is not None:
            condiciones.append(f"{columna_fecha} < %s")
            parametros.append(
                datetime.combine(hasta + timedelta(days=1), time.min)
            )

    orden = args.get("orden", meta["orden_default"]).strip()
    if orden not in meta["ordenes"]:
        orden = meta["orden_default"]

    direccion = args.get("dir", "asc").strip().lower()
    if direccion not in ("asc", "desc"):
        direccion = "asc"

    where_sql = (" WHERE " + " AND ".join(condiciones)) if condiciones else ""
    order_sql = (
        f'ORDER BY {meta["ordenes"][orden]["sql"]} {direccion.upper()}, '
        f'{meta["pk_sql"]} ASC'
    )

    with get_db().cursor() as cursor:
        cursor.execute(
            f'SELECT COUNT(*) AS total {meta["desde"]}{where_sql}',
            tuple(parametros),
        )
        total = int(cursor.fetchone()["total"])

        pagina = _entero(args.get("pagina", 1)) or 1
        pagina = max(1, pagina)
        total_paginas = max(1, ceil(total / POR_PAGINA))
        pagina = min(pagina, total_paginas)
        desplazamiento = (pagina - 1) * POR_PAGINA

        cursor.execute(
            f'SELECT {meta["select"]} {meta["desde"]}{where_sql} '
            f"{order_sql} LIMIT %s OFFSET %s",
            tuple(parametros) + (POR_PAGINA, desplazamiento),
        )
        filas = cursor.fetchall()

    opciones_orden = [
        {"valor": clave, "etiqueta": definicion["etiqueta"]}
        for clave, definicion in meta["ordenes"].items()
    ]

    parametros_consulta = {"q": busqueda, "orden": orden, "dir": direccion}
    for filtro in filtros:
        parametros_consulta[filtro["param"]] = valores[filtro["param"]]
    if columna_fecha:
        parametros_consulta["desde"] = valores["desde"]
        parametros_consulta["hasta"] = valores["hasta"]
    parametros_consulta = {
        clave: valor
        for clave, valor in parametros_consulta.items()
        if valor not in ("", None)
    }

    return {
        "tabla": tabla,
        "meta": meta,
        "filas": filas,
        "filtros": filtros,
        "valores": valores,
        "busqueda": busqueda,
        "orden": orden,
        "direccion": direccion,
        "ordenes": opciones_orden,
        "pagina": pagina,
        "total": total,
        "total_paginas": total_paginas,
        "por_pagina": POR_PAGINA,
        "desde_fila": desplazamiento + 1 if total else 0,
        "hasta_fila": min(desplazamiento + POR_PAGINA, total),
        "consulta": urlencode(parametros_consulta),
    }


def obtener_fila(tabla, clave):
    """Devuelve una fila con los mismos campos que el listado."""

    meta = TABLAS[tabla]
    try:
        clave = normalizar_clave(meta, clave)
    except ValueError:
        return None
    with get_db().cursor() as cursor:
        cursor.execute(
            f'SELECT {meta["select"]} {meta["desde"]} '
            f'WHERE {meta["pk_sql"]} = %s',
            (clave,),
        )
        return cursor.fetchone()


def valores_formulario(meta, fila):
    """Convierte una fila de la base en valores para el formulario."""

    datos = {}
    for nombre, campo in meta["campos"].items():
        valor = fila.get(campo["columna"])
        if campo["tipo"] == "checkbox":
            datos[nombre] = bool(valor)
        elif valor is None:
            datos[nombre] = ""
        else:
            datos[nombre] = str(valor)
    return datos


def valores_iniciales(meta):
    """Valores por defecto para un alta."""

    datos = {}
    for nombre, campo in meta["campos"].items():
        if campo["tipo"] == "checkbox":
            datos[nombre] = nombre == "activo"
        elif nombre == "dificultad":
            datos[nombre] = "inicial"
        else:
            datos[nombre] = ""
    return datos


def hay_intentos_activos():
    """Indica si hay equipos jugando en este momento."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM intento WHERE fecha_fin IS NULL"
        )
        return int(cursor.fetchone()["total"]) > 0


def obtener_intentos_activos():
    """Equipos jugando, estación actual y última actividad registrada."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT DATE_FORMAT(NOW(), %s) AS ahora",
            ("%d/%m/%Y %H:%i:%s",),
        )
        ahora = cursor.fetchone()["ahora"]

        cursor.execute(
            "SELECT i.id, i.equipo_id, e.nombre AS equipo_nombre, "
            "       i.dificultad, i.ultima_estacion_visitada, "
            "       es.nombre AS estacion_nombre, es.orden AS estacion_orden, "
            "       i.fecha_inicio, i.cantidad_ayudas, "
            "       GREATEST("
            "         i.fecha_inicio,"
            "         COALESCE(("
            "           SELECT MAX(ie.fecha) FROM intento_envio ie "
            "           WHERE ie.intento_id = i.id"
            "         ), i.fecha_inicio),"
            "         COALESCE(("
            "           SELECT MAX(re.fecha_respondida) FROM respuesta_elegida re "
            "           WHERE re.intento_id = i.id"
            "         ), i.fecha_inicio),"
            "         COALESCE(("
            "           SELECT MAX(ies.fecha_inicio) FROM intento_estacion ies "
            "           WHERE ies.intento_id = i.id"
            "         ), i.fecha_inicio)"
            "       ) AS ultima_actividad, "
            "       TIMESTAMPDIFF(SECOND, i.fecha_inicio, NOW()) AS transcurrido "
            "FROM intento i "
            "JOIN equipo e ON e.id = i.equipo_id "
            "JOIN estacion es ON es.id = i.ultima_estacion_visitada "
            "WHERE i.fecha_fin IS NULL "
            "ORDER BY i.fecha_inicio, i.id"
        )
        filas = cursor.fetchall()

    return {
        "filas": filas,
        "total": len(filas),
        "actualizado": ahora,
    }


def resumen_panel():
    """Conteos por tabla y estado general del juego."""

    tablas = []
    with get_db().cursor() as cursor:
        for nombre, meta in TABLAS.items():
            cursor.execute(
                f'SELECT COUNT(*) AS total FROM {meta["tabla_sql"]}'
            )
            total = int(cursor.fetchone()["total"])

            activos = None
            inactivos = None
            if meta["tiene_activo"]:
                cursor.execute(
                    f'SELECT SUM(activo = 1) AS activos, '
                    f'SUM(activo = 0) AS inactivos FROM {meta["tabla_sql"]}'
                )
                conteos = cursor.fetchone()
                activos = int(conteos["activos"] or 0)
                inactivos = int(conteos["inactivos"] or 0)

            tablas.append(
                {
                    "tabla": nombre,
                    "etiqueta": meta["etiqueta"],
                    "singular": meta["singular"],
                    "grupo": meta["grupo"],
                    "total": total,
                    "activos": activos,
                    "inactivos": inactivos,
                    "editable": bool(meta["campos"]),
                }
            )

        cursor.execute(
            "SELECT COUNT(*) AS intentos, COUNT(DISTINCT equipo_id) AS equipos "
            "FROM intento WHERE fecha_fin IS NULL"
        )
        estado = cursor.fetchone()

        cursor.execute(
            "SELECT MAX(fecha) AS ultima FROM ("
            "  SELECT MAX(fecha_inicio) AS fecha FROM intento"
            "  UNION ALL SELECT MAX(fecha) FROM intento_envio"
            "  UNION ALL SELECT MAX(fecha_fin) FROM intento"
            ") AS eventos"
        )
        ultima = cursor.fetchone()["ultima"]

    return {
        "tablas": tablas,
        "estado": {
            "intentos_activos": int(estado["intentos"] or 0),
            "equipos_jugando": int(estado["equipos"] or 0),
            "ultima_actividad": ultima,
        },
    }
