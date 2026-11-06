# Paso 11b — Ranking por nivel

> **Origen:** pedido posterior al `paso11`, antes del `paso12`.
> **Tipo:** feat.
> **Requiere:** `paso11` aprobado y commiteado.
> **Commit:** `feat: ranking por nivel`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Reglas de puntaje y ranking"),
> `docs/escape-room.md`, `docs/navegacion-por-app.md` y `app/servicios/ranking.py`.

## Contexto

La feria va a ofrecer los niveles `inicial` e `intermedio`. Comparar tiempos
entre niveles distintos no es justo: un equipo de `intermedio` suele tardar más
y quedaría siempre debajo de uno de `inicial`.

## Objetivo

Mantener el ranking general y agregar una posición competitiva por nivel, sin
cambiar el orden ni los criterios de desempate.

## Alcance

- `app/servicios/ranking.py`:
  - Agregar `dificultad` a la fila normalizada.
  - Calcular `posicion_nivel` con `ROW_NUMBER() OVER (PARTITION BY dificultad ...)`.
  - Conservar `posicion` como posición general.
  - Aceptar un filtro opcional por `dificultad`.
  - Agregar `obtener_ranking_por_nivel()`.
- `app/routes/ranking.py`:
  - `/ranking` renderiza una tabla por nivel.
  - `/ranking/datos` devuelve `{actualizado, niveles: [{valor, etiqueta, filas}]}`.
- `app/templates/ranking.html` y `app/static/js/ranking.js`:
  - Una sección por nivel, con su propio cuerpo de tabla.
  - El polling actualiza cada sección sin borrar las tablas si falla.
- `app/routes/juego.py` y `app/templates/final.html`:
  - Posición del intento dentro de su nivel.
  - Top 10 del nivel del intento.
  - Tabla general con columna **Nivel** y filtro por nivel.
- Tests: `tests/test_ranking.py`, `tests/test_publico.py`,
  `tests/test_reglas_juego.py`.
- Documentación: `AGENTS.md`, `docs/navegacion-por-app.md`, `README.md`,
  `MEMORY.md` y este índice.

## Fuera de alcance

- Contenido `intermedio` (se trata en el `paso11c`).
- Docker (queda para un paso posterior, opcional).
- Cambios de esquema o de las reglas de puntaje.
- `docs/escape-room.md`: solo se actualiza si el usuario lo autoriza.

## Reglas

- Solo participan intentos con `finalizado = 'completo'`.
- El orden es el mismo en la posición general y en la de nivel: tiempo,
  incorrectas, ayudas, `fecha_inicio`, `id`.
- Los filtros no cambian ninguna posición.
- La vista pública no expone `equipo_id` ni `intento_id`.
- Un nivel se muestra si está habilitado o si ya tiene intentos completados.
- `inicial` se muestra siempre.

## Criterio de aceptación

- Un equipo de `intermedio` puede ser `#1` de su nivel aunque sea más lento
  que uno de `inicial`.
- `posicion` sigue siendo la general y `posicion_nivel` la del nivel.
- La tabla general del final conserva la columna **Nivel** y el filtro por
  nivel.
- El top 10 del final es del nivel del intento.
- `/ranking` muestra una tabla por nivel y `/ranking/datos` entrega el JSON
  agrupado, sin `equipo_id` ni `intento_id`.
- Si falla el polling, se conservan todas las tablas y aparece
  **Reconectando…**.
- `pytest -q` pasa dos veces seguidas.

## Verificación

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Consultas útiles:

```sql
SELECT i.id, i.dificultad, e.nombre,
       TIMESTAMPDIFF(SECOND, i.fecha_inicio, i.fecha_fin) AS segundos
FROM intento i
JOIN equipo e ON e.id = i.equipo_id
WHERE i.finalizado = 'completo'
ORDER BY i.dificultad, segundos;
```

Revisar a mano:

- `/ranking` con equipos de ambos niveles.
- `/juego/final` de un intento `intermedio`.
- Que el JSON no incluya ids internos.

## Ojo con

- No usar `puntaje_obtenido` para ordenar.
- No comparar niveles para la posición competitiva.
- No borrar la tabla del televisor cuando falla el polling.
- No confundir `posicion` (general) con `posicion_nivel`.
