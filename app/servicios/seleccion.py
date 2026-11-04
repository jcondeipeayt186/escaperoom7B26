"""Selección aleatoria de preguntas, congelada por intento y estación."""

import random

from ..db import transaction


class ErrorSeleccion(RuntimeError):
    """La estación no se puede preparar con el contenido disponible."""


class SeleccionIncompleta(ErrorSeleccion):
    """Hay una selección parcial guardada para el intento y la estación."""


def preparar_estacion(intento_id, estacion_id, dificultad):
    """Asegura ``intento_estacion`` y las 4 preguntas de la estación.

    Todo ocurre en una transacción. Si ya existe la selección, se reutiliza
    tal cual; si no existe, se sortea una vez y se persiste.
    """

    with transaction() as cursor:
        cursor.execute(
            "SELECT id FROM intento "
            "WHERE id = %s AND fecha_fin IS NULL FOR UPDATE",
            (intento_id,),
        )
        if cursor.fetchone() is None:
            raise ErrorSeleccion("El intento ya no está activo.")

        _asegurar_intento_estacion(cursor, intento_id, estacion_id)

        seleccion = _leer_seleccion(cursor, intento_id, estacion_id)
        if seleccion:
            if len(seleccion) != 4:
                raise SeleccionIncompleta(
                    "La selección de preguntas de esta estación está incompleta. "
                    "Avisá a la organización."
                )
            return seleccion

        preguntas = _elegir_preguntas(cursor, estacion_id, dificultad)

        for orden, pregunta_id in enumerate(preguntas, start=1):
            cursor.execute(
                "INSERT INTO intento_pregunta "
                "(intento_id, estacion_id, pregunta_id, orden) "
                "VALUES (%s, %s, %s, %s)",
                (intento_id, estacion_id, pregunta_id, orden),
            )

        return _leer_seleccion(cursor, intento_id, estacion_id)


def _asegurar_intento_estacion(cursor, intento_id, estacion_id):
    """Crea la fila de la estación una sola vez, sin reiniciar la fecha."""

    cursor.execute(
        "SELECT id FROM intento_estacion "
        "WHERE intento_id = %s AND estacion_id = %s FOR UPDATE",
        (intento_id, estacion_id),
    )
    if cursor.fetchone() is not None:
        return

    cursor.execute(
        "INSERT INTO intento_estacion (intento_id, estacion_id, fecha_inicio) "
        "VALUES (%s, %s, NOW(3))",
        (intento_id, estacion_id),
    )


def _leer_seleccion(cursor, intento_id, estacion_id):
    cursor.execute(
        "SELECT pregunta_id, orden FROM intento_pregunta "
        "WHERE intento_id = %s AND estacion_id = %s "
        "ORDER BY orden FOR UPDATE",
        (intento_id, estacion_id),
    )
    return cursor.fetchall()


def _elegir_preguntas(cursor, estacion_id, dificultad):
    """Devuelve 4 ids de preguntas, en el orden en que se van a mostrar."""

    cursor.execute(
        "SELECT id, nombre FROM tema "
        "WHERE estacion_id = %s AND activo = 1 ORDER BY id",
        (estacion_id,),
    )
    temas = cursor.fetchall()
    if not temas:
        raise ErrorSeleccion("La estación no tiene temas activos.")

    cursor.execute(
        "SELECT p.id, p.tema_id "
        "FROM pregunta p "
        "JOIN tema t ON t.id = p.tema_id "
        "WHERE t.estacion_id = %s AND t.activo = 1 "
        "  AND p.activo = 1 AND p.dificultad = %s "
        "ORDER BY p.id",
        (estacion_id, dificultad),
    )
    preguntas = cursor.fetchall()
    if len(preguntas) < 4:
        raise ErrorSeleccion(
            "La estación no tiene al menos 4 preguntas de la dificultad elegida."
        )

    por_tema = {tema["id"]: [] for tema in temas}
    for pregunta in preguntas:
        por_tema[pregunta["tema_id"]].append(pregunta["id"])

    for tema in temas:
        if not por_tema[tema["id"]]:
            raise ErrorSeleccion(
                f'El tema "{tema["nombre"]}" no tiene preguntas de la '
                "dificultad elegida."
            )

    if len(temas) > 4:
        temas_elegidos = random.sample(temas, 4)
        elegidas = [
            random.choice(por_tema[tema["id"]]) for tema in temas_elegidos
        ]
    else:
        elegidas = [random.choice(por_tema[tema["id"]]) for tema in temas]
        usadas = set(elegidas)
        restantes = [
            pregunta["id"] for pregunta in preguntas if pregunta["id"] not in usadas
        ]
        faltan = 4 - len(elegidas)
        if len(restantes) < faltan:
            raise ErrorSeleccion(
                "La estación no tiene preguntas suficientes para completar las 4."
            )
        elegidas.extend(random.sample(restantes, faltan))

    if len(elegidas) != 4 or len(set(elegidas)) != 4:
        raise ErrorSeleccion("No se pudieron seleccionar 4 preguntas distintas.")

    random.shuffle(elegidas)
    return elegidas
