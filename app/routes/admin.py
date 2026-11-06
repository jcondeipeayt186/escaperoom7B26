"""Panel de administración: login, listados, alta, edición y baja lógica."""

import hmac
from functools import wraps

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from ..csrf import rotar_token
from ..servicios import admin_acciones as acciones
from ..servicios import admin_consultas as consultas
from ..servicios import admin_estadisticas
from ..servicios import cobertura as servicio_cobertura
from ..servicios.admin_tablas import (
    CLAVES_JUEGO,
    CLAVES_SOLO_LECTURA,
    TABLAS,
    resolver_campos,
)
from ..servicios.configuracion import (
    DIFICULTADES,
    ETIQUETAS_DIFICULTAD,
    dificultad_habilitada,
    leer_configuracion,
)
from ..servicios.tiempos import ahora_texto

bp = Blueprint("admin", __name__)


def login_requerido(vista):
    """Redirige al login si la sesión no tiene el permiso de administración."""

    @wraps(vista)
    def envoltorio(*args, **kwargs):
        if not session.get("admin_autenticado"):
            return redirect(url_for("admin.login"))
        return vista(*args, **kwargs)

    return envoltorio


@bp.get("/admin")
def login():
    """Formulario de ingreso al panel."""

    if session.get("admin_autenticado"):
        return redirect(url_for("admin.panel"))

    return render_template("admin/login.html", error=None, usuario="")


@bp.post("/admin/login")
def autenticar():
    """Valida las credenciales configuradas por variables de entorno."""

    usuario = request.form.get("usuario", "").strip()
    clave = request.form.get("clave", "")

    admin_user = current_app.config.get("ADMIN_USER")
    admin_hash = current_app.config.get("ADMIN_PASSWORD_HASH")

    valido = False
    if admin_user and admin_hash:
        usuario_ok = hmac.compare_digest(usuario, str(admin_user))
        try:
            clave_ok = check_password_hash(admin_hash, clave)
        except (TypeError, ValueError):
            clave_ok = False
        valido = usuario_ok and clave_ok

    if not valido:
        return (
            render_template(
                "admin/login.html",
                error="Usuario o clave incorrectos.",
                usuario=usuario,
            ),
            401,
        )

    session["admin_autenticado"] = True
    rotar_token()
    flash("Sesión iniciada.", "success")
    return redirect(url_for("admin.panel"))


@bp.post("/admin/logout")
@login_requerido
def logout():
    """Cierra solamente la sesión administrativa."""

    session.pop("admin_autenticado", None)
    rotar_token()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("admin.login"))


@bp.get("/admin/")
@login_requerido
def panel():
    """Panel de control con cards por tabla y estado del juego."""

    return render_template("admin/panel.html", **consultas.resumen_panel())


@bp.get("/admin/cobertura")
@login_requerido
def cobertura():
    """Reporte de cobertura de cada nivel por estación y tema."""

    datos = servicio_cobertura.obtener_cobertura()
    configuracion = leer_configuracion()
    datos["habilitadas"] = {
        dificultad: dificultad_habilitada(dificultad, configuracion)
        for dificultad in DIFICULTADES
    }
    datos["intentos_activos"] = consultas.obtener_intentos_activos()["total"]
    return render_template("admin/cobertura.html", **datos)


@bp.get("/admin/dificultades")
@login_requerido
def dificultades():
    """Formulario con los toggles de intermedio y avanzado."""

    return render_template("admin/dificultades.html", **_datos_dificultades())


@bp.post("/admin/dificultades")
@login_requerido
def guardar_dificultades():
    """Valida y persiste los toggles de dificultad."""

    deseadas = {
        "intermedio": request.form.get("intermedio") == "1",
        "avanzado": request.form.get("avanzado") == "1",
    }

    try:
        acciones.guardar_dificultades(deseadas)
    except acciones.ErrorAdmin as error:
        return (
            render_template(
                "admin/dificultades.html",
                **_datos_dificultades(error.errores, error.mensaje),
            ),
            400,
        )

    flash("Dificultades actualizadas.", "success")
    return redirect(url_for("admin.dificultades"))


@bp.get("/admin/intentos-activos")
@login_requerido
def intentos_activos():
    """Equipos jugando en este momento y motivo del bloqueo."""

    return render_template(
        "admin/intentos_activos.html", **consultas.obtener_intentos_activos()
    )


@bp.get("/admin/estadisticas")
@login_requerido
def estadisticas():
    """Métricas y gráficos del panel, con filtros por fecha y dificultad."""

    return render_template(
        "admin/estadisticas.html",
        **admin_estadisticas.obtener_estadisticas(request.args),
        actualizado=ahora_texto(),
    )


@bp.get("/admin/<tabla>")
@login_requerido
def listado(tabla):
    """Listado filtrable, ordenable y paginado de una tabla."""

    if tabla not in TABLAS:
        abort(404)
    return render_template(
        "admin/listado.html", **consultas.listar(tabla, request.args)
    )


@bp.get("/admin/<tabla>/nuevo")
@login_requerido
def nuevo(tabla):
    """Formulario de alta para las tablas editables."""

    meta = _meta_editable(tabla)
    datos = consultas.valores_iniciales(meta)
    if tabla == "pregunta":
        datos["activo"] = False

    return render_template(
        "admin/formulario.html",
        tabla=tabla,
        meta=meta,
        modo="crear",
        campos=resolver_campos(meta),
        datos=datos,
        errores={},
        error_general=None,
        clave=None,
    )


