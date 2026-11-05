"""Definición de las tablas y campos que administra el panel.

Toda la metadata de esta módulo es fija: los nombres de tablas y columnas que
se interpolan en el SQL salen de acá, nunca de la URL ni del formulario.
"""

from ..db import get_db

DIFICULTADES = ("inicial", "intermedio", "avanzado")

OPCIONES_ACTIVO = [
    {"valor": "1", "etiqueta": "Activos"},
    {"valor": "0", "etiqueta": "Inactivos"},
]
OPCIONES_SI_NO = [
    {"valor": "1", "etiqueta": "Sí"},
    {"valor": "0", "etiqueta": "No"},
]
OPCIONES_DIFICULTAD = [
    {"valor": dificultad, "etiqueta": dificultad.capitalize()}
    for dificultad in DIFICULTADES
]
OPCIONES_FINALIZADO = [
    {"valor": "completo", "etiqueta": "Completo"},
    {"valor": "abandono", "etiqueta": "Abandono"},
    {
        "valor": "por_respuestas_incorrectas",
        "etiqueta": "Por respuestas incorrectas",
    },
    {"valor": "por_tiempo", "etiqueta": "Por tiempo"},
]

# Claves de configuración que no se editan desde este formulario.
CLAVES_SOLO_LECTURA = {
    "dificultad_intermedia_habilitada",
    "dificultad_avanzada_habilitada",
    "preguntas_por_estacion",
    "max_temas_por_estacion",
}

# Parámetros del juego: se editan con rango y se bloquean con intentos activos.
CLAVES_JUEGO = {
    "duracion_estacion_segundos": {"minimo": 30, "maximo": 3600},
    "max_ayudas_estacion": {"minimo": 1, "maximo": 10},
    "max_envios_estacion": {"minimo": 1, "maximo": 10},
    "max_respuestas_incorrectas": {"minimo": 1, "maximo": 10},
    "max_integrantes_equipo": {"minimo": 1, "maximo": 4},
}


def _col(campo, etiqueta, formato="texto", recortar=False):
    return {
        "campo": campo,
        "etiqueta": etiqueta,
        "formato": formato,
        "recortar": recortar,
    }


def _filtro(param, etiqueta, columna, opciones=None, fuente=None, tipo="select"):
    return {
        "param": param,
        "etiqueta": etiqueta,
        "columna": columna,
        "opciones": opciones,
        "fuente": fuente,
        "tipo": tipo,
    }


def _campo(
    nombre,
    etiqueta,
    tipo="texto",
    columna=None,
    obligatorio=True,
    maximo=None,
    minimo=None,
    maximo_numero=None,
    minimo_numero=None,
    ayuda=None,
    fuente=None,
    opciones=None,
):
    return {
        "nombre": nombre,
        "etiqueta": etiqueta,
        "tipo": tipo,
        "columna": columna or nombre,
        "obligatorio": obligatorio,
        "maximo": maximo,
        "minimo": minimo,
        "maximo_numero": maximo_numero,
        "minimo_numero": minimo_numero,
        "ayuda": ayuda,
        "fuente": fuente,
        "opciones": opciones,
        "solo_lectura": False,
    }


