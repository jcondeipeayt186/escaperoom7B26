"""Rutas del juego: bienvenida, identidad y estaciones."""

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from ..servicios import configuracion as config
from ..servicios import envios, equipos
from ..servicios.estaciones import (
    contar_estaciones_activas,
    obtener_estacion,
    obtener_preguntas_seleccionadas,
    obtener_resumen_estacion,
)
from ..servicios.seleccion import ErrorSeleccion, preparar_estacion
from ..servicios.tiempos import calcular_tiempos

bp = Blueprint("juego", __name__)

MOTIVOS_ELIMINACION = {
    "abandono": "El equipo abandonó el juego.",
    "por_respuestas_incorrectas": (
        "Llegaron al máximo de respuestas incorrectas permitidas."
    ),
    "por_tiempo": "Se terminó el tiempo de la estación.",
}


@bp.get("/")
def bienvenida():
    """Muestra el formulario de ingreso."""

    contexto = equipos.contexto_de_sesion()
    if contexto is None:
        equipos.limpiar_sesion_juego()

    parametros = config.leer_configuracion()
    dificultades = config.dificultades_habilitadas(parametros)

    return render_template(
        "bienvenida.html",
        dificultades=dificultades,
        max_integrantes=config.maximo_integrantes(parametros),
        valores={
            "nombre": "",
            "cantidad_personas": "",
            "dificultad": dificultades[0]["valor"] if dificultades else "",
        },
        errores={},
        intento_activo=contexto,
    )


@bp.post("/")
def registrar_equipo():
    """Valida el formulario y crea el equipo o deriva a identificación."""

    parametros = config.leer_configuracion()
    dificultades = config.dificultades_habilitadas(parametros)
    max_integrantes = config.maximo_integrantes(parametros)

    valores = {
        "nombre": equipos.normalizar_nombre(request.form.get("nombre", "")),
        "cantidad_personas": request.form.get("cantidad_personas", "").strip(),
        "dificultad": request.form.get("dificultad", "").strip(),
    }
    errores, cantidad_personas = _validar_bienvenida(
        valores, max_integrantes, parametros
    )

    if errores:
        return (
            render_template(
                "bienvenida.html",
                dificultades=dificultades,
                max_integrantes=max_integrantes,
                valores=valores,
                errores=errores,
                intento_activo=equipos.contexto_de_sesion(),
            ),
            400,
        )

    equipo_existente = equipos.buscar_equipo_por_nombre(valores["nombre"])
    if equipo_existente is not None:
        equipos.guardar_identificacion(
            valores["nombre"], cantidad_personas, valores["dificultad"]
        )
        flash(
            "Ese nombre de equipo ya existe. Ingresá el ID para continuar.",
            "info",
        )
        return redirect(url_for("juego.identificar"))

    try:
        equipo_id, intento_id = equipos.crear_equipo_y_intento(
            valores["nombre"], cantidad_personas, valores["dificultad"]
        )
    except equipos.NombreDuplicado:
        # Otra pestaña creó el mismo nombre entre la búsqueda y el alta.
        equipos.guardar_identificacion(
            valores["nombre"], cantidad_personas, valores["dificultad"]
        )
        flash(
            "Ese nombre de equipo ya existe. Ingresá el ID para continuar.",
            "info",
        )
        return redirect(url_for("juego.identificar"))

    equipos.guardar_sesion(equipo_id, intento_id)
    flash("¡Equipo registrado! Comienza la misión.", "success")
    return redirect(url_for("juego.juego"))


@bp.get("/equipo/identificar")
def identificar():
    """Pide el ID cuando el nombre del equipo ya está registrado."""

    datos = equipos.identificacion_pendiente()
    if datos is None:
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return redirect(url_for("juego.bienvenida"))

    return render_template("identificar.html", identificacion=datos, error=None)


