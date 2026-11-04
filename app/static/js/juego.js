document.addEventListener("submit", (evento) => {
  const formulario = evento.target;
  const mensaje = formulario.dataset.confirmar;

  if (mensaje && !window.confirm(mensaje)) {
    evento.preventDefault();
    return;
  }

  const boton = formulario.querySelector("[data-deshabilitar-al-enviar]");
  if (boton) {
    boton.disabled = true;
  }
});
