(function () {
  "use strict";

  const contenedor = document.getElementById("ranking");
  if (!contenedor) return;

  const hora = document.getElementById("ranking-hora");
  const reconectando = document.getElementById("ranking-reconectando");
  const vacio = document.getElementById("ranking-vacio");
  const url = contenedor.dataset.url;
  const intervalo = Number(contenedor.dataset.intervalo) || 8000;

  // Una entrada por sección de nivel renderizada por el servidor.
  const secciones = new Map();
  document.querySelectorAll("section[data-nivel]").forEach(function (seccion) {
    secciones.set(seccion.getAttribute("data-nivel"), {
      seccion: seccion,
      cuerpo: seccion.querySelector("tbody"),
      vacio: seccion.querySelector("[data-vacio]"),
      tabla: seccion.querySelector("[data-tabla]"),
    });
  });

  let consultando = false;

  function dosDigitos(numero) {
    return String(numero).padStart(2, "0");
  }

  function formatoTiempo(total) {
    const segundos = Math.max(0, Number(total) || 0);
    return (
      dosDigitos(Math.floor(segundos / 3600)) +
      ":" +
      dosDigitos(Math.floor((segundos % 3600) / 60)) +
      ":" +
      dosDigitos(segundos % 60)
    );
  }

  function celda(texto) {
    const td = document.createElement("td");
    td.textContent = texto;
    return td;
  }

  function crearFila(fila) {
    const tr = document.createElement("tr");
    tr.appendChild(celda("#" + fila.posicion));
    tr.appendChild(celda(fila.equipo));
    tr.appendChild(celda(fila.numero_intento));
    tr.appendChild(celda(formatoTiempo(fila.segundos)));
    tr.appendChild(celda(fila.incorrectas));
    tr.appendChild(celda(fila.ayudas));
    tr.appendChild(celda(fila.fecha_fin));
    return tr;
  }

  function pintarNivel(nivel) {
    const seccion = secciones.get(nivel.valor);
    if (!seccion) return false;

    const filas = Array.isArray(nivel.filas) ? nivel.filas : [];

    // textContent en cada celda: el nombre del equipo nunca se interpreta
    // como HTML.
    if (seccion.cuerpo) {
      seccion.cuerpo.replaceChildren(...filas.map(crearFila));
    }
    if (seccion.vacio) seccion.vacio.hidden = filas.length > 0;
    if (seccion.tabla) seccion.tabla.hidden = filas.length === 0;
    seccion.seccion.hidden = false;

    return filas.length > 0;
  }

  function pintar(datos) {
    if (!Array.isArray(datos.niveles)) return;

    let hayFilas = false;
    const vistos = new Set();

    datos.niveles.forEach(function (nivel) {
      vistos.add(nivel.valor);
      if (pintarNivel(nivel)) hayFilas = true;
    });

    // Si un nivel se deshabilita y deja de venir, se oculta su sección.
    secciones.forEach(function (seccion, valor) {
      if (!vistos.has(valor)) seccion.seccion.hidden = true;
    });

    vacio.hidden = hayFilas;
    if (datos.actualizado) hora.textContent = datos.actualizado;
    reconectando.hidden = true;
    contenedor.classList.remove("ranking--sin-conexion");
  }

  async function actualizar() {
    if (consultando || !url) return;
    consultando = true;

    try {
      const respuesta = await fetch(url, {
        cache: "no-store",
        headers: { Accept: "application/json" },
      });
      if (!respuesta.ok) {
        throw new Error("Respuesta " + respuesta.status);
      }

      pintar(await respuesta.json());
    } catch (error) {
      // Se conservan las últimas tablas y solo se avisa que no hay conexión.
      reconectando.hidden = false;
      contenedor.classList.add("ranking--sin-conexion");
    } finally {
      consultando = false;
    }
  }

  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) actualizar();
  });

  window.setInterval(function () {
    if (!document.hidden) actualizar();
  }, intervalo);

  actualizar();
})();