@bp.post("/equipo/identificar")
def confirmar_identificacion():
    """Comprueba el ID contra el nombre y reanuda o crea el intento."""

    datos = equipos.identificacion_pendiente()
    if datos is None:
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return redirect(url_for("juego.bienvenida"))

    equipo_id_texto = request.form.get("equipo_id", "").strip()
    if not equipo_id_texto.isdigit():
        return (
            render_template(
                "identificar.html",
                identificacion=datos,
                error="El ID no es válido. Revisá el número que te mostramos.",
            ),
            400,
        )

    equipo = equipos.equipo_por_id_y_nombre(int(equipo_id_texto), datos["nombre"])
    if equipo is None:
        return (
            render_template(
                "identificar.html",
                identificacion=datos,
                error="No pudimos identificar ese equipo con el ID indicado. "
                "Revisá el número y volvé a intentar.",
            ),
            400,
        )

    parametros = config.leer_configuracion()
    if not config.es_dificultad_valida(datos["dificultad"], parametros):
        equipos.limpiar_identificacion()
        flash(
            "La dificultad elegida ya no está habilitada. Elegí otra para continuar.",
            "warning",
        )
        return redirect(url_for("juego.bienvenida"))

    resultado = equipos.obtener_o_crear_intento(equipo["id"], datos["dificultad"])
    if resultado is None:
        return (
            render_template(
                "identificar.html",
                identificacion=datos,
                error="No pudimos identificar ese equipo con el ID indicado. "
                "Revisá el número y volvé a intentar.",
            ),
            400,
        )

    intento_id, reanudado = resultado
    equipos.guardar_sesion(equipo["id"], intento_id)

    if reanudado:
        flash("Retomamos el intento que tenías en curso.", "success")
    else:
        flash("¡Bienvenido de nuevo! Empieza un intento nuevo.", "success")

    return redirect(url_for("juego.juego"))


@bp.get("/juego")
def juego():
    """Redirige a la estación actual del intento."""

    contexto = equipos.contexto_de_sesion()
    if contexto is None:
        if equipos.contexto_finalizado_de_sesion() is not None:
            return redirect(url_for("juego.eliminado"))
        equipos.limpiar_sesion_juego()
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return redirect(url_for("juego.bienvenida"))

    estacion = obtener_estacion(contexto["intento"]["ultima_estacion_visitada"])
    if estacion is None or not estacion["activo"]:
        return _estacion_no_disponible(
            "No pudimos encontrar la estación actual del intento. "
            "Avisá a la organización.",
            estacion,
        )

    return redirect(url_for("juego.estacion", orden=estacion["orden"]))


@bp.get("/juego/estado")
def estado():
    """Devuelve los contadores para resincronizar sin recargar la página.

    Normalmente es de solo lectura. Si el tiempo de la estación ya se agotó,
    cierra el intento como ``por_tiempo`` y devuelve la redirección.
    """

    contexto = equipos.contexto_de_sesion()
    if contexto is None:
        if equipos.contexto_finalizado_de_sesion() is not None:
            destino = url_for("juego.eliminado")
        else:
            equipos.limpiar_sesion_juego()
            destino = url_for("juego.bienvenida")
        return jsonify({"redirigir": destino})

    actual = obtener_estacion(contexto["intento"]["ultima_estacion_visitada"])
    if actual is None or not actual["activo"]:
        return (
            jsonify(
                {"error": "La estación actual del intento no está disponible."}
            ),
            404,
        )

    datos, respuesta = _resolver_estacion(
        actual["orden"], cerrar_por_tiempo=False
    )
    if respuesta is not None:
        if isinstance(respuesta, tuple):
            return jsonify({"error": "La estación no está disponible."}), 503
        return jsonify({"redirigir": respuesta.location})

    if datos["tiempo_agotado"]:
        envios.cerrar_por_tiempo_agotado(
            datos["contexto"]["intento"]["id"],
            datos["estacion"]["id"],
            datos["tiempos"]["duracion_estacion_segundos"],
        )
        return jsonify(
            {
                "estado": "por_tiempo",
                "redirigir": url_for("juego.eliminado"),
            }
        )

    return jsonify(datos["tiempos"])


