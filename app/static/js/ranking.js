(function () {
  "use strict";

  const contenedor = document.getElementById("ranking");
  if (!contenedor) return;

  const cuerpo = document.getElementById("ranking-filas");
  const hora = document.getElementById("ranking-hora");
  const reconectando = document.getElementById("ranking-reconectando");
  const vacio = document.getElementById("ranking-vacio");
  const url = contenedor.dataset.url;
  const intervalo = Number(contenedor.dataset.intervalo) || 8000;

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

  function pintar(datos) {
    if (!Array.isArray(datos.filas)) return;

    // textContent en cada celda: el nombre del equipo nunca se interpreta
    // como HTML.
    cuerpo.replaceChildren.apply(cuerpo, datos.filas.map(crearFila));
    vacio.hidden = datos.filas.length > 0;
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
      // Se conserva la última tabla y solo se avisa que no hay conexión.
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
