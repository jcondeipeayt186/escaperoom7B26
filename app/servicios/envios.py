"""Envíos, ayudas, abandono y cierre de una estación."""

from ..db import transaction


class ErrorPartida(RuntimeError):
    """La acción no es válida para el estado actual de la partida."""


class EnvioIncompleto(ErrorPartida):
    """El formulario no trae una respuesta válida por cada pregunta."""


def registrar_envio(
    intento_id, estacion_id, respuestas, max_incorrectas, max_envios
):
    """Registra un envío completo y aplica las reglas de la estación.

    ``respuestas`` asocia cada ``pregunta_id`` con el ``respuesta_id`` elegido.
    Devuelve un diccionario con el estado resultante: ``completada``,
    ``eliminado``, ``solo_finalizar`` o ``continua``.
    """

    with transaction() as cursor:
        _bloquear_intento(cursor, intento_id)
        estacion = _bloquear_estacion(cursor, intento_id, estacion_id)
        if estacion["completada"]:
            raise ErrorPartida("La estación ya está completada.")

        envios = _contar_envios(cursor, intento_id, estacion_id)
        if envios >= max_envios:
            raise ErrorPartida(
                "Ya no quedan envíos disponibles en esta estación."
            )

        preguntas = _preguntas_congeladas(cursor, intento_id, estacion_id)
        elecciones = _validar_respuestas(cursor, preguntas, respuestas)
        correctas = sum(1 for eleccion in elecciones if eleccion["correcta"])
        incorrectas = len(elecciones) - correctas

        cursor.execute(
            "INSERT INTO intento_envio "
            "(intento_id, estacion_id, fecha, respuestas_correctas, "
            " respuestas_incorrectas) "
            "VALUES (%s, %s, NOW(3), %s, %s)",
            (intento_id, estacion_id, correctas, incorrectas),
        )
        envio_id = cursor.lastrowid

        for eleccion in elecciones:
            cursor.execute(
                "INSERT INTO respuesta_elegida "
                "(fecha_respondida, intento_id, intento_envio_id, respuesta_id) "
                "VALUES (NOW(3), %s, %s, %s)",
                (intento_id, envio_id, eleccion["respuesta_id"]),
            )
            if not eleccion["correcta"]:
                cursor.execute(
                    "INSERT INTO incorrecta "
                    "(pregunta_id, respuesta_id, fecha, intento_id, "
                    " intento_envio_id) "
                    "VALUES (%s, %s, NOW(3), %s, %s)",
                    (
                        eleccion["pregunta_id"],
                        eleccion["respuesta_id"],
                        intento_id,
                        envio_id,
                    ),
                )

        total_incorrectas = _contar_incorrectas(cursor, intento_id, estacion_id)
        total_envios = envios + 1
        resultado = {
            "correctas": correctas,
            "incorrectas": incorrectas,
            "total_incorrectas": total_incorrectas,
            "envios": total_envios,
        }

        if correctas == len(preguntas):
            cursor.execute("SELECT NOW(3) AS ahora")
            ahora = cursor.fetchone()["ahora"]
            cursor.execute(
                "UPDATE intento_estacion "
                "SET completada = 1, fecha_fin = %s "
                "WHERE intento_id = %s AND estacion_id = %s",
                (ahora, intento_id, estacion_id),
            )
            if not _hay_estacion_posterior(cursor, estacion_id):
                _cerrar_intento_completo(cursor, intento_id, ahora)
            resultado["estado"] = "completada"
            return resultado

        if total_incorrectas >= max_incorrectas:
            _cerrar_intento(cursor, intento_id, "por_respuestas_incorrectas")
            _cerrar_estacion(cursor, intento_id, estacion_id)
            resultado["estado"] = "eliminado"
            return resultado

        if total_envios >= max_envios:
            resultado["estado"] = "solo_finalizar"
            return resultado

        resultado["estado"] = "continua"
        return resultado


