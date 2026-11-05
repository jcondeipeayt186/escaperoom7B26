"""Altas, ediciones y bajas lógicas del panel de administración."""

import re

import pymysql

from ..db import transaction
from .admin_tablas import (
    CLAVES_JUEGO,
    CLAVES_SOLO_LECTURA,
    DIFICULTADES,
    TABLAS,
    normalizar_clave,
)

PATRON_CLAVE = re.compile(r"^[a-z][a-z0-9_]{0,79}$")


class ErrorAdmin(RuntimeError):
    """Un dato no cumple las reglas del panel."""

    def __init__(self, mensaje="No se pudo guardar.", errores=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.errores = errores or {}


def leer_formulario(meta, formulario):
    """Lee los campos declarados en la metadata y normaliza checkboxes."""

    datos = {}
    for nombre, campo in meta["campos"].items():
        if campo["tipo"] == "checkbox":
            datos[nombre] = formulario.get(nombre) == "1"
        else:
            datos[nombre] = formulario.get(nombre, "").strip()
    return datos


def crear(tabla, datos):
    """Crea una fila y devuelve su clave."""

    meta = TABLAS.get(tabla)
    if meta is None or not meta["campos"]:
        raise ErrorAdmin("Esa tabla es de solo lectura.")

    try:
        with transaction() as cursor:
            if tabla == "estacion":
                return _crear_estacion(cursor, datos)
            if tabla == "tema":
                return _crear_tema(cursor, datos)
            if tabla == "pregunta":
                return _crear_pregunta(cursor, datos)
            if tabla == "respuesta":
                return _crear_respuesta(cursor, datos)
            if tabla == "configuracion":
                return _crear_configuracion(cursor, datos)
    except pymysql.err.IntegrityError as error:
        raise ErrorAdmin(
            "No se pudo guardar: ya existe un registro con esos datos."
        ) from error

    raise ErrorAdmin("Esa tabla es de solo lectura.")


def actualizar(tabla, clave, datos):
    """Actualiza una fila existente."""

    meta = TABLAS.get(tabla)
    if meta is None or not meta["campos"]:
        raise ErrorAdmin("Esa tabla es de solo lectura.")

    clave = normalizar_clave(meta, clave)

    try:
        with transaction() as cursor:
            fila = _bloquear_fila(cursor, meta, clave)
            if fila is None:
                raise ErrorAdmin("No encontramos esa fila.")

            if tabla == "estacion":
                return _actualizar_estacion(cursor, datos, fila)
            if tabla == "tema":
                return _actualizar_tema(cursor, datos, fila)
            if tabla == "pregunta":
                return _actualizar_pregunta(cursor, datos, fila)
            if tabla == "respuesta":
                return _actualizar_respuesta(cursor, datos, fila)
            if tabla == "configuracion":
                return _actualizar_configuracion(cursor, datos, fila)
    except pymysql.err.IntegrityError as error:
        raise ErrorAdmin(
            "No se pudo guardar: ya existe un registro con esos datos."
        ) from error

    raise ErrorAdmin("Esa tabla es de solo lectura.")


def desactivar(tabla, clave):
    """Aplica una baja lógica a una fila de contenido."""

    meta = TABLAS.get(tabla)
    if meta is None or not meta["campos"] or not meta["tiene_activo"]:
        raise ErrorAdmin("Esa tabla es de solo lectura.")

    clave = normalizar_clave(meta, clave)

    try:
        with transaction() as cursor:
            fila = _bloquear_fila(cursor, meta, clave)
            if fila is None:
                raise ErrorAdmin("No encontramos esa fila.")
            if not bool(fila["activo"]):
                return

            if tabla == "estacion":
                return _actualizar_estacion(
                    cursor,
                    {
                        "nombre": fila["nombre"],
                        "descripcion": fila["descripcion"],
                        "orden": fila["orden"],
                        "activo": False,
                    },
                    fila,
                )
            if tabla == "tema":
                return _actualizar_tema(
                    cursor,
                    {
                        "nombre": fila["nombre"],
                        "estacion_id": fila["estacion_id"],
                        "activo": False,
                    },
                    fila,
                )
            if tabla == "pregunta":
                return _actualizar_pregunta(
                    cursor,
                    {
                        "titulo": fila["titulo"],
                        "descripcion": fila["descripcion"],
                        "tema_id": fila["tema_id"],
                        "dificultad": fila["dificultad"],
                        "activo": False,
                    },
                    fila,
                )
            if tabla == "respuesta":
                return _actualizar_respuesta(
                    cursor,
                    {
                        "contenido": fila["contenido"],
                        "pregunta_id": fila["pregunta_id"],
                        "correcta": bool(fila["correcta"]),
                        "activo": False,
                    },
                    fila,
                )
    except pymysql.err.IntegrityError as error:
        raise ErrorAdmin(
            "No se pudo desactivar: el registro está relacionado con otros datos."
        ) from error

    raise ErrorAdmin("Esa tabla es de solo lectura.")


# ---------------------------------------------------------------------------
# Estaciones
# ---------------------------------------------------------------------------


def _crear_estacion(cursor, datos):
    nombre, descripcion, orden, activo = _validar_estacion(datos)

    if _hay_intentos_activos(cursor):
        raise ErrorAdmin(
            "No se pueden crear estaciones mientras hay equipos jugando."
        )

    _comprobar_nombre_estacion(cursor, nombre)

    if _ordenes_ocupados(cursor) >= 5:
        raise ErrorAdmin(
            "Ya hay 5 estaciones con orden asignado. Para crear otra, primero "
            "liberá un orden editando una estación existente.",
            {"orden": "Los órdenes 1 a 5 están ocupados."},
        )

    if _estacion_por_orden(cursor, orden) is not None:
        raise ErrorAdmin(
            "Ese orden ya está ocupado. Elegí un orden libre.",
            {"orden": "El orden de estación es único, incluso entre inactivas."},
        )

    cursor.execute(
        "INSERT INTO estacion (nombre, descripcion, orden, activo) "
        "VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, orden, int(activo)),
    )
    if activo:
        _exigir_estacion_inicial(cursor)
    return cursor.lastrowid


def _actualizar_estacion(cursor, datos, fila):
    nombre, descripcion, orden, activo = _validar_estacion(datos)
    activo_anterior = bool(fila["activo"])
    orden_anterior = int(fila["orden"])

    if (
        activo != activo_anterior or orden != orden_anterior
    ) and _hay_intentos_activos(cursor):
        raise ErrorAdmin(
            "No se puede cambiar el orden ni activar/desactivar estaciones "
            "mientras hay equipos jugando."
        )

    _comprobar_nombre_estacion(cursor, nombre, fila["id"])

    if orden == orden_anterior:
        cursor.execute(
            "UPDATE estacion SET nombre = %s, descripcion = %s, activo = %s "
            "WHERE id = %s",
            (nombre, descripcion, int(activo), fila["id"]),
        )
    else:
        otra = _estacion_por_orden(cursor, orden, fila["id"])
        temporal = None
        if otra is not None:
            temporal = _orden_temporal(cursor)
            cursor.execute(
                "UPDATE estacion SET orden = %s WHERE id = %s",
                (temporal, otra["id"]),
            )

        cursor.execute(
            "UPDATE estacion SET nombre = %s, descripcion = %s, orden = %s, "
            "activo = %s WHERE id = %s",
            (nombre, descripcion, orden, int(activo), fila["id"]),
        )

        if otra is not None:
            cursor.execute(
                "UPDATE estacion SET orden = %s WHERE id = %s",
                (orden_anterior, otra["id"]),
            )

    _exigir_estacion_inicial(cursor)


def _validar_estacion(datos):
    errores = {}
    nombre = _texto(datos, "nombre", "El nombre", errores, maximo=80)
    descripcion = _texto(
        datos,
        "descripcion",
        "La descripción",
        errores,
        maximo=255,
        obligatorio=False,
    )
    orden = _entero(datos, "orden", "El orden", errores, 1, 5)
    activo = _booleano(datos, "activo")
    _lanzar_si_errores(errores)
    return nombre, descripcion, orden, activo


def _comprobar_nombre_estacion(cursor, nombre, excluir=None):
    cursor.execute(
        "SELECT id FROM estacion WHERE nombre = %s AND id <> %s",
        (nombre, excluir or 0),
    )
    if cursor.fetchone() is not None:
        raise ErrorAdmin(
            "Ya existe una estación con ese nombre.",
            {"nombre": "El nombre de la estación es único."},
        )


def _estacion_por_orden(cursor, orden, excluir=None):
    cursor.execute(
        "SELECT id, orden FROM estacion WHERE orden = %s AND id <> %s FOR UPDATE",
        (orden, excluir or 0),
    )
    return cursor.fetchone()


def _ordenes_ocupados(cursor):
    cursor.execute("SELECT COUNT(*) AS total FROM estacion")
    return int(cursor.fetchone()["total"])


def _orden_temporal(cursor):
    for candidato in (0, 250, 251, 252, 253, 254, 255):
        cursor.execute("SELECT id FROM estacion WHERE orden = %s", (candidato,))
        if cursor.fetchone() is None:
            return candidato
    raise ErrorAdmin("No se pudo reordenar la estación.")


def _exigir_estacion_inicial(cursor):
    cursor.execute(
        "SELECT COUNT(*) AS total FROM estacion WHERE activo = 1 AND orden = 1"
    )
    if int(cursor.fetchone()["total"]) == 0:
        raise ErrorAdmin(
            "Tiene que quedar al menos una estación activa con orden 1.",
            {"activo": "Sin una estación activa de orden 1 el juego no puede empezar."},
        )


# ---------------------------------------------------------------------------
# Temas
# ---------------------------------------------------------------------------


def _crear_tema(cursor, datos):
    nombre, estacion_id, activo = _validar_tema(datos)
    _comprobar_estacion_existente(cursor, estacion_id)
    _comprobar_nombre_tema(cursor, nombre, estacion_id)
    if activo:
        _comprobar_maximo_temas(cursor, estacion_id)

    cursor.execute(
        "INSERT INTO tema (nombre, estacion_id, activo) VALUES (%s, %s, %s)",
        (nombre, estacion_id, int(activo)),
    )
    return cursor.lastrowid


def _actualizar_tema(cursor, datos, fila):
    nombre, estacion_id, activo = _validar_tema(datos)
    _comprobar_estacion_existente(cursor, estacion_id)

    if estacion_id != int(fila["estacion_id"]) and _tema_en_uso(
        cursor, fila["id"]
    ):
        raise ErrorAdmin(
            "Ese tema ya se usó en un intento. No se puede mover a otra estación.",
            {"estacion_id": "El tema ya tiene preguntas seleccionadas en intentos."},
        )

    _comprobar_nombre_tema(cursor, nombre, estacion_id, fila["id"])
    if activo:
        _comprobar_maximo_temas(cursor, estacion_id, fila["id"])

    cursor.execute(
        "UPDATE tema SET nombre = %s, estacion_id = %s, activo = %s "
        "WHERE id = %s",
        (nombre, estacion_id, int(activo), fila["id"]),
    )


def _validar_tema(datos):
    errores = {}
    nombre = _texto(datos, "nombre", "El nombre", errores, maximo=80)
    estacion_id = _entero(
        datos, "estacion_id", "La estación", errores, 1, 4294967295
    )
    activo = _booleano(datos, "activo")
    _lanzar_si_errores(errores)
    return nombre, estacion_id, activo


def _comprobar_estacion_existente(cursor, estacion_id):
    cursor.execute("SELECT id FROM estacion WHERE id = %s", (estacion_id,))
    if cursor.fetchone() is None:
        raise ErrorAdmin(
            "La estación elegida no existe.",
            {"estacion_id": "Elegí una estación válida."},
        )


def _comprobar_nombre_tema(cursor, nombre, estacion_id, excluir=None):
    cursor.execute(
        "SELECT id FROM tema WHERE estacion_id = %s AND nombre = %s AND id <> %s",
        (estacion_id, nombre, excluir or 0),
    )
    if cursor.fetchone() is not None:
        raise ErrorAdmin(
            "Ya existe un tema con ese nombre en la estación.",
            {"nombre": "El nombre del tema es único dentro de la estación."},
        )


def _comprobar_maximo_temas(cursor, estacion_id, excluir=None):
    cursor.execute(
        "SELECT COUNT(*) AS total FROM tema "
        "WHERE estacion_id = %s AND activo = 1 AND id <> %s",
        (estacion_id, excluir or 0),
    )
    if int(cursor.fetchone()["total"]) >= 4:
        raise ErrorAdmin(
            "La estación ya tiene 4 temas activos.",
            {"activo": "El máximo es de 4 temas activos por estación."},
        )


def _tema_en_uso(cursor, tema_id):
    cursor.execute(
        "SELECT 1 FROM intento_pregunta ip "
        "JOIN pregunta p ON p.id = ip.pregunta_id "
        "WHERE p.tema_id = %s LIMIT 1",
        (tema_id,),
    )
    return cursor.fetchone() is not None


# ---------------------------------------------------------------------------
# Preguntas
# ---------------------------------------------------------------------------


def _crear_pregunta(cursor, datos):
    titulo, descripcion, tema_id, dificultad = _validar_pregunta(datos)
    _comprobar_tema_existente(cursor, tema_id)

    cursor.execute(
        "INSERT INTO pregunta "
        "(titulo, descripcion, tema_id, dificultad, activo) "
        "VALUES (%s, %s, %s, %s, 0)",
        (titulo, descripcion, tema_id, dificultad),
    )
    return cursor.lastrowid


def _actualizar_pregunta(cursor, datos, fila):
    titulo, descripcion, tema_id, dificultad = _validar_pregunta(datos)
    activo = _booleano(datos, "activo")
    activo_anterior = bool(fila["activo"])

    _comprobar_tema_existente(cursor, tema_id)

    if tema_id != int(fila["tema_id"]) and _pregunta_usada(cursor, fila["id"]):
        raise ErrorAdmin(
            "Esa pregunta ya se usó en un intento. No se puede mover a otro tema.",
            {"tema_id": "La pregunta ya tiene selecciones guardadas en intentos."},
        )

    if activo and not activo_anterior:
        _validar_respuestas_activas(cursor, fila["id"])

    cursor.execute(
        "UPDATE pregunta SET titulo = %s, descripcion = %s, tema_id = %s, "
        "dificultad = %s, activo = %s WHERE id = %s",
        (titulo, descripcion, tema_id, dificultad, int(activo), fila["id"]),
    )


def _validar_pregunta(datos):
    errores = {}
    titulo = _texto(datos, "titulo", "El título", errores, maximo=255)
    descripcion = _texto(
        datos,
        "descripcion",
        "La descripción",
        errores,
        maximo=2000,
        obligatorio=False,
    )
    tema_id = _entero(datos, "tema_id", "El tema", errores, 1, 4294967295)
    dificultad = str(datos.get("dificultad", "")).strip()
    if dificultad not in DIFICULTADES:
        errores["dificultad"] = "Elegí una dificultad válida."
    _lanzar_si_errores(errores)
    return titulo, descripcion, tema_id, dificultad


def _comprobar_tema_existente(cursor, tema_id):
    cursor.execute("SELECT id FROM tema WHERE id = %s", (tema_id,))
    if cursor.fetchone() is None:
        raise ErrorAdmin(
            "El tema elegido no existe.",
            {"tema_id": "Elegí un tema válido."},
        )


def _pregunta_usada(cursor, pregunta_id):
    cursor.execute(
        "SELECT 1 FROM intento_pregunta WHERE pregunta_id = %s LIMIT 1",
        (pregunta_id,),
    )
    return cursor.fetchone() is not None


# ---------------------------------------------------------------------------
# Respuestas
# ---------------------------------------------------------------------------


def _crear_respuesta(cursor, datos):
    contenido, pregunta_id, correcta, activo = _validar_respuesta(datos)
    pregunta = _comprobar_pregunta_existente(cursor, pregunta_id)

    if _pregunta_en_intento_activo(cursor, pregunta_id):
        raise ErrorAdmin(
            "La pregunta está en un intento en curso. "
            "No se pueden agregar respuestas hasta que termine."
        )

    if bool(pregunta["activo"]) and activo and correcta:
        cursor.execute(
            "UPDATE respuesta SET correcta = 0 WHERE pregunta_id = %s",
            (pregunta_id,),
        )

    cursor.execute(
        "INSERT INTO respuesta (contenido, correcta, pregunta_id, activo) "
        "VALUES (%s, %s, %s, %s)",
        (contenido, int(correcta), pregunta_id, int(activo)),
    )

    if bool(pregunta["activo"]):
        _validar_respuestas_activas(cursor, pregunta_id)
    return cursor.lastrowid


def _actualizar_respuesta(cursor, datos, fila):
    contenido, pregunta_id, correcta, activo = _validar_respuesta(datos)
    pregunta = _comprobar_pregunta_existente(cursor, pregunta_id)
    pregunta_anterior = int(fila["pregunta_id"])
    cambio_padre = pregunta_id != pregunta_anterior

    if cambio_padre and _respuesta_usada(cursor, fila["id"]):
        raise ErrorAdmin(
            "Esa respuesta ya se usó en un intento. "
            "No se puede mover a otra pregunta.",
            {"pregunta_id": "La respuesta ya tiene elecciones guardadas."},
        )

    if cambio_padre and _pregunta_en_intento_activo(cursor, pregunta_anterior):
        raise ErrorAdmin(
            "La pregunta original está en un intento en curso. "
            "No se puede mover la respuesta hasta que termine.",
            {"pregunta_id": "La pregunta original tiene un intento activo."},
        )

    if _pregunta_en_intento_activo(cursor, pregunta_id):
        cambia_correcta = correcta != bool(fila["correcta"])
        cambia_activo = activo != bool(fila["activo"])
        if cambia_correcta or cambia_activo:
            raise ErrorAdmin(
                "La pregunta está en un intento en curso. No se pueden cambiar "
                "la respuesta correcta ni el estado hasta que termine."
            )

    if bool(pregunta["activo"]) and activo and correcta:
        cursor.execute(
            "UPDATE respuesta SET correcta = 0 "
            "WHERE pregunta_id = %s AND id <> %s",
            (pregunta_id, fila["id"]),
        )

    cursor.execute(
        "UPDATE respuesta SET contenido = %s, correcta = %s, pregunta_id = %s, "
        "activo = %s WHERE id = %s",
        (contenido, int(correcta), pregunta_id, int(activo), fila["id"]),
    )

    if cambio_padre:
        cursor.execute(
            "SELECT activo FROM pregunta WHERE id = %s", (pregunta_anterior,)
        )
        anterior = cursor.fetchone()
        if anterior is not None and bool(anterior["activo"]):
            _validar_respuestas_activas(cursor, pregunta_anterior)

    if bool(pregunta["activo"]):
        _validar_respuestas_activas(cursor, pregunta_id)


def _validar_respuesta(datos):
    errores = {}
    contenido = _texto(datos, "contenido", "El contenido", errores, maximo=255)
    pregunta_id = _entero(
        datos, "pregunta_id", "La pregunta", errores, 1, 4294967295
    )
    correcta = _booleano(datos, "correcta")
    activo = _booleano(datos, "activo")
    _lanzar_si_errores(errores)
    return contenido, pregunta_id, correcta, activo


def _comprobar_pregunta_existente(cursor, pregunta_id):
    cursor.execute(
        "SELECT id, activo FROM pregunta WHERE id = %s", (pregunta_id,)
    )
    pregunta = cursor.fetchone()
    if pregunta is None:
        raise ErrorAdmin(
            "La pregunta elegida no existe.",
            {"pregunta_id": "Elegí una pregunta válida."},
        )
    return pregunta


def _pregunta_en_intento_activo(cursor, pregunta_id):
    cursor.execute(
        "SELECT 1 FROM intento_pregunta ip "
        "JOIN intento i ON i.id = ip.intento_id "
        "WHERE ip.pregunta_id = %s AND i.fecha_fin IS NULL LIMIT 1",
        (pregunta_id,),
    )
    return cursor.fetchone() is not None


def _respuesta_usada(cursor, respuesta_id):
    cursor.execute(
        "SELECT 1 FROM respuesta_elegida WHERE respuesta_id = %s "
        "UNION SELECT 1 FROM incorrecta WHERE respuesta_id = %s LIMIT 1",
        (respuesta_id, respuesta_id),
    )
    return cursor.fetchone() is not None


def _validar_respuestas_activas(cursor, pregunta_id):
    cursor.execute(
        "SELECT COUNT(*) AS total, SUM(correcta = 1) AS correctas "
        "FROM respuesta WHERE pregunta_id = %s AND activo = 1",
        (pregunta_id,),
    )
    estado = cursor.fetchone()
    total = int(estado["total"] or 0)
    correctas = int(estado["correctas"] or 0)
    if total < 2 or correctas != 1:
        raise ErrorAdmin(
            "Una pregunta activa necesita al menos 2 respuestas activas y "
            "exactamente una marcada como correcta.",
            {"activo": "Revisá las respuestas activas y la correcta."},
        )


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------


def _crear_configuracion(cursor, datos):
    clave = str(datos.get("clave", "")).strip()
    errores = {}
    if not PATRON_CLAVE.match(clave):
        errores["clave"] = (
            "Usá minúsculas, números y guiones bajos. Debe empezar con una letra."
        )
    valor = _texto(datos, "valor", "El valor", errores, maximo=255)
    _lanzar_si_errores(errores)

    cursor.execute("SELECT clave FROM configuracion WHERE clave = %s", (clave,))
    if cursor.fetchone() is not None:
        raise ErrorAdmin(
            "Ya existe una clave con ese nombre.",
            {"clave": "La clave debe ser única."},
        )

    if clave in CLAVES_JUEGO:
        regla = CLAVES_JUEGO[clave]
        if not valor.isdigit():
            raise ErrorAdmin(
                "Ese parámetro debe ser un número entero.",
                {"valor": "Ingresá un número entero."},
            )
        numero = int(valor)
        if not regla["minimo"] <= numero <= regla["maximo"]:
            raise ErrorAdmin(
                f"El valor debe estar entre {regla['minimo']} y "
                f"{regla['maximo']}.",
                {"valor": f"Rango permitido: {regla['minimo']} a {regla['maximo']}."},
            )
        if _hay_intentos_activos(cursor):
            raise ErrorAdmin(
                "No se pueden crear parámetros del juego mientras hay equipos "
                "jugando.",
                {"valor": "Esperá a que terminen los intentos activos."},
            )

    cursor.execute(
        "INSERT INTO configuracion (clave, valor) VALUES (%s, %s)",
        (clave, valor),
    )
    return clave


def _actualizar_configuracion(cursor, datos, fila):
    clave = fila["clave"]
    errores = {}
    valor = _texto(datos, "valor", "El valor", errores, maximo=255)
    _lanzar_si_errores(errores)

    cambia = valor != str(fila["valor"])

    if clave in CLAVES_SOLO_LECTURA and cambia:
        raise ErrorAdmin(
            "Ese parámetro se administra desde otra pantalla del panel.",
            {"valor": "Esta clave no se edita desde Configuración."},
        )

    if clave in CLAVES_JUEGO:
        regla = CLAVES_JUEGO[clave]
        if not valor.isdigit():
            raise ErrorAdmin(
                "Ese parámetro debe ser un número entero.",
                {"valor": "Ingresá un número entero."},
            )
        numero = int(valor)
        if not regla["minimo"] <= numero <= regla["maximo"]:
            raise ErrorAdmin(
                f"El valor debe estar entre {regla['minimo']} y "
                f"{regla['maximo']}.",
                {"valor": f"Rango permitido: {regla['minimo']} a {regla['maximo']}."},
            )
        if cambia and _hay_intentos_activos(cursor):
            raise ErrorAdmin(
                "No se pueden cambiar los parámetros del juego mientras hay "
                "equipos jugando.",
                {"valor": "Esperá a que terminen los intentos activos."},
            )

    cursor.execute(
        "UPDATE configuracion SET valor = %s WHERE clave = %s",
        (valor, clave),
    )


# ---------------------------------------------------------------------------
# Helpers generales
# ---------------------------------------------------------------------------


def _bloquear_fila(cursor, meta, clave):
    cursor.execute(
        f'SELECT * FROM {meta["tabla_sql"]} '
        f'WHERE {meta["pk_col"]} = %s FOR UPDATE',
        (clave,),
    )
    return cursor.fetchone()


def _hay_intentos_activos(cursor):
    cursor.execute(
        "SELECT COUNT(*) AS total FROM intento WHERE fecha_fin IS NULL"
    )
    return int(cursor.fetchone()["total"]) > 0


def _texto(datos, nombre, etiqueta, errores, maximo=None, obligatorio=True):
    valor = datos.get(nombre, "")
    if valor is None:
        valor = ""
    if not isinstance(valor, str):
        valor = str(valor)
    valor = valor.strip()

    if obligatorio and not valor:
        errores[nombre] = f"{etiqueta} es obligatorio."
    elif maximo is not None and len(valor) > maximo:
        errores[nombre] = f"{etiqueta} no puede superar los {maximo} caracteres."
    return valor


def _entero(datos, nombre, etiqueta, errores, minimo, maximo):
    texto = str(datos.get(nombre, "")).strip()
    if not texto:
        errores[nombre] = f"{etiqueta} es obligatorio."
        return None
    if not texto.isdigit():
        errores[nombre] = f"{etiqueta} debe ser un número entero."
        return None
    numero = int(texto)
    if not minimo <= numero <= maximo:
        errores[nombre] = f"{etiqueta} debe estar entre {minimo} y {maximo}."
        return None
    return numero


def _booleano(datos, nombre):
    valor = datos.get(nombre)
    return valor in (True, 1, "1", "true", "on")


def _lanzar_si_errores(errores):
    if errores:
        raise ErrorAdmin("Revisá los datos marcados.", errores)