@bp.get("/juego/estacion/<int:orden>")
def estacion(orden):
    """Muestra la estación actual con sus 4 preguntas congeladas."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if datos["resumen"]["completada"]:
        return redirect(url_for("juego.transicion", orden=datos["estacion"]["orden"]))

    preguntas, respuesta = _preguntas_para_jugar(datos)
    if respuesta is not None:
        return respuesta

    return render_template(
        "estacion.html",
        equipo=datos["contexto"]["equipo"],
        intento=datos["contexto"]["intento"],
        estacion=datos["estacion"],
        total_estaciones=datos["total_estaciones"],
        preguntas=preguntas,
        resumen=datos["resumen"],
        maximos=datos["maximos"],
        tiempos=datos["tiempos"],
        modo_solo_finalizar=(
            datos["resumen"]["envios"] >= datos["maximos"]["envios"]
        ),
    )


@bp.post("/juego/estacion/<int:orden>/responder")
def responder(orden):
    """Registra un envío y aplica las reglas de la estación."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if datos["resumen"]["completada"]:
        return redirect(url_for("juego.transicion", orden=datos["estacion"]["orden"]))

    preguntas, respuesta = _preguntas_para_jugar(datos)
    if respuesta is not None:
        return respuesta

    respuestas, error = _leer_respuestas(request.form, preguntas)
    if error is not None:
        flash(error, "danger")
        return redirect(url_for("juego.estacion", orden=orden))

    try:
        resultado = envios.registrar_envio(
            datos["contexto"]["intento"]["id"],
            datos["estacion"]["id"],
            respuestas,
            datos["maximos"]["incorrectas"],
            datos["maximos"]["envios"],
        )
    except envios.ErrorPartida as error:
        flash(str(error), "warning")
        return redirect(url_for("juego.estacion", orden=orden))

    if resultado["estado"] == "completada":
        flash("¡Las 4 respuestas son correctas! Estación superada.", "success")
        return redirect(url_for("juego.transicion", orden=orden))

    if resultado["estado"] == "eliminado":
        flash(
            "El equipo quedó eliminado por acumular respuestas incorrectas.",
            "danger",
        )
        return redirect(url_for("juego.eliminado"))

    if resultado["estado"] == "solo_finalizar":
        flash(
            f"Acertaste {resultado['correctas']} de 4. "
            "Ya no quedan envíos: solo podés finalizar el juego.",
            "warning",
        )
        return redirect(url_for("juego.estacion", orden=orden))

    flash(
        f"Acertaste {resultado['correctas']} de 4. "
        f"Incorrectas acumuladas: {resultado['total_incorrectas']} "
        f"de {datos['maximos']['incorrectas']}.",
        "info",
    )
    return redirect(url_for("juego.estacion", orden=orden))


@bp.post("/juego/estacion/<int:orden>/ayuda")
def ayuda(orden):
    """Registra una ayuda sin mostrar el texto de la pista."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if datos["resumen"]["completada"]:
        return redirect(url_for("juego.transicion", orden=datos["estacion"]["orden"]))

    if datos["resumen"]["envios"] >= datos["maximos"]["envios"]:
        flash("Ya no quedan envíos: solo podés finalizar el juego.", "warning")
        return redirect(url_for("juego.estacion", orden=orden))

    try:
        resultado = envios.registrar_ayuda(
            datos["contexto"]["intento"]["id"],
            datos["estacion"]["id"],
            datos["maximos"]["ayudas"],
            datos["maximos"]["envios"],
        )
    except envios.ErrorPartida as error:
        flash(str(error), "warning")
        return redirect(url_for("juego.estacion", orden=orden))

    if resultado["registrada"]:
        flash(
            f"Ayuda registrada ({resultado['ayudas']} de "
            f"{datos['maximos']['ayudas']}).",
            "success",
        )
    else:
        flash("Ya usaron todas las ayudas de esta estación.", "info")
    return redirect(url_for("juego.estacion", orden=orden))


@bp.post("/juego/estacion/<int:orden>/abandonar")
def abandonar(orden):
    """Cierra el intento como abandono."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if datos["resumen"]["completada"]:
        return redirect(url_for("juego.transicion", orden=datos["estacion"]["orden"]))

    try:
        envios.abandonar(
            datos["contexto"]["intento"]["id"], datos["estacion"]["id"]
        )
    except envios.ErrorPartida as error:
        flash(str(error), "warning")
        return redirect(url_for("juego.estacion", orden=orden))

    flash("El equipo abandonó el juego.", "info")
    return redirect(url_for("juego.eliminado"))