def registrar_ayuda(intento_id, estacion_id, max_ayudas, max_envios):
    """Suma una ayuda si quedan disponibles."""

    with transaction() as cursor:
        _bloquear_intento(cursor, intento_id)
        estacion = _bloquear_estacion(cursor, intento_id, estacion_id)
        if estacion["completada"]:
            raise ErrorPartida("La estación ya está completada.")

        if _contar_envios(cursor, intento_id, estacion_id) >= max_envios:
            raise ErrorPartida(
                "Ya no quedan envíos: solo podés finalizar el juego."
            )

        if estacion["ayudas"] >= max_ayudas:
            return {"registrada": False, "ayudas": int(estacion["ayudas"])}

        cursor.execute(
            "UPDATE intento_estacion SET ayudas = ayudas + 1 "
            "WHERE intento_id = %s AND estacion_id = %s",
            (intento_id, estacion_id),
        )
        cursor.execute(
            "UPDATE intento SET cantidad_ayudas = cantidad_ayudas + 1 "
            "WHERE id = %s",
            (intento_id,),
        )
        return {"registrada": True, "ayudas": int(estacion["ayudas"]) + 1}


def abandonar(intento_id, estacion_id):
    """Cierra el intento como abandono y cierra la estación actual."""

    with transaction() as cursor:
        _bloquear_intento(cursor, intento_id)
        _bloquear_estacion(cursor, intento_id, estacion_id)
        _cerrar_intento(cursor, intento_id, "abandono")
        _cerrar_estacion(cursor, intento_id, estacion_id)


def finalizar_por_incorrectas(intento_id, estacion_id, max_envios):
    """Cierra el intento cuando ya no quedan envíos disponibles."""

    with transaction() as cursor:
        _bloquear_intento(cursor, intento_id)
        estacion = _bloquear_estacion(cursor, intento_id, estacion_id)
        if estacion["completada"]:
            raise ErrorPartida("La estación ya está completada.")

        if _contar_envios(cursor, intento_id, estacion_id) < max_envios:
            raise ErrorPartida(
                "Todavía quedan envíos disponibles en esta estación."
            )

        _cerrar_intento(cursor, intento_id, "por_respuestas_incorrectas")
        _cerrar_estacion(cursor, intento_id, estacion_id)


def cerrar_por_tiempo_agotado(intento_id, estacion_id, duracion_segundos):
    """Cierra el intento como ``por_tiempo`` si la estación se agotó.

    Vuelve a comprobar el tiempo con el reloj de MySQL dentro de la
    transacción. Es idempotente: si el intento ya no está activo, la estación
    está completada o todavía queda tiempo, no modifica nada y devuelve
    ``False``.
    """

    with transaction() as cursor:
        cursor.execute(
            "SELECT id FROM intento "
            "WHERE id = %s AND fecha_fin IS NULL FOR UPDATE",
            (intento_id,),
        )
        if cursor.fetchone() is None:
            return False

        cursor.execute(
            "SELECT TIMESTAMPDIFF(SECOND, fecha_inicio, NOW(3)) AS transcurridos, "
            "       completada "
            "FROM intento_estacion "
            "WHERE intento_id = %s AND estacion_id = %s FOR UPDATE",
            (intento_id, estacion_id),
        )
        estacion = cursor.fetchone()
        if (
            estacion is None
            or estacion["completada"]
            or int(estacion["transcurridos"]) < duracion_segundos
        ):
            return False

        _cerrar_intento(cursor, intento_id, "por_tiempo")
        _cerrar_estacion(cursor, intento_id, estacion_id)
        return True


def _bloquear_intento(cursor, intento_id):
    cursor.execute(
        "SELECT id FROM intento "
        "WHERE id = %s AND fecha_fin IS NULL FOR UPDATE",
        (intento_id,),
    )
    if cursor.fetchone() is None:
        raise ErrorPartida("El intento ya no está activo.")


def _bloquear_estacion(cursor, intento_id, estacion_id):
    cursor.execute(
        "SELECT id, ayudas, completada FROM intento_estacion "
        "WHERE intento_id = %s AND estacion_id = %s FOR UPDATE",
        (intento_id, estacion_id),
    )
    estacion = cursor.fetchone()
    if estacion is None:
        raise ErrorPartida("La estación todavía no está preparada.")
    return estacion


