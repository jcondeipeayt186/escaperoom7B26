"""Atajos compartidos por los tests."""

from pathlib import Path

TOKEN_PRUEBA = "token-de-pruebas-estable"

RAIZ = Path(__file__).resolve().parents[1]
SEEDS = (
    RAIZ / "bd" / "seeds" / "001_contenido_inicial.sql",
    RAIZ / "bd" / "seeds" / "002_contenido_intermedio.sql",
    RAIZ / "bd" / "seeds" / "003_contenido_avanzado.sql",
)


def _sentencias(texto):
    """Separa un script SQL simple por punto y coma, sin ejecutar comentarios."""

    for fragmento in texto.split(";"):
        if not fragmento.strip():
            continue
        sin_comentarios = "\n".join(
            linea
            for linea in fragmento.splitlines()
            if not linea.strip().startswith("--")
        )
        if not sin_comentarios.strip():
            continue
        yield fragmento


def aplicar_seed(db, base):
    """Reejecuta todos los seeds sobre ``base`` con la conexión ya abierta."""

    with db.cursor() as cursor:
        for seed in SEEDS:
            texto = seed.read_text(encoding="utf-8").replace(
                "escape_room_7b2026", base
            )
            for sentencia in _sentencias(texto):
                cursor.execute(sentencia)


def token_csrf(cliente):
    """Devuelve el token de la sesión, creándolo si el test no visitó una página."""

    with cliente.session_transaction() as sesion:
        token = sesion.get("csrf_token")
        if not token:
            token = TOKEN_PRUEBA
            sesion["csrf_token"] = token
        return token


def post(cliente, url, datos=None, **kwargs):
    """POST con el token CSRF de la sesión y los datos indicados."""

    cuerpo = dict(datos or {})
    cuerpo.setdefault("csrf_token", token_csrf(cliente))
    return cliente.post(url, data=cuerpo, **kwargs)


def iniciar_sesion(cliente, equipo_id, intento_id):
    with cliente.session_transaction() as sesion:
        sesion["equipo_id"] = equipo_id
        sesion["intento_id"] = intento_id


def cerrar_sesion(cliente):
    with cliente.session_transaction() as sesion:
        sesion.pop("equipo_id", None)
        sesion.pop("intento_id", None)


def fila(db, sql, parametros=()):
    with db.cursor() as cursor:
        cursor.execute(sql, parametros)
        return cursor.fetchone()


def filas(db, sql, parametros=()):
    with db.cursor() as cursor:
        cursor.execute(sql, parametros)
        return cursor.fetchall()


def ejecutar(db, sql, parametros=()):
    with db.cursor() as cursor:
        cursor.execute(sql, parametros)
        return cursor.lastrowid


def estacion_inicial(db):
    return fila(
        db,
        "SELECT id FROM estacion WHERE activo = 1 ORDER BY orden LIMIT 1",
    )["id"]


def crear_equipo(db, nombre, cantidad=2, dificultad="inicial"):
    """Crea equipo e intento activo y devuelve sus ids."""

    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) VALUES (%s, %s)",
        (nombre, cantidad),
    )
    intento_id = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, ultima_estacion_visitada) "
        "VALUES (%s, %s, NOW(3), %s)",
        (equipo_id, dificultad, estacion_inicial(db)),
    )
    return equipo_id, intento_id


def preparar_por_url(cliente, db, intento_id, orden=1):
    """Entra a la estación por la ruta real y devuelve preguntas congeladas."""

    respuesta = cliente.get(f"/juego/estacion/{orden}")
    assert respuesta.status_code == 200, respuesta.get_data(as_text=True)
    estacion_id = fila(
        db,
        "SELECT id FROM estacion WHERE activo = 1 AND orden = %s",
        (orden,),
    )["id"]
    return estacion_id, preguntas_del_intento(db, intento_id, estacion_id)


def preguntas_del_intento(db, intento_id, estacion_id):
    """Preguntas congeladas con sus opciones y cuál es la correcta."""

    registros = filas(
        db,
        "SELECT ip.pregunta_id, ip.orden, r.id AS respuesta_id, r.correcta "
        "FROM intento_pregunta ip "
        "JOIN respuesta r ON r.pregunta_id = ip.pregunta_id "
        "WHERE ip.intento_id = %s AND ip.estacion_id = %s "
        "ORDER BY ip.orden, r.id",
        (intento_id, estacion_id),
    )
    preguntas = {}
    for registro in registros:
        pregunta = preguntas.setdefault(
            registro["pregunta_id"],
            {
                "id": registro["pregunta_id"],
                "orden": registro["orden"],
                "correcta": None,
                "incorrectas": [],
            },
        )
        if registro["correcta"]:
            pregunta["correcta"] = registro["respuesta_id"]
        else:
            pregunta["incorrectas"].append(registro["respuesta_id"])

    return sorted(preguntas.values(), key=lambda item: item["orden"])


def formulario(preguntas, incorrectas=0):
    """Arma un envío con las primeras ``incorrectas`` respuestas falladas."""

    datos = {}
    for indice, pregunta in enumerate(preguntas):
        if indice < incorrectas:
            datos[f"pregunta_{pregunta['id']}"] = pregunta["incorrectas"][0]
        else:
            datos[f"pregunta_{pregunta['id']}"] = pregunta["correcta"]
    return datos


def enviar(cliente, orden, datos):
    return post(cliente, f"/juego/estacion/{orden}/responder", datos)


def completar_estacion(cliente, db, intento_id, orden):
    """Responde las 4 preguntas correctas y devuelve la respuesta del POST."""

    estacion_id, preguntas = preparar_por_url(
        cliente, db, intento_id, orden
    )
    return estacion_id, enviar(cliente, orden, formulario(preguntas))


def fila_tiempo(db, intento_id, estacion_id):
    return fila(
        db,
        "SELECT ie.fecha_inicio, ie.fecha_fin, ie.completada "
        "FROM intento_estacion ie "
        "WHERE ie.intento_id = %s AND ie.estacion_id = %s",
        (intento_id, estacion_id),
    )


def estado_intento(db, intento_id):
    return fila(
        db,
        "SELECT finalizado, fecha_fin, puntaje_obtenido, cantidad_ayudas "
        "FROM intento WHERE id = %s",
        (intento_id,),
    )


def conteo(db, tabla, condiciones="", parametros=()):
    return fila(
        db, f"SELECT COUNT(*) AS total FROM {tabla} {condiciones}", parametros
    )["total"]


def login_admin(cliente, credenciales):
    cliente.get("/admin")
    return post(
        cliente,
        "/admin/login",
        {
            "usuario": credenciales["usuario"],
            "clave": credenciales["clave"],
        },
    )
