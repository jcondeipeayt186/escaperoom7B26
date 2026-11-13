# Paso 05 — Temporizadores y reanudación

> **Origen:** Pedido 5 de `docs/primeros-pasos.md` (Paso 5).
> **Tipo:** código.
> **Requiere:** `paso04` aprobado y commiteado.
> **Commit:** `feat: temporizadores y reanudación`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Temporizadores" y "Decisiones
> registradas"), `docs/escape-room.md`, `docs/navegacion-por-app.md` (HUD y
> pantalla 3.3) y `sql/descripcion-de-la-base-de-datos.md` (`intento`,
> `intento_estacion`, `configuracion`).

## Contexto

La estación 1 se juega, se registran envíos, ayudas y eliminaciones. Falta
que el tiempo sea del servidor y sobreviva recargas.

## Objetivo

Que los dos contadores se calculen desde fechas de MySQL, no se reinicien al
recargar y que el tiempo agotado elimine al equipo.

## Alcance

- Helper de tiempo en el servidor: tiempo general transcurrido y segundos
  restantes de la estación.
- Enviar a la plantilla los segundos y la hora del servidor.
- `static/js/temporizadores.js`: cuenta local entre sincronizaciones.
- `GET /juego/estado` (JSON, solo lectura) para resincronizar cada 10
  segundos. Es una ruta nueva respecto del mapa de
  `docs/navegacion-por-app.md`: anotarla en `MEMORY.md`.
- Contador general ascendente. En este paso se implementó en `HH:MM:SS`; un
  ajuste posterior al `paso11f` lo unificó a `MM:SS`, igual que el contador de
  estación.
- Contador de estación descendente en formato `MM:SS`.
- A los 30 segundos restantes: texto titilante y audio local.
- Al llegar a 0: finalizar como `por_tiempo` y redirigir a eliminación.
- Reanudar desde `intento.ultima_estacion_visitada`.
- Desbloquear el audio con la primera interacción del usuario.

## Reglas

- La fuente de verdad es el servidor. `Date.now()` solo dibuja la cuenta
  entre sincronizaciones.
- Validar el tiempo agotado en **cada** request de juego, aunque el cliente
  no haya redirigido.
- `intento.fecha_inicio` e `intento_estacion.fecha_inicio` se escriben una
  sola vez. Recargar no las resetea.
- Al agotarse el tiempo: `finalizado = 'por_tiempo'`, `fecha_fin` del
  servidor y `puntaje_obtenido` en `NULL`.
- El aviso de 30 segundos es siempre visual; el audio es un refuerzo.
- Audio local en `static/audio/`. Si no hay archivo, generar un WAV corto con
  la biblioteca estándar de Python; no depender de Internet.
- Si el equipo tenía un intento activo, `/juego` retoma la estación que
  corresponde según `ultima_estacion_visitada`.

## Criterio de aceptación

- [ ] Recargar no reinicia ni el contador general ni el de la estación.
- [ ] El contador general sigue subiendo después de recargar.
- [ ] A los 30 segundos aparece el texto titilante y suena el audio tras la
      primera interacción.
- [ ] Al llegar a 0 el intento queda `por_tiempo` y no se puede seguir.
- [ ] Un POST después del tiempo agotado se rechaza aunque el reloj del
      navegador esté manipulado.
- [ ] Reabrir la app retoma la estación correcta.
- [ ] Con el audio bloqueado, el aviso visual igual funciona.

## Verificación

1. Bajar `duracion_estacion_segundos` a `20` en `configuracion` para probar
   rápido. Restaurar a `240` al terminar.
2. Entrar a la estación, esperar, recargar y comparar los contadores.
3. Esperar los últimos 30 segundos y confirmar texto y audio.
4. Esperar el cero y verificar en MySQL:

```sql
SELECT id, finalizado, fecha_fin, puntaje_obtenido
FROM intento WHERE id = <id>;

SELECT TIMESTAMPDIFF(SECOND, fecha_inicio, NOW()) AS general,
       TIMESTAMPDIFF(SECOND, ie.fecha_inicio, NOW()) AS estacion
FROM intento i
JOIN intento_estacion ie ON ie.intento_id = i.id
WHERE i.id = <id> AND ie.estacion_id = <id>;
```

5. Cerrar el navegador, volver a abrir y confirmar que retoma la estación.

## Trampas conocidas

- `ultima_estacion_visitada` guarda `estacion.id`, no `orden`.
- Una pestaña en segundo plano frena los `setInterval`. Resincronizar al
  volver a la pestaña (`visibilitychange`) y cada 10 segundos.
- No calcular el tiempo con la hora del cliente como fuente de verdad.
- No reiniciar `intento_estacion.fecha_inicio` al reanudar: reutilizar la
  fila existente.
- El audio puede estar bloqueado por el navegador hasta el primer clic.
  Desbloquearlo en "Iniciar" y no depender de que suene.

## No hagas todavía

Estaciones 2 a 5, ranking público, estadísticas y admin.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado de los temporizadores y la ruta nueva
  `/juego/estado`.
- Commit: `feat: temporizadores y reanudación`.