def _preguntas_congeladas(cursor, intento_id, estacion_id):
    cursor.execute(
        "SELECT pregunta_id FROM intento_pregunta "
        "WHERE intento_id = %s AND estacion_id = %s ORDER BY orden",
        (intento_id, estacion_id),
    )
    preguntas = cursor.fetchall()
    if len(preguntas) != 4:
        raise ErrorPartida(
            "La estación no tiene sus 4 preguntas preparadas. "
            "Avisá a la organización."
        )
    return [fila["pregunta_id"] for fila in preguntas]


def _validar_respuestas(cursor, preguntas, respuestas):
    """Comprueba que cada respuesta exista y pertenezca a su pregunta."""

    if set(respuestas) != set(preguntas):
        raise EnvioIncompleto(
            "Respondé las 4 preguntas antes de comprobar."
        )

    ids = list(respuestas.values())
    placeholders = ", ".join(["%s"] * len(ids))
    cursor.execute(
        f"SELECT id, pregunta_id, correcta FROM respuesta "
        f"WHERE id IN ({placeholders})",
        tuple(ids),
    )
    filas = {fila["id"]: fila for fila in cursor.fetchall()}

    elecciones = []
    for pregunta_id in preguntas:
        respuesta_id = respuestas[pregunta_id]
        fila = filas.get(respuesta_id)
        if fila is None or fila["pregunta_id"] != pregunta_id:
            raise EnvioIncompleto(
                "Una de las respuestas no corresponde a su pregunta. "
                "Volvé a intentarlo."
            )

        elecciones.append(
            {
                "pregunta_id": pregunta_id,
                "respuesta_id": respuesta_id,
                "correcta": bool(fila["correcta"]),
            }
        )

    return elecciones


def _contar_envios(cursor, intento_id, estacion_id):
    cursor.execute(
        "SELECT COUNT(*) AS total FROM intento_envio "
        "WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )
    return int(cursor.fetchone()["total"])


def _contar_incorrectas(cursor, intento_id, estacion_id):
    cursor.execute(
        "SELECT COUNT(*) AS total FROM incorrecta i "
        "JOIN intento_envio e ON e.id = i.intento_envio_id "
        "WHERE i.intento_id = %s AND e.estacion_id = %s",
        (intento_id, estacion_id),
    )
    return int(cursor.fetchone()["total"])


def _cerrar_intento(cursor, intento_id, finalizado):
    cursor.execute(
        "UPDATE intento "
        "SET finalizado = %s, fecha_fin = NOW(3), puntaje_obtenido = NULL "
        "WHERE id = %s AND fecha_fin IS NULL",
        (finalizado, intento_id),
    )


def _cerrar_intento_completo(cursor, intento_id, fecha_fin):
    """Cierra el intento al completar la última estación.

    ``fecha_fin`` es la misma que se guardó en ``intento_estacion`` para que
    el puntaje no incluya el tiempo de la transición ni de la pantalla final.
    """

    cursor.execute(
        "UPDATE intento "
        "SET finalizado = 'completo', fecha_fin = %s, "
        "    puntaje_obtenido = TIMESTAMPDIFF(SECOND, fecha_inicio, %s) "
        "WHERE id = %s AND fecha_fin IS NULL",
        (fecha_fin, fecha_fin, intento_id),
    )


def _hay_estacion_posterior(cursor, estacion_id):
    """Indica si después de esta estación sigue el recorrido activo."""

    cursor.execute(
        "SELECT 1 FROM estacion e "
        "JOIN estacion actual ON actual.id = %s "
        "WHERE e.activo = 1 AND e.orden > actual.orden LIMIT 1",
        (estacion_id,),
    )
    return cursor.fetchone() is not None


def _cerrar_estacion(cursor, intento_id, estacion_id):
    cursor.execute(
        "UPDATE intento_estacion "
        "SET fecha_fin = COALESCE(fecha_fin, NOW(3)) "
        "WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )
