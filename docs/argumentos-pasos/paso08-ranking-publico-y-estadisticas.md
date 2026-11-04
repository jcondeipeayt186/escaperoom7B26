# Paso 08 — Ranking público y estadísticas

> **Origen:** Pedido 8 de `docs/primeros-pasos.md` (Paso 7).
> **Tipo:** código.
> **Requiere:** `paso07` cerrado.
> **Commit:** `feat: ranking público y estadísticas`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Reglas de puntaje y ranking",
> "Estadísticas públicas"), `docs/escape-room.md`,
> `docs/navegacion-por-app.md` (pantallas 4.1 y 4.2) y
> `sql/descripcion-de-la-base-de-datos.md`.

## Contexto

El MVP funciona y el ranking básico existe dentro de `/juego/final`.

## Objetivo

Dejar la vista del televisor actualizándose sola y la página pública de
estadísticas sin datos sensibles.

## Alcance

- `GET /ranking`: solo lectura, tipografía grande, tabla con posición, equipo,
  número de intento, tiempo total, incorrectas, ayudas y fecha de fin.
- `GET /ranking/datos`: JSON para el polling.
- Polling cada 5–10 segundos con `fetch`.
- Indicador de última actualización.
- Si falla el polling, mantener la tabla y mostrar "Reconectando...".
- `GET /estadisticas`: cards con equipos, integrantes, intentos iniciados,
  intentos completados, tiempo promedio de los completados, respuestas
  realizadas y porcentaje de aciertos.
- Gráfico simple de intentos por estado, con barras CSS/SVG generadas en el
  servidor.

## Reglas del ranking

- Solo `finalizado = 'completo'`.
- Orden: segundos ascendentes; luego respuestas incorrectas ascendentes;
  luego `cantidad_ayudas` ascendente; luego `fecha_inicio` ascendente; luego
  `id` ascendente.
- Mostrar el número de intento cuando un equipo repitió:
  `ROW_NUMBER() OVER (PARTITION BY equipo_id ORDER BY id)` o una subconsulta
  equivalente.
- No mostrar `equipo_id` en el JSON si no hace falta.
- No usar WebSockets: el polling alcanza.

## Reglas de las estadísticas

- Solo agregados.
- Sin nombres de equipos.
- Sin detalle por pregunta.
- Sin respuestas correctas ni opciones.
- Accesible sin login.
- Los cálculos salen de la base, no del cliente.

## Criterio de aceptación

- [ ] El ranking se actualiza solo al terminar un intento, dentro del
      intervalo de polling.
- [ ] La vista se lee a varios metros (probar con zoom o en pantalla grande).
- [ ] Un equipo que repitió muestra su número de intento.
- [ ] `/estadisticas` no muestra nombres de equipos ni respuestas correctas.
- [ ] `/ranking/datos` devuelve solo los completados y ordenados.
- [ ] Si se corta la red o el servidor, la tabla queda y aparece
      "Reconectando...".
- [ ] Todo funciona sin Internet.

## Verificación

1. Abrir `/ranking` en una ventana grande.
2. Completar un intento desde otra ventana y esperar el polling.
3. Revisar el JSON:

```bash
curl -s http://127.0.0.1:5000/ranking/datos | python -m json.tool
```

4. Buscar fugas en las estadísticas:

```bash
curl -s http://127.0.0.1:5000/estadisticas \
  | grep -iE "Los Tigres|correcta|respuesta_id"
```

Esperado: sin nombres de equipos ni referencias a la respuesta correcta.

5. En el navegador, activar "Offline" en las herramientas de desarrollo y
   confirmar que la tabla no desaparece.

## Trampas conocidas

- No ordenar por `puntaje_obtenido` ni por puntos.
- `finalizado = 'completo'` es la única condición; `fecha_fin` no nula no
  alcanza.
- El tiempo se calcula con `TIMESTAMPDIFF(SECOND, ...)`, no con el reloj del
  navegador.
- No exponer `equipo_id`, correos ni datos que no estén en la pantalla.
- El polling no debe reemplazar la tabla con un estado vacío ante un error.

## No hagas todavía

Admin, cobertura, toggles de dificultad y pruebas automatizadas completas.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado del ranking y las estadísticas.
- Commit: `feat: ranking público y estadísticas`.