TABLAS = {
    "estacion": {
        "tabla_sql": "estacion",
        "etiqueta": "Estaciones",
        "singular": "Estación",
        "grupo": "contenido",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "e.id",
        "select": "e.id, e.nombre, e.descripcion, e.orden, e.activo",
        "desde": "FROM estacion e",
        "columnas": [
            _col("id", "ID"),
            _col("orden", "Orden"),
            _col("nombre", "Nombre"),
            _col("descripcion", "Descripción", recortar=True),
            _col("activo", "Estado", "activo"),
        ],
        "busqueda": ["e.nombre", "e.descripcion"],
        "columna_fecha": None,
        "filtros": [
            _filtro("activo", "Estado", "e.activo", opciones=OPCIONES_ACTIVO),
        ],
        "ordenes": {
            "id": {"sql": "e.id", "etiqueta": "ID"},
            "nombre": {"sql": "e.nombre", "etiqueta": "Nombre"},
            "orden": {"sql": "e.orden", "etiqueta": "Orden"},
            "activo": {"sql": "e.activo", "etiqueta": "Estado"},
        },
        "orden_default": "orden",
        "tiene_activo": True,
        "campos": {
            "nombre": _campo(
                "nombre", "Nombre", maximo=80, ayuda="Máximo 80 caracteres."
            ),
            "descripcion": _campo(
                "descripcion",
                "Descripción",
                tipo="textarea",
                obligatorio=False,
                maximo=255,
            ),
            "orden": _campo(
                "orden",
                "Orden",
                tipo="numero",
                minimo_numero=1,
                maximo_numero=5,
                ayuda="Del 1 al 5. El orden es único, incluso entre inactivas.",
            ),
            "activo": _campo("activo", "Activa", tipo="checkbox"),
        },
    },
    "tema": {
        "tabla_sql": "tema",
        "etiqueta": "Temas",
        "singular": "Tema",
        "grupo": "contenido",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "t.id",
        "select": (
            "t.id, t.nombre, t.estacion_id, e.nombre AS estacion_nombre, t.activo"
        ),
        "desde": "FROM tema t JOIN estacion e ON e.id = t.estacion_id",
        "columnas": [
            _col("id", "ID"),
            _col("nombre", "Nombre"),
            _col("estacion_nombre", "Estación"),
            _col("activo", "Estado", "activo"),
        ],
        "busqueda": ["t.nombre", "e.nombre"],
        "columna_fecha": None,
        "filtros": [
            _filtro("activo", "Estado", "t.activo", opciones=OPCIONES_ACTIVO),
            _filtro(
                "estacion_id",
                "Estación",
                "t.estacion_id",
                fuente="estaciones",
            ),
        ],
        "ordenes": {
            "id": {"sql": "t.id", "etiqueta": "ID"},
            "nombre": {"sql": "t.nombre", "etiqueta": "Nombre"},
            "estacion": {"sql": "e.orden", "etiqueta": "Estación"},
            "activo": {"sql": "t.activo", "etiqueta": "Estado"},
        },
        "orden_default": "id",
        "tiene_activo": True,
        "campos": {
            "nombre": _campo("nombre", "Nombre", maximo=80),
            "estacion_id": _campo(
                "estacion_id",
                "Estación",
                tipo="select",
                fuente="estaciones",
            ),
            "activo": _campo("activo", "Activo", tipo="checkbox"),
        },
    },
    "pregunta": {
        "tabla_sql": "pregunta",
        "etiqueta": "Preguntas",
        "singular": "Pregunta",
        "grupo": "contenido",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "p.id",
        "select": (
            "p.id, p.titulo, p.descripcion, p.tema_id, t.nombre AS tema_nombre, "
            "e.id AS estacion_id, e.nombre AS estacion_nombre, p.dificultad, "
            "p.activo"
        ),
        "desde": (
            "FROM pregunta p "
            "JOIN tema t ON t.id = p.tema_id "
            "JOIN estacion e ON e.id = t.estacion_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("titulo", "Título", recortar=True),
            _col("tema_nombre", "Tema"),
            _col("estacion_nombre", "Estación"),
            _col("dificultad", "Dificultad", "dificultad"),
            _col("activo", "Estado", "activo"),
        ],
        "busqueda": ["p.titulo", "p.descripcion", "t.nombre", "e.nombre"],
        "columna_fecha": None,
        "filtros": [
            _filtro("activo", "Estado", "p.activo", opciones=OPCIONES_ACTIVO),
            _filtro(
                "dificultad",
                "Dificultad",
                "p.dificultad",
                opciones=OPCIONES_DIFICULTAD,
            ),
            _filtro(
                "estacion_id",
                "Estación",
                "t.estacion_id",
                fuente="estaciones",
            ),
            _filtro("tema_id", "Tema", "p.tema_id", fuente="temas"),
        ],
        "ordenes": {
            "id": {"sql": "p.id", "etiqueta": "ID"},
            "titulo": {"sql": "p.titulo", "etiqueta": "Título"},
            "dificultad": {"sql": "p.dificultad", "etiqueta": "Dificultad"},
            "tema": {"sql": "t.nombre", "etiqueta": "Tema"},
            "activo": {"sql": "p.activo", "etiqueta": "Estado"},
        },
        "orden_default": "id",
        "tiene_activo": True,
        "campos": {
            "titulo": _campo("titulo", "Título", maximo=255),
            "descripcion": _campo(
                "descripcion",
                "Descripción",
                tipo="textarea",
                obligatorio=False,
                maximo=2000,
            ),
            "tema_id": _campo(
                "tema_id", "Tema", tipo="select", fuente="temas"
            ),
            "dificultad": _campo(
                "dificultad",
                "Dificultad",
                tipo="select",
                opciones=OPCIONES_DIFICULTAD,
            ),
            "activo": _campo("activo", "Activa", tipo="checkbox"),
        },
    },
    "respuesta": {
        "tabla_sql": "respuesta",
        "etiqueta": "Respuestas",
        "singular": "Respuesta",
        "grupo": "contenido",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "r.id",
        "select": (
            "r.id, r.contenido, r.correcta, r.pregunta_id, "
            "p.titulo AS pregunta_titulo, r.activo"
        ),
        "desde": "FROM respuesta r JOIN pregunta p ON p.id = r.pregunta_id",
        "columnas": [
            _col("id", "ID"),
            _col("contenido", "Contenido", recortar=True),
            _col("pregunta_titulo", "Pregunta", recortar=True),
            _col("correcta", "Correcta", "booleano"),
            _col("activo", "Estado", "activo"),
        ],
        "busqueda": ["r.contenido", "p.titulo"],
        "columna_fecha": None,
        "filtros": [
            _filtro("activo", "Estado", "r.activo", opciones=OPCIONES_ACTIVO),
            _filtro("correcta", "Correcta", "r.correcta", opciones=OPCIONES_SI_NO),
            _filtro(
                "pregunta_id",
                "Pregunta",
                "r.pregunta_id",
                fuente="preguntas",
            ),
        ],
        "ordenes": {
            "id": {"sql": "r.id", "etiqueta": "ID"},
            "contenido": {"sql": "r.contenido", "etiqueta": "Contenido"},
            "pregunta": {"sql": "p.titulo", "etiqueta": "Pregunta"},
            "correcta": {"sql": "r.correcta", "etiqueta": "Correcta"},
            "activo": {"sql": "r.activo", "etiqueta": "Estado"},
        },
        "orden_default": "id",
        "tiene_activo": True,
        "campos": {
            "contenido": _campo("contenido", "Contenido", maximo=255),
            "pregunta_id": _campo(
                "pregunta_id", "Pregunta", tipo="select", fuente="preguntas"
            ),
            "correcta": _campo(
                "correcta",
                "Es la respuesta correcta",
                tipo="checkbox",
                ayuda="Cada pregunta activa debe tener exactamente una correcta.",
            ),
            "activo": _campo("activo", "Activa", tipo="checkbox"),
        },
    },
    "configuracion": {
        "tabla_sql": "configuracion",
        "etiqueta": "Configuración",
        "singular": "Parámetro",
        "grupo": "contenido",
        "pk": "clave",
        "pk_col": "clave",
        "pk_sql": "c.clave",
        "select": "c.clave, c.valor",
        "desde": "FROM configuracion c",
        "columnas": [
            _col("clave", "Clave"),
            _col("valor", "Valor"),
        ],
        "busqueda": ["c.clave", "c.valor"],
        "columna_fecha": None,
        "filtros": [],
        "ordenes": {
            "clave": {"sql": "c.clave", "etiqueta": "Clave"},
            "valor": {"sql": "c.valor", "etiqueta": "Valor"},
        },
        "orden_default": "clave",
        "tiene_activo": False,
        "campos": {
            "clave": _campo(
                "clave",
                "Clave",
                maximo=80,
                ayuda="Solo minúsculas, números y guiones bajos. No se puede cambiar.",
            ),
            "valor": _campo("valor", "Valor", maximo=255),
        },
    },
    "equipo": {
        "tabla_sql": "equipo",
        "etiqueta": "Equipos",
        "singular": "Equipo",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "e.id",
        "select": "e.id, e.nombre, e.cantidad_personas, e.fecha_creacion",
        "desde": "FROM equipo e",
        "columnas": [
            _col("id", "ID"),
            _col("nombre", "Nombre"),
            _col("cantidad_personas", "Integrantes"),
            _col("fecha_creacion", "Creado", "fecha"),
        ],
        "busqueda": ["e.nombre"],
        "columna_fecha": "e.fecha_creacion",
        "filtros": [],
        "ordenes": {
            "id": {"sql": "e.id", "etiqueta": "ID"},
            "nombre": {"sql": "e.nombre", "etiqueta": "Nombre"},
            "cantidad": {
                "sql": "e.cantidad_personas",
                "etiqueta": "Integrantes",
            },
            "fecha": {"sql": "e.fecha_creacion", "etiqueta": "Fecha"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "intento": {
        "tabla_sql": "intento",
        "etiqueta": "Intentos",
        "singular": "Intento",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "i.id",
        "select": (
            "i.id, i.equipo_id, e.nombre AS equipo_nombre, i.dificultad, "
            "i.fecha_inicio, i.fecha_fin, i.se_completo_ok, i.cantidad_ayudas, "
            "i.puntaje_obtenido, i.finalizado, i.ultima_estacion_visitada"
        ),
        "desde": "FROM intento i JOIN equipo e ON e.id = i.equipo_id",
        "columnas": [
            _col("id", "ID"),
            _col("equipo_nombre", "Equipo"),
            _col("dificultad", "Dificultad", "dificultad"),
            _col("fecha_inicio", "Inicio", "fecha"),
            _col("fecha_fin", "Fin", "fecha"),
            _col("finalizado", "Resultado", "finalizado"),
            _col("cantidad_ayudas", "Ayudas"),
            _col("puntaje_obtenido", "Segundos"),
            _col("se_completo_ok", "Completó", "booleano"),
            _col("ultima_estacion_visitada", "Última estación"),
        ],
        "busqueda": ["e.nombre"],
        "columna_fecha": "i.fecha_inicio",
        "filtros": [
            _filtro(
                "dificultad",
                "Dificultad",
                "i.dificultad",
                opciones=OPCIONES_DIFICULTAD,
            ),
            _filtro(
                "finalizado",
                "Resultado",
                "i.finalizado",
                opciones=OPCIONES_FINALIZADO,
            ),
            _filtro("equipo_id", "Equipo", "i.equipo_id", fuente="equipos"),
        ],
        "ordenes": {
            "id": {"sql": "i.id", "etiqueta": "ID"},
            "inicio": {"sql": "i.fecha_inicio", "etiqueta": "Inicio"},
            "fin": {"sql": "i.fecha_fin", "etiqueta": "Fin"},
            "dificultad": {"sql": "i.dificultad", "etiqueta": "Dificultad"},
            "finalizado": {"sql": "i.finalizado", "etiqueta": "Resultado"},
            "puntaje": {"sql": "i.puntaje_obtenido", "etiqueta": "Segundos"},
            "ayudas": {"sql": "i.cantidad_ayudas", "etiqueta": "Ayudas"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "intento_estacion": {
        "tabla_sql": "intento_estacion",
        "etiqueta": "Intentos por estación",
        "singular": "Intento por estación",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "ie.id",
        "select": (
            "ie.id, ie.intento_id, ie.estacion_id, es.nombre AS estacion_nombre, "
            "ie.fecha_inicio, ie.fecha_fin, ie.ayudas, ie.completada"
        ),
        "desde": (
            "FROM intento_estacion ie "
            "JOIN estacion es ON es.id = ie.estacion_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("intento_id", "Intento"),
            _col("estacion_nombre", "Estación"),
            _col("fecha_inicio", "Inicio", "fecha"),
            _col("fecha_fin", "Fin", "fecha"),
            _col("ayudas", "Ayudas"),
            _col("completada", "Completada", "booleano"),
        ],
        "busqueda": ["CAST(ie.intento_id AS CHAR)", "es.nombre"],
        "columna_fecha": "ie.fecha_inicio",
        "filtros": [
            _filtro("intento_id", "Intento", "ie.intento_id", tipo="numero"),
            _filtro(
                "estacion_id",
                "Estación",
                "ie.estacion_id",
                fuente="estaciones",
            ),
            _filtro("completada", "Completada", "ie.completada", opciones=OPCIONES_SI_NO),
        ],
        "ordenes": {
            "id": {"sql": "ie.id", "etiqueta": "ID"},
            "inicio": {"sql": "ie.fecha_inicio", "etiqueta": "Inicio"},
            "fin": {"sql": "ie.fecha_fin", "etiqueta": "Fin"},
            "ayudas": {"sql": "ie.ayudas", "etiqueta": "Ayudas"},
            "completada": {"sql": "ie.completada", "etiqueta": "Completada"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "intento_envio": {
        "tabla_sql": "intento_envio",
        "etiqueta": "Envíos",
        "singular": "Envío",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "ie.id",
        "select": (
            "ie.id, ie.intento_id, ie.estacion_id, es.nombre AS estacion_nombre, "
            "ie.fecha, ie.respuestas_correctas, ie.respuestas_incorrectas"
        ),
        "desde": (
            "FROM intento_envio ie JOIN estacion es ON es.id = ie.estacion_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("intento_id", "Intento"),
            _col("estacion_nombre", "Estación"),
            _col("fecha", "Fecha", "fecha"),
            _col("respuestas_correctas", "Correctas"),
            _col("respuestas_incorrectas", "Incorrectas"),
        ],
        "busqueda": ["CAST(ie.intento_id AS CHAR)", "es.nombre"],
        "columna_fecha": "ie.fecha",
        "filtros": [
            _filtro("intento_id", "Intento", "ie.intento_id", tipo="numero"),
            _filtro(
                "estacion_id",
                "Estación",
                "ie.estacion_id",
                fuente="estaciones",
            ),
        ],
        "ordenes": {
            "id": {"sql": "ie.id", "etiqueta": "ID"},
            "fecha": {"sql": "ie.fecha", "etiqueta": "Fecha"},
            "correctas": {
                "sql": "ie.respuestas_correctas",
                "etiqueta": "Correctas",
            },
            "incorrectas": {
                "sql": "ie.respuestas_incorrectas",
                "etiqueta": "Incorrectas",
            },
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "intento_pregunta": {
        "tabla_sql": "intento_pregunta",
        "etiqueta": "Preguntas del intento",
        "singular": "Pregunta del intento",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "ip.id",
        "select": (
            "ip.id, ip.intento_id, ip.estacion_id, es.nombre AS estacion_nombre, "
            "ip.pregunta_id, p.titulo AS pregunta_titulo, ip.orden"
        ),
        "desde": (
            "FROM intento_pregunta ip "
            "JOIN estacion es ON es.id = ip.estacion_id "
            "JOIN pregunta p ON p.id = ip.pregunta_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("intento_id", "Intento"),
            _col("estacion_nombre", "Estación"),
            _col("pregunta_titulo", "Pregunta", recortar=True),
            _col("orden", "Orden"),
        ],
        "busqueda": ["CAST(ip.intento_id AS CHAR)", "p.titulo"],
        "columna_fecha": None,
        "filtros": [
            _filtro("intento_id", "Intento", "ip.intento_id", tipo="numero"),
            _filtro(
                "estacion_id",
                "Estación",
                "ip.estacion_id",
                fuente="estaciones",
            ),
        ],
        "ordenes": {
            "id": {"sql": "ip.id", "etiqueta": "ID"},
            "orden": {"sql": "ip.orden", "etiqueta": "Orden"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "respuesta_elegida": {
        "tabla_sql": "respuesta_elegida",
        "etiqueta": "Respuestas elegidas",
        "singular": "Respuesta elegida",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "re.id",
        "select": (
            "re.id, re.fecha_respondida, re.intento_id, re.intento_envio_id, "
            "p.id AS pregunta_id, p.titulo AS pregunta_titulo, re.respuesta_id, "
            "r.contenido AS respuesta_contenido"
        ),
        "desde": (
            "FROM respuesta_elegida re "
            "JOIN respuesta r ON r.id = re.respuesta_id "
            "JOIN pregunta p ON p.id = r.pregunta_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("fecha_respondida", "Fecha", "fecha"),
            _col("intento_id", "Intento"),
            _col("intento_envio_id", "Envío"),
            _col("pregunta_titulo", "Pregunta", recortar=True),
            _col("respuesta_contenido", "Respuesta", recortar=True),
        ],
        "busqueda": [
            "CAST(re.intento_id AS CHAR)",
            "p.titulo",
            "r.contenido",
        ],
        "columna_fecha": "re.fecha_respondida",
        "filtros": [
            _filtro("intento_id", "Intento", "re.intento_id", tipo="numero"),
            _filtro(
                "intento_envio_id",
                "Envío",
                "re.intento_envio_id",
                tipo="numero",
            ),
            _filtro(
                "pregunta_id",
                "Pregunta",
                "p.id",
                fuente="preguntas",
            ),
        ],
        "ordenes": {
            "id": {"sql": "re.id", "etiqueta": "ID"},
            "fecha": {"sql": "re.fecha_respondida", "etiqueta": "Fecha"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
    "incorrecta": {
        "tabla_sql": "incorrecta",
        "etiqueta": "Respuestas incorrectas",
        "singular": "Respuesta incorrecta",
        "grupo": "historico",
        "pk": "id",
        "pk_col": "id",
        "pk_sql": "inc.id",
        "select": (
            "inc.id, inc.pregunta_id, p.titulo AS pregunta_titulo, "
            "inc.respuesta_id, r.contenido AS respuesta_contenido, inc.fecha, "
            "inc.intento_id, inc.intento_envio_id"
        ),
        "desde": (
            "FROM incorrecta inc "
            "JOIN pregunta p ON p.id = inc.pregunta_id "
            "JOIN respuesta r ON r.id = inc.respuesta_id"
        ),
        "columnas": [
            _col("id", "ID"),
            _col("fecha", "Fecha", "fecha"),
            _col("intento_id", "Intento"),
            _col("intento_envio_id", "Envío"),
            _col("pregunta_titulo", "Pregunta", recortar=True),
            _col("respuesta_contenido", "Respuesta", recortar=True),
        ],
        "busqueda": [
            "CAST(inc.intento_id AS CHAR)",
            "p.titulo",
            "r.contenido",
        ],
        "columna_fecha": "inc.fecha",
        "filtros": [
            _filtro("intento_id", "Intento", "inc.intento_id", tipo="numero"),
            _filtro(
                "intento_envio_id",
                "Envío",
                "inc.intento_envio_id",
                tipo="numero",
            ),
            _filtro(
                "pregunta_id",
                "Pregunta",
                "inc.pregunta_id",
                fuente="preguntas",
            ),
        ],
        "ordenes": {
            "id": {"sql": "inc.id", "etiqueta": "ID"},
            "fecha": {"sql": "inc.fecha", "etiqueta": "Fecha"},
        },
        "orden_default": "id",
        "tiene_activo": False,
        "campos": {},
    },
}


def obtener_meta(tabla):
    """Devuelve la metadata de una tabla conocida o ``None``."""

    return TABLAS.get(tabla)


def normalizar_clave(meta, valor):
    """Convierte la clave de la URL al tipo de la clave primaria."""

    if meta["pk"] == "id":
        if not str(valor).isdigit():
            raise ValueError("La clave debe ser un número entero.")
        return int(valor)
    return str(valor)


def opciones_estaciones():
    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, orden, activo FROM estacion ORDER BY orden, id"
        )
        return [
            {
                "valor": str(fila["id"]),
                "etiqueta": (
                    f'#{fila["id"]} · {fila["nombre"]} (orden {fila["orden"]})'
                    + ("" if fila["activo"] else " — inactiva")
                ),
            }
            for fila in cursor.fetchall()
        ]


def opciones_temas():
    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT t.id, t.nombre, e.nombre AS estacion_nombre, t.activo "
            "FROM tema t JOIN estacion e ON e.id = t.estacion_id "
            "ORDER BY e.orden, t.nombre, t.id"
        )
        return [
            {
                "valor": str(fila["id"]),
                "etiqueta": (
                    f'#{fila["id"]} · {fila["nombre"]} — {fila["estacion_nombre"]}'
                    + ("" if fila["activo"] else " — inactivo")
                ),
            }
            for fila in cursor.fetchall()
        ]


def opciones_preguntas():
    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT p.id, p.titulo, p.dificultad, t.nombre AS tema_nombre, "
            "       e.nombre AS estacion_nombre, p.activo "
            "FROM pregunta p "
            "JOIN tema t ON t.id = p.tema_id "
            "JOIN estacion e ON e.id = t.estacion_id "
            "ORDER BY e.orden, t.nombre, p.id"
        )
        return [
            {
                "valor": str(fila["id"]),
                "etiqueta": (
                    f'#{fila["id"]} · {fila["titulo"]} — '
                    f'{fila["estacion_nombre"]} / {fila["tema_nombre"]} '
                    f'({fila["dificultad"]})'
                    + ("" if fila["activo"] else " — inactiva")
                ),
            }
            for fila in cursor.fetchall()
        ]


def opciones_equipos():
    with get_db().cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM equipo ORDER BY id")
        return [
            {
                "valor": str(fila["id"]),
                "etiqueta": f'#{fila["id"]} · {fila["nombre"]}',
            }
            for fila in cursor.fetchall()
        ]


FUENTES_OPCIONES = {
    "estaciones": opciones_estaciones,
    "temas": opciones_temas,
    "preguntas": opciones_preguntas,
    "equipos": opciones_equipos,
}


def resolver_filtros(meta):
    """Devuelve los filtros con sus opciones ya cargadas."""

    filtros = []
    for definicion in meta["filtros"]:
        filtro = dict(definicion)
        if filtro.get("fuente"):
            filtro["opciones"] = FUENTES_OPCIONES[filtro["fuente"]]()
        filtros.append(filtro)
    return filtros


def resolver_campos(meta):
    """Devuelve los campos del formulario con sus opciones ya cargadas."""

    campos = []
    for nombre, definicion in meta["campos"].items():
        campo = dict(definicion)
        campo["nombre"] = nombre
        if campo.get("fuente"):
            campo["opciones"] = FUENTES_OPCIONES[campo["fuente"]]()
        campos.append(campo)
    return campos
