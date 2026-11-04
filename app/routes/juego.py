"""Rutas del juego: bienvenida, identidad y tablero provisorio."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..servicios import configuracion as config
from ..servicios import equipos
from ..servicios.estaciones import contar_estaciones_activas, obtener_estacion

bp = Blueprint("juego", __name__)


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
    """Tablero provisorio: equipo, intento y estación a jugar."""

    contexto = equipos.contexto_de_sesion()
    if contexto is None:
        equipos.limpiar_sesion_juego()
        flash("Ingresá el nombre de tu equipo para comenzar.", "info")
        return redirect(url_for("juego.bienvenida"))

    estacion = obtener_estacion(contexto["intento"]["ultima_estacion_visitada"])

    return render_template(
        "juego.html",
        equipo=contexto["equipo"],
        intento=contexto["intento"],
        estacion=estacion,
        total_estaciones=contar_estaciones_activas(),
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