@bp.post("/admin/<tabla>/nuevo")
@login_requerido
def crear(tabla):
    """Valida y guarda una fila nueva."""

    meta = _meta_editable(tabla)
    datos = acciones.leer_formulario(meta, request.form)

    try:
        acciones.crear(tabla, datos)
    except acciones.ErrorAdmin as error:
        return (
            render_template(
                "admin/formulario.html",
                tabla=tabla,
                meta=meta,
                modo="crear",
                campos=resolver_campos(meta),
                datos=datos,
                errores=error.errores,
                error_general=error.mensaje,
                clave=None,
            ),
            400,
        )

    if tabla == "pregunta":
        flash(
            "Pregunta creada. Queda inactiva hasta que tenga al menos dos "
            "respuestas activas y una correcta.",
            "success",
        )
    elif tabla == "configuracion":
        flash("Parámetro creado.", "success")
    else:
        flash("Fila creada.", "success")
    return redirect(url_for("admin.listado", tabla=tabla))


@bp.get("/admin/<tabla>/<fila_id>")
@login_requerido
def detalle(tabla, fila_id):
    """Vista de solo lectura de cualquier fila."""

    meta = TABLAS.get(tabla)
    if meta is None:
        abort(404)

    fila = consultas.obtener_fila(tabla, fila_id)
    if fila is None:
        abort(404)

    return render_template(
        "admin/detalle.html",
        tabla=tabla,
        meta=meta,
        fila=fila,
        clave=fila_id,
        columnas=meta["columnas"],
    )


@bp.get("/admin/<tabla>/<fila_id>/editar")
@login_requerido
def editar(tabla, fila_id):
    """Formulario de edición para las tablas editables."""

    meta = _meta_editable(tabla)
    fila = consultas.obtener_fila(tabla, fila_id)
    if fila is None:
        abort(404)

    return render_template(
        "admin/formulario.html",
        tabla=tabla,
        meta=meta,
        modo="editar",
        campos=_campos_para_formulario(tabla, meta, fila),
        datos=consultas.valores_formulario(meta, fila),
        errores={},
        error_general=None,
        clave=fila_id,
    )


@bp.post("/admin/<tabla>/<fila_id>/editar")
@login_requerido
def actualizar(tabla, fila_id):
    """Valida y guarda los cambios de una fila."""

    meta = _meta_editable(tabla)
    fila = consultas.obtener_fila(tabla, fila_id)
    if fila is None:
        abort(404)

    datos = acciones.leer_formulario(meta, request.form)

    try:
        acciones.actualizar(tabla, fila_id, datos)
    except ValueError:
        abort(404)
    except acciones.ErrorAdmin as error:
        return (
            render_template(
                "admin/formulario.html",
                tabla=tabla,
                meta=meta,
                modo="editar",
                campos=_campos_para_formulario(tabla, meta, fila),
                datos=datos,
                errores=error.errores,
                error_general=error.mensaje,
                clave=fila_id,
            ),
            400,
        )

    flash("Cambios guardados.", "success")
    return redirect(url_for("admin.listado", tabla=tabla))


@bp.post("/admin/<tabla>/<fila_id>/desactivar")
@login_requerido
def desactivar(tabla, fila_id):
    """Aplica una baja lógica desde el listado."""

    meta = TABLAS.get(tabla)
    if meta is None or not meta["campos"] or not meta["tiene_activo"]:
        abort(404)

    try:
        acciones.desactivar(tabla, fila_id)
    except ValueError:
        abort(404)
    except acciones.ErrorAdmin as error:
        flash(error.mensaje, "danger")
    else:
        flash("Fila desactivada.", "success")

    return redirect(url_for("admin.listado", tabla=tabla))


def _datos_dificultades(errores=None, error_general=None):
    """Arma el estado de cobertura y toggles para la plantilla."""

    configuracion = leer_configuracion()
    datos_cobertura = servicio_cobertura.obtener_cobertura()
    activos = consultas.obtener_intentos_activos()

    dificultades = []
    for dificultad in ("intermedio", "avanzado"):
        nivel = servicio_cobertura.obtener_nivel(datos_cobertura, dificultad)
        dificultades.append(
            {
                "valor": dificultad,
                "etiqueta": ETIQUETAS_DIFICULTAD[dificultad],
                "habilitada": dificultad_habilitada(dificultad, configuracion),
                "cobertura_completa": bool(nivel and nivel["completa"]),
                "estaciones_completas": (
                    nivel["estaciones_completas"] if nivel else 0
                ),
                "total_estaciones": nivel["total_estaciones"] if nivel else 0,
                "temas_sin_preguntas": (
                    nivel["temas_sin_preguntas"] if nivel else 0
                ),
            }
        )

    return {
        "cobertura": datos_cobertura,
        "dificultades": dificultades,
        "intentos_activos": activos["total"],
        "errores": errores or {},
        "error_general": error_general,
    }


def _meta_editable(tabla):
    meta = TABLAS.get(tabla)
    if meta is None or not meta["campos"]:
        abort(404)
    return meta


def _campos_para_formulario(tabla, meta, fila):
    """Carga opciones y marca campos que no se pueden modificar."""

    campos = resolver_campos(meta)
    if tabla != "configuracion":
        return campos

    clave = fila["clave"]
    for campo in campos:
        if campo["nombre"] == "clave":
            campo["solo_lectura"] = True
            campo["ayuda"] = "La clave no se puede modificar."
        elif clave in CLAVES_SOLO_LECTURA:
            campo["solo_lectura"] = True
            campo["ayuda"] = (
                "Se administra desde otra pantalla del panel."
            )
        elif clave in CLAVES_JUEGO and consultas.hay_intentos_activos():
            campo["solo_lectura"] = True
            campo["ayuda"] = (
                "No se puede cambiar mientras hay equipos jugando."
            )
    return campos
