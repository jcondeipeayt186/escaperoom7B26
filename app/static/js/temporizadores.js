(function () {
  "use strict";

  const hud = document.querySelector("[data-tiempos]");
  if (!hud) return;

  const generalEl = document.getElementById("tiempo-general");
  const estacionEl = document.getElementById("tiempo-estacion");
  const avisoEl = document.getElementById("aviso-30");
  const audio = document.getElementById("audio-aviso");
  const estadoUrl = hud.dataset.estadoUrl;

  const avisoSegundos = Number(hud.dataset.avisoSegundos) || 30;
  let servidorMs = Number(hud.dataset.servidorMs) || Date.now();
  let intentoInicioMs = Number(hud.dataset.intentoInicioMs) || servidorMs;
  let estacionFinMs = Number(hud.dataset.estacionFinMs) || servidorMs;
  let estacionFija = Number(hud.dataset.estacionSegundos) || 0;
  let completada = hud.dataset.completada === "si";
  let baseRendimiento = performance.now();

  let avisoDisparado = false;
  let audioDesbloqueado = false;
  let bloqueado = false;
  let sincronizando = false;

  function ahoraServidorMs() {
    return servidorMs + (performance.now() - baseRendimiento);
  }

  function generalSegundos() {
    return Math.max(0, Math.floor((ahoraServidorMs() - intentoInicioMs) / 1000));
  }

  function restantesSegundos() {
    if (completada) return estacionFija;
    return Math.max(0, Math.ceil((estacionFinMs - ahoraServidorMs()) / 1000));
  }

  function dosDigitos(numero) {
    return String(numero).padStart(2, "0");
  }

  function formatoGeneral(total) {
    return (
      dosDigitos(Math.floor(total / 3600)) +
      ":" +
      dosDigitos(Math.floor((total % 3600) / 60)) +
      ":" +
      dosDigitos(total % 60)
    );
  }

  function formatoEstacion(total) {
    return dosDigitos(Math.floor(total / 60)) + ":" + dosDigitos(total % 60);
  }

  function mostrarAviso() {
    if (!avisoEl) return;

    avisoEl.hidden = false;
    avisoEl.classList.add("aviso-30--visible");

    if (avisoDisparado) return;
    avisoDisparado = true;
    reproducirAudio();
  }

  function reproducirAudio() {
    if (!audio) return;

    audio.currentTime = 0;
    const intento = audio.play();
    if (intento && typeof intento.catch === "function") {
      intento.catch(function () {});
    }
  }

  function desbloquearAudio() {
    if (!audio || audioDesbloqueado) return;
    audioDesbloqueado = true;

    if (avisoDisparado) {
      reproducirAudio();
      return;
    }

    const intento = audio.play();
    if (intento && typeof intento.then === "function") {
      intento
        .then(function () {
          audio.pause();
          audio.currentTime = 0;
        })
        .catch(function () {});
    }
  }

  function bloquearJuego() {
    bloqueado = true;
    document
      .querySelectorAll("main button, main input")
      .forEach(function (elemento) {
        elemento.disabled = true;
      });
  }

  function actualizar() {
    if (generalEl) {
      generalEl.textContent = formatoGeneral(generalSegundos());
    }

    const restantes = restantesSegundos();
    if (estacionEl) {
      estacionEl.textContent = formatoEstacion(restantes);
    }

    if (!completada && restantes > 0 && restantes <= avisoSegundos) {
      mostrarAviso();
    }

    if (!completada && restantes <= 0 && !bloqueado) {
      bloquearJuego();
      sincronizar();
    }
  }

  async function sincronizar() {
    if (sincronizando || !estadoUrl) return;
    sincronizando = true;
    let reintentar = false;

    try {
      const respuesta = await fetch(estadoUrl, {
        cache: "no-store",
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      if (!respuesta.ok) return;

      const datos = await respuesta.json();
      if (datos.redirigir) {
        window.location.assign(datos.redirigir);
        return;
      }

      servidorMs = Number(datos.servidor_ms) || servidorMs;
      intentoInicioMs = Number(datos.intento_inicio_ms) || intentoInicioMs;
      estacionFinMs = Number(datos.estacion_fin_ms) || estacionFinMs;
      estacionFija = Number(datos.estacion_segundos) || 0;
      completada = Boolean(datos.completada);
      baseRendimiento = performance.now();

      actualizar();
      reintentar = bloqueado && !completada;
    } catch (error) {
      // Sin conexión: seguimos dibujando con los últimos valores conocidos.
    } finally {
      sincronizando = false;
    }

    if (reintentar) {
      window.setTimeout(sincronizar, 500);
    }
  }

  document.addEventListener("pointerdown", desbloquearAudio, { once: true });
  document.addEventListener("keydown", desbloquearAudio, { once: true });

  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) sincronizar();
  });

  window.setInterval(actualizar, 250);
  window.setInterval(sincronizar, 10000);

  actualizar();
})();