@bp.post("/juego/estacion/<int:orden>/finalizar")
def finalizar(orden):
    """Finaliza el intento cuando ya no quedan envíos disponibles."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if datos["resumen"]["completada"]:
        return redirect(url_for("juego.transicion", orden=datos["estacion"]["orden"]))

    try:
        envios.finalizar_por_incorrectas(
            datos["contexto"]["intento"]["id"],
            datos["estacion"]["id"],
            datos["maximos"]["envios"],
        )
    except envios.ErrorPartida as error:
        flash(str(error), "warning")
        return redirect(url_for("juego.estacion", orden=orden))

    flash("El intento finalizó por respuestas incorrectas.", "danger")
    return redirect(url_for("juego.eliminado"))


@bp.get("/juego/transicion/<int:orden>")
def transicion(orden):
    """Muestra la confirmación mínima de una estación superada."""

    datos, respuesta = _resolver_estacion(orden)
    if respuesta is not None:
        return respuesta

    if not datos["resumen"]["completada"]:
        return redirect(url_for("juego.estacion", orden=orden))

    return render_template(
        "transicion.html",
        equipo=datos["contexto"]["equipo"],
        intento=datos["contexto"]["intento"],
        estacion=datos["estacion"],
        total_estaciones=datos["total_estaciones"],
        resumen=datos["resumen"],
        maximos=datos["maximos"],
        tiempos=datos["tiempos"],
    )


@bp.get("/juego/eliminado")
def eliminado():
    """Explica por qué el equipo quedó fuera del juego."""

    if equipos.contexto_de_sesion() is not None:
        return redirect(url_for("juego.juego"))

    finalizado = equipos.contexto_finalizado_de_sesion()
    if finalizado is None:
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return redirect(url_for("juego.bienvenida"))

    if finalizado["intento"]["finalizado"] == "completo":
        return redirect(url_for("juego.bienvenida"))

    estacion = obtener_estacion(
        finalizado["intento"]["ultima_estacion_visitada"]
    )
    motivo = MOTIVOS_ELIMINACION.get(
        finalizado["intento"]["finalizado"],
        "El intento no se pudo completar.",
    )

    return render_template(
        "eliminado.html",
        equipo=finalizado["equipo"],
        intento=finalizado["intento"],
        estacion=estacion,
        total_estaciones=contar_estaciones_activas(),
        motivo=motivo,
    )


def _resolver_estacion(orden, cerrar_por_tiempo=True):
    """Valida sesión, orden y estado; devuelve datos o una respuesta."""

    contexto = equipos.contexto_de_sesion()
    if contexto is None:
        if equipos.contexto_finalizado_de_sesion() is not None:
            return None, redirect(url_for("juego.eliminado"))
        equipos.limpiar_sesion_juego()
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return None, redirect(url_for("juego.bienvenida"))

    actual = obtener_estacion(contexto["intento"]["ultima_estacion_visitada"])
    if actual is None or not actual["activo"]:
        return None, _estacion_no_disponible(
            "No pudimos encontrar la estación actual del intento. "
            "Avisá a la organización.",
            actual,
        )

    total_estaciones = contar_estaciones_activas()
    if not 1 <= orden <= total_estaciones:
        abort(404)

    if orden != actual["orden"]:
        return None, redirect(url_for("juego.estacion", orden=actual["orden"]))

    try:
        preparar_estacion(
            contexto["intento"]["id"],
            actual["id"],
            contexto["intento"]["dificultad"],
        )
    except ErrorSeleccion as error:
        return None, _estacion_no_disponible(str(error), actual)

    parametros = config.leer_configuracion()
    intento_id = contexto["intento"]["id"]
    resumen = obtener_resumen_estacion(intento_id, actual["id"])
    duracion = config.duracion_estacion(parametros)
    tiempos = calcular_tiempos(intento_id, actual["id"], duracion)
    tiempo_agotado = (
        not resumen["completada"] and tiempos["estacion_segundos"] <= 0
    )

    if tiempo_agotado and cerrar_por_tiempo:
        if envios.cerrar_por_tiempo_agotado(intento_id, actual["id"], duracion):
            flash("Se terminó el tiempo de la estación.", "danger")
        return None, redirect(url_for("juego.eliminado"))

    return (
        {
            "contexto": contexto,
            "estacion": actual,
            "total_estaciones": total_estaciones,
            "resumen": resumen,
            "maximos": config.maximos_estacion(parametros),
            "tiempos": tiempos,
            "tiempo_agotado": tiempo_agotado,
        },
        None,
    )


def _preguntas_para_jugar(datos):
    preguntas = obtener_preguntas_seleccionadas(
        datos["contexto"]["intento"]["id"], datos["estacion"]["id"]
    )
    if len(preguntas) != 4 or any(not pregunta["opciones"] for pregunta in preguntas):
        return None, _estacion_no_disponible(
            "La estación no tiene las preguntas y opciones completas para jugar. "
            "Avisá a la organización.",
            datos["estacion"],
        )
    return preguntas, None


def _leer_respuestas(formulario, preguntas):
    """Convierte el formulario en ``{pregunta_id: respuesta_id}``."""

    respuestas = {}
    permitidos = set()

    for pregunta in preguntas:
        clave = f"pregunta_{pregunta['id']}"
        permitidos.add(clave)
        valores = formulario.getlist(clave)
        if len(valores) != 1:
            return None, "Respondé las 4 preguntas antes de comprobar."
        valor = valores[0].strip()
        if not valor.isdigit():
            return None, "Una de las respuestas no es válida. Volvé a intentarlo."
        respuestas[pregunta["id"]] = int(valor)

    for clave in formulario.keys():
        if clave.startswith("pregunta_") and clave not in permitidos:
            return None, "El formulario tiene preguntas que no corresponden."

    return respuestas, None


def _estacion_no_disponible(mensaje, estacion=None):
    """Muestra un error de configuración sin cortar con una excepción."""

    return (
        render_template(
            "estacion_no_disponible.html",
            mensaje=mensaje,
            estacion=estacion,
            total_estaciones=contar_estaciones_activas(),
        ),
        503,
    )


def _validar_bienvenida(valores, max_integrantes, parametros):
    """Devuelve errores por campo y la cantidad ya convertida a entero."""

    errores = {}
    nombre = valores["nombre"]

    if not nombre:
        errores["nombre"] = "Ingresá el nombre del equipo."
    elif len(nombre) > equipos.LARGO_MAXIMO_NOMBRE:
        errores["nombre"] = (
            f"El nombre no puede superar los {equipos.LARGO_MAXIMO_NOMBRE} caracteres."
        )

    cantidad_personas = None
    cantidad_texto = valores["cantidad_personas"]
    if not cantidad_texto.isdigit():
        errores["cantidad_personas"] = "Elegí la cantidad de integrantes."
    else:
        cantidad_personas = int(cantidad_texto)
        if not 1 <= cantidad_personas <= max_integrantes:
            errores["cantidad_personas"] = (
                f"La cantidad de integrantes debe estar entre 1 y {max_integrantes}."
            )

    if not config.es_dificultad_valida(valores["dificultad"], parametros):
        errores["dificultad"] = "Elegí una dificultad habilitada."

    return errores, cantidad_personas
