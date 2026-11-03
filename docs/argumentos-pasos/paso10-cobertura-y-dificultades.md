# Paso 10 — Cobertura, dificultades y gráficos

> **Origen:** Pedido 10 de `docs/primeros-pasos.md` (Paso 8, segunda parte).
> **Tipo:** código.
> **Requiere:** `paso09` aprobado y commiteado.
> **Commit:** `feat: cobertura y control de dificultades`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Selección de preguntas por
> estación", "Administración" y "Decisiones registradas"), `docs/escape-room.md`,
> `docs/navegacion-por-app.md` (5.5 a 5.8) y
> `sql/descripcion-de-la-base-de-datos.md` (`configuracion`).

## Contexto

El admin tiene login, panel y CRUD. Las dificultades siguen deshabilitadas en
`configuracion` y no hay reporte de cobertura.

## Objetivo

Controlar qué niveles se pueden habilitar y ver las métricas del juego, sin
permitir estados inválidos.

## Alcance

- `GET /admin/cobertura`: tabla estación × nivel con temas activos, preguntas
  por tema, total y estado verde/rojo.
- `GET /admin/dificultades` y `POST /admin/dificultades`: toggles de
  `intermedio` y `avanzado`.
- `GET /admin/intentos-activos`: equipos jugando y motivo del bloqueo.
- `GET /admin/estadisticas`: gráficos de equipos, intentos finalizados,
  tiempo promedio por estación, tiempo promedio de completados, porcentaje de
  utilización de cada pregunta y porcentaje de aciertos.
- Función única de cobertura reutilizada por el reporte y por el toggle.

## Reglas de cobertura

Un nivel se puede habilitar solo si, para **todas** las estaciones activas:

- cada tema activo tiene al menos 1 pregunta activa de ese nivel, y
- la estación tiene al menos `preguntas_por_estacion` (4) preguntas activas
  de ese nivel.

`inicial` siempre está habilitada y no se toca.

## Reglas de los toggles

- No habilitar un nivel sin cobertura completa.
- No deshabilitar un nivel si hay intentos activos (`fecha_fin IS NULL`).
- Persistir en `configuracion`.
- Validar en el servidor aunque el cliente mande el POST directamente.
- La bienvenida debe reflejar el cambio: solo ofrece las dificultades
  habilitadas.
- `inicial` no se puede deshabilitar.

## Reglas de los gráficos

- Recomendado: barras CSS/SVG generadas en el servidor. Cero dependencias y
  funciona sin Internet.
- Si se usa Chart.js, va local en `static/vendor/`, nunca por CDN.
- Los datos se calculan en el servidor.
- Filtros por fecha y dificultad: opcionales; si se agregan, parametrizados.

## Criterio de aceptación

- [ ] Con el contenido actual, `intermedio` y `avanzado` no se pueden
      habilitar.
- [ ] El reporte marca en rojo los temas sin preguntas del nivel y las
      estaciones con menos de 4.
- [ ] Con un intento activo, los toggles quedan bloqueados.
- [ ] Al terminar todos los intentos, los toggles vuelven a habilitarse.
- [ ] Un POST manual para habilitar sin cobertura se rechaza.
- [ ] La bienvenida solo muestra las dificultades habilitadas.
- [ ] Los gráficos cargan sin Internet.
- [ ] `inicial` aparece siempre habilitada.

## Verificación

Cobertura por tema y nivel:

```sql
SELECT e.orden, e.nombre AS estacion, t.id AS tema_id, t.nombre AS tema,
       COUNT(p.id) AS preguntas_nivel
FROM estacion e
JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.dificultad = 'intermedio' AND p.activo = 1
WHERE e.activo = 1
GROUP BY e.id, e.orden, e.nombre, t.id, t.nombre
ORDER BY e.orden, t.nombre;
```

Esperado: todos los temas en 0 para `intermedio` y `avanzado`.

Intentos activos:

```sql
SELECT COUNT(*) AS activos FROM intento WHERE fecha_fin IS NULL;
```

Con `activos > 0`, el toggle debe estar bloqueado.

Configuración:

```sql
SELECT clave, valor FROM configuracion WHERE clave LIKE 'dificultad%';
```

Probar el POST directo con `curl` o desde las herramientas del navegador y
confirmar que el servidor rechaza el cambio.

## Trampas conocidas

- La cobertura se calcula por tema **y** por estación, no solo por estación.
- El bloqueo usa `fecha_fin IS NULL`, no `finalizado`.
- `configuracion.valor` es texto: convertir a entero donde corresponda.
- No alcanza con deshabilitar el botón en el HTML; validar en el servidor.
- No habilitar un nivel "solo para probar" en la base de la feria.
- Si se agrega Chart.js, verificar que no queden referencias a CDN.

## No hagas todavía

Pruebas automatizadas completas, backup y puesta en marcha.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado de cobertura y dificultades.
- Commit: `feat: cobertura y control de dificultades`.
