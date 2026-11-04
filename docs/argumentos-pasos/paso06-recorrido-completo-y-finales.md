# Paso 06 — Recorrido completo y finales (MVP)

> **Origen:** Pedido 6 de `docs/primeros-pasos.md` (Paso 6).
> **Tipo:** código.
> **Requiere:** `paso05` aprobado y commiteado.
> **Commit:** `feat: recorrido completo y pantallas de finalización`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Flujo de pantallas", "Reglas de
> puntaje y ranking" y "Temporizadores"), `docs/escape-room.md`,
> `docs/navegacion-por-app.md` (pantallas 3.4 a 3.6 y sección 6) y
> `sql/descripcion-de-la-base-de-datos.md`.

## Contexto

La estación 1 funciona con envío, ayudas, eliminaciones y temporizadores.

## Objetivo

Cerrar el recorrido de las 5 estaciones, las transiciones, las tres formas de
eliminación, la pantalla final y el ranking básico.

## Alcance

- Generalizar las rutas de estación para `orden` 1 a 5.
- `GET /juego/transicion/<orden>`.
- Transición con resumen de la estación y botón **Continuar** (o **Ver
  resultado** en la quinta).
- `POST /juego/transicion/<orden>/continuar` para preparar la estación
  siguiente.
- `POST /juego/transicion/<orden>/abandonar` con confirmación en las
  estaciones 1 a 4.
- `GET /juego/final`.
- `GET /juego/eliminado` completa, con el motivo.
- `templates/transicion.html`, `templates/final.html` y
  `templates/eliminado.html` definitivos.
- Pantalla final con resultado, posición, top 10 y ranking completo
  filtrable por equipo, número de intento y fecha de fin.
- Cálculo de `puntaje_obtenido` y del ranking básico.
- Actualización de `ultima_estacion_visitada` al presionar **Continuar**.
- Bloqueo de avance fuera de orden.

No implementar todavía el ranking público con polling, las estadísticas ni el
admin.

## Reglas del recorrido

- Solo se puede jugar la estación que indica `ultima_estacion_visitada`.
- Al completar una estación, se actualiza `intento_estacion.completada = 1`
  y `fecha_fin`. `ultima_estacion_visitada` sigue apuntando a esa estación
  para que la transición sea accesible.
- Al presionar **Continuar**, la estación siguiente se prepara y recién ahí
  `ultima_estacion_visitada` pasa a la estación siguiente (por `id`, no por
  `orden`). La operación es idempotente.
- El cronómetro de la estación siguiente arranca cuando se entra a ella
  después de la transición, no al completar la anterior.
- No se puede volver a una estación completada ni saltar hacia adelante por
  URL.
- La transición solo se muestra si la estación está completada.

## Reglas del final

- Al completar la quinta estación se finaliza el intento:
  `finalizado = 'completo'`, `fecha_fin` del servidor y
  `puntaje_obtenido = TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin)`.
- El tiempo total se congela al completar la quinta estación; la transición
  y la pantalla final no suman tiempo.
- `/juego/final` solo se muestra si `finalizado = 'completo'`; con un intento
  activo redirige a la estación actual y con uno no completado redirige a
  eliminación.
- La pantalla final muestra el tiempo total, la posición, un top 10 y el
  ranking completo con filtros por nombre de equipo, número de intento y
  fecha de fin. Las filas incluyen la fecha y hora de fin.
- Los filtros se resuelven en el servidor con parámetros GET y no cambian la
  posición general de cada fila.
- Un intento finalizado no se reanuda. El próximo ingreso crea uno nuevo.

## Reglas de eliminación

- `por_tiempo`: se agotó el tiempo de la estación.
- `por_respuestas_incorrectas`: en una estación se acumularon 2 incorrectas o se agotaron los
  envíos.
- `abandono`: el equipo confirmó el abandono, ya sea desde la estación o
  desde la transición de las estaciones 1 a 4.
