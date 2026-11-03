# Paso 04 — Envío, HUD y reglas de la estación

> **Origen:** Pedido 4 de `docs/primeros-pasos.md` (Paso 4, segunda parte).
> **Tipo:** código.
> **Requiere:** `paso03` aprobado y commiteado.
> **Commit:** `feat: envío de respuestas y reglas de la estación`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Decisiones registradas", puntos 1 y
> 15), `docs/escape-room.md`, `docs/navegacion-por-app.md` (pantalla 3.3) y
> `sql/descripcion-de-la-base-de-datos.md` (`intento_envio`,
> `respuesta_elegida`, `incorrecta`, `intento_estacion`).

## Contexto

La estación 1 muestra las 4 preguntas congeladas, pero el formulario no hace
nada.

## Objetivo

Procesar el envío, registrar todo lo que eligió el equipo, aplicar las
reglas de la estación y permitir ayudas y abandono.

## Alcance

- `POST /juego/estacion/<orden>/responder`.
- `POST /juego/estacion/<orden>/ayuda`.
- `POST /juego/estacion/<orden>/abandonar`.
- `POST /juego/estacion/<orden>/finalizar` para el estado "solo queda
  finalizar". Es una ruta nueva respecto del mapa de
  `docs/navegacion-por-app.md`: anotarla en `MEMORY.md`.
- `templates/transicion.html` y `templates/eliminado.html` mínimos. Se
  completan en el `paso06`.
- Zona de mensajes en `estacion.html`: aciertos del envío, incorrectas
  acumuladas, aviso de último envío.
- HUD actualizado desde el servidor: ayudas, incorrectas y envíos.

## Reglas del envío

1. Validar que haya exactamente una opción marcada por cada una de las 4
   preguntas del intento.
2. Validar que cada `respuesta_id` pertenezca a la pregunta correspondiente
   del `intento_pregunta` y esté activa.
3. En una transacción: crear `intento_envio` con la fecha del servidor y los
   conteos; insertar las 4 filas de `respuesta_elegida`; insertar en
   `incorrecta` solo las incorrectas.
4. Después de registrar, evaluar en este orden:
   1. Si las 4 están correctas: marcar `intento_estacion.completada = 1`,
      `fecha_fin` del servidor y redirigir a la transición.
   2. Si las incorrectas acumuladas en la estación llegan a
      `max_respuestas_incorrectas`: finalizar como
      `por_respuestas_incorrectas` y redirigir a eliminación.
   3. Si ya se hicieron `max_envios_estacion` envíos y el último no está todo
      correcto: dejar la estación en modo "solo finalizar", sin formulario ni
      ayudas. El botón **Finalizar juego** cierra como
      `por_respuestas_incorrectas`.
   4. En cualquier otro caso: quedan envíos disponibles y se vuelve a mostrar
      el formulario.
5. Un envío incompleto no crea `intento_envio` ni filas de respuestas.

## Reglas de ayudas y abandono

- Ayudas: máximo `max_ayudas_estacion` (2) por estación e intento. Cada
  ayuda incrementa `intento_estacion.ayudas` e `intento.cantidad_ayudas` en
  una transacción. Al llegar a 2, los botones se deshabilitan.
- La app no muestra el texto de las pistas. Solo registra la ayuda.
- Abandono: pide confirmación en el navegador y finaliza como `abandono`,
  con `fecha_fin` del servidor.
- Toda acción sobre un intento finalizado redirige a eliminación o final; no
  se puede seguir jugando.

## Criterio de aceptación

- [ ] Un envío con todo correcto pasa a la transición y deja la estación
      completada.
- [ ] Un envío con 2 incorrectas elimina al equipo.
- [ ] Dos envíos con 1 incorrecta cada uno eliminan al equipo.
- [ ] Al segundo envío sin todo correcto, solo queda **Finalizar juego**.
- [ ] Las ayudas llegan como máximo a 2 y quedan deshabilitadas.
- [ ] Abandonar pide confirmación y cierra el intento como `abandono`.
- [ ] Todas las respuestas elegidas quedan en `respuesta_elegida`; solo las
      incorrectas quedan además en `incorrecta`.
- [ ] Un envío incompleto se rechaza sin crear `intento_envio`.
- [ ] No se puede enviar dos veces el mismo formulario por doble clic.

## Verificación

Jugar tres veces la estación: todo correcto, 1 incorrecta y 2 incorrectas.
Después:

```sql
SELECT id, fecha, respuestas_correctas, respuestas_incorrectas
FROM intento_envio
WHERE intento_id = <id> AND estacion_id = <id>
ORDER BY id;

SELECT COUNT(*) AS elegidas
FROM respuesta_elegida
WHERE intento_envio_id = <id>;

SELECT COUNT(*) AS incorrectas
FROM incorrecta
WHERE intento_envio_id = <id>;

SELECT ayudas, completada, fecha_inicio, fecha_fin
FROM intento_estacion
WHERE intento_id = <id> AND estacion_id = <id>;

SELECT finalizado, fecha_fin, cantidad_ayudas, puntaje_obtenido
FROM intento WHERE id = <id>;
```

Esperado: 4 filas en `respuesta_elegida` por envío, `incorrecta` solo con las
falladas y los estados del intento coherentes.

Para probar el estado "solo finalizar" sin pelearte con la aritmética del
juego, subir temporalmente `max_respuestas_incorrectas` a `3` en
`configuracion`, hacer dos envíos con 1 incorrecta cada uno y después
restaurar el valor a `2`.

## Trampas conocidas

- El doble clic puede crear dos envíos. Usar POST + redirección (PRG),
  deshabilitar el botón al enviar y volver a validar el estado en el
  servidor.
- No confiar en que las 4 respuestas correspondan a las 4 preguntas: validar
  cada una contra `intento_pregunta`.
- No borrar ni volver a sortear `intento_pregunta` al recargar.
- Las incorrectas se acumulan dentro de la estación, no en todo el intento.
- No marcar la estación como completada antes de confirmar que las 4 son
  correctas.
- No usar GET para acciones que cambian estado.

## No hagas todavía

Temporizadores, estaciones 2 a 5, ranking público, estadísticas y admin.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado de la estación 1 y la ruta nueva
  `/juego/estacion/<orden>/finalizar`.
- Commit: `feat: envío de respuestas y reglas de la estación`.