- En los tres casos: `fecha_fin` del servidor y `puntaje_obtenido = NULL`.
- La pantalla explica el motivo, muestra la estación alcanzada, el tiempo
  total, las ayudas, las incorrectas y las estaciones completadas.

## Reglas del ranking

Solo intentos completos, ordenados por:

1. menor tiempo total (`TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin)`);
2. menor cantidad de incorrectas;
3. menor cantidad de ayudas;
4. `fecha_inicio` ascendente (el intento que comenzó antes);
5. `id` ascendente como desempate estable.

El ranking se muestra recortado a las primeras 10 posiciones y, en una card
aparte, completo y filtrable. El número de intento se cuenta sobre todos los
intentos del equipo, incluidos los no completados. No ordenar por
`puntaje_obtenido` ni por puntos.

## Criterio de aceptación

- [ ]  Un equipo completa las 5 estaciones y ve su resultado.
- [ ]  Un equipo tiene una incorrecta en cada estación, es decir, en cada primer envio de respuestas va una incorrecta, luego las responde bien pasando correctamente en el segundo envio. Recibe 2 ayudas. Completa las 5 estaciones y ve su resultado con sus incorrectas.
- [ ]  Un equipo es eliminado por tiempo, por incorrectas y por abandono.
- [ ]  El ranking ordena por tiempo, luego incorrectas, luego ayudas, luego el intento que comenzó antes.
- [ ]  Un intento no completado no aparece en el ranking.
- [ ]  No se puede saltar de la estación 2 a la 5 por URL.
- [ ]  El tiempo total de un intento completo coincide con la diferencia
  entre `fecha_inicio` y `fecha_fin`.
- [ ]  `puntaje_obtenido` queda `NULL` en los intentos no completados.
- [ ]  Los filtros del ranking completo no alteran la posición general.
- [ ]  La fecha de fin se muestra como `dd/mm/aaaa HH:MM`.

## Verificación

Jugar las 5 estaciones. Después:

```sql
SELECT id, equipo_id, dificultad, fecha_inicio, fecha_fin, finalizado,
       puntaje_obtenido, cantidad_ayudas, ultima_estacion_visitada
FROM intento WHERE id = <id>;

SELECT e.orden, e.nombre, ie.fecha_inicio, ie.fecha_fin,
       ie.ayudas, ie.completada
FROM intento_estacion ie
JOIN estacion e ON e.id = ie.estacion_id
WHERE ie.intento_id = <id>
ORDER BY e.orden;
```

Esperado: 5 filas en `intento_estacion`, todas completadas, y `puntaje_obtenido`
igual a los segundos totales.

Ranking:

```sql
SELECT i.id, e.nombre,
       TIMESTAMPDIFF(SECOND, i.fecha_inicio, i.fecha_fin) AS segundos,
       (SELECT COUNT(*) FROM incorrecta inc WHERE inc.intento_id = i.id)
         AS incorrectas,
       i.cantidad_ayudas, i.fecha_inicio
FROM intento i
JOIN equipo e ON e.id = i.equipo_id
WHERE i.finalizado = 'completo'
ORDER BY segundos ASC,
         incorrectas ASC,
         i.cantidad_ayudas ASC,
         i.fecha_inicio ASC,
         i.id ASC;
```

## Trampas conocidas

- No usar `estacion.id` como si fuera `estacion.orden`.
- No contar el tiempo de la transición ni de la pantalla final.
- No finalizar el intento al completar una estación intermedia.
- No finalizar el intento por tener 2 o más incorrectas mientras cada una sea de una estación distinta.
- No permitir reanudar un intento finalizado.
- No mostrar el ranking con intentos abandonados o eliminados.
- Cuidado con el doble POST al continuar una transición: la creación de la
  estación siguiente debe ser idempotente.

## Este es el corte del MVP

Antes de seguir con el `paso08`, hacer el `paso07`: probar el juego con dos o
tres personas. No arrancar el admin sin ese corte.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado del MVP.
- Commit: `feat: recorrido completo y pantallas de finalización`.
