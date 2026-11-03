# Paso 00 — Verificar base y contenido

> **Origen:** Paso 1 de `docs/primeros-pasos.md`.
> **Tipo:** infra (verificación, sin código de app).
> **Requiere:** MySQL 8 instalado y el repositorio clonado.
> **Commit:** no lleva commit. Si encontrás un error en `bd/schema.sql` o en
> el seed, pará y consultá antes de tocarlo.
>
> **Antes de empezar:** leé `AGENTS.md`, `docs/escape-room.md`,
> `sql/descripcion-de-la-base-de-datos.md` y `MEMORY.md`.

## Contexto

El esquema (`bd/schema.sql`) y el contenido inicial
(`bd/seeds/001_contenido_inicial.sql`) ya existen. Todavía no hay aplicación
Flask.

El Paso 0 de `primeros-pasos.md` (venv, `requirements.txt`, `.env.example`,
`.gitignore`) se resuelve en el `paso01`, porque el Pedido 1 ya incluye esos
archivos. Acá no se crean archivos del repositorio.

## Objetivo

Dejar una base `escape_room_7b2026` creada desde cero, con el seed ejecutado
dos veces, y los conteos de control verificados.

## Alcance

- Crear la base con `bd/schema.sql`.
- Ejecutar `bd/seeds/001_contenido_inicial.sql` dos veces.
- Correr las consultas de control de este archivo.
- Anotar el resultado en `MEMORY.md`.
- No crear la app, no crear `requirements.txt`, no editar el seed.

## Reglas

- MySQL 8, `utf8mb4` / `utf8mb4_unicode_ci`.
- No cargar preguntas de `intermedio` ni `avanzado`.
- No "arreglar" el seed para que dé los conteos esperados: si algo no
  coincide, se revisa y se consulta.
- Para pruebas destructivas, usar una base local, nunca la de la feria.

## Criterio de aceptación

- [ ] `bd/schema.sql` corre sin errores en una base limpia.
- [ ] El seed corre dos veces sin duplicar filas.
- [ ] Hay 5 estaciones, 14 temas, 20 preguntas y 60 respuestas activas.
- [ ] Cada estación tiene 4 preguntas `inicial` activas.
- [ ] Cada tema activo tiene al menos 1 pregunta `inicial` activa.
- [ ] Cada pregunta tiene 3 respuestas activas y exactamente 1 correcta.
- [ ] Cada estación tiene 4 temas activos o menos.
- [ ] `configuracion` tiene 9 claves y las dos dificultades valen `0`.

## Verificación

Crear y cargar:

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
```

Conteos generales:

```sql
USE escape_room_7b2026;

SELECT 'estacion' AS tabla, COUNT(*) AS filas FROM estacion WHERE activo = 1
UNION ALL SELECT 'tema', COUNT(*) FROM tema WHERE activo = 1
UNION ALL SELECT 'pregunta', COUNT(*) FROM pregunta WHERE activo = 1
UNION ALL SELECT 'respuesta', COUNT(*) FROM respuesta WHERE activo = 1;
```

Esperado: `5`, `14`, `20`, `60`.

Cobertura por estación:

```sql
SELECT e.orden, e.nombre,
       COUNT(DISTINCT t.id) AS temas,
       COUNT(DISTINCT p.id) AS preguntas_inicial
FROM estacion e
LEFT JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.dificultad = 'inicial' AND p.activo = 1
WHERE e.activo = 1
GROUP BY e.id, e.orden, e.nombre
ORDER BY e.orden;
```

Esperado:

| orden | estación | temas | preguntas_inicial |
| --- | --- | --- | --- |
| 1 | Redes | 4 | 4 |
| 2 | Hardware | 3 | 4 |
| 3 | Internet | 3 | 4 |
| 4 | Ciberseguridad | 2 | 4 |
| 5 | Sistemas Operativos | 2 | 4 |

Temas sin preguntas del nivel:

```sql
SELECT t.id, t.nombre, e.nombre AS estacion
FROM tema t
JOIN estacion e ON e.id = t.estacion_id
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.dificultad = 'inicial' AND p.activo = 1
WHERE t.activo = 1 AND e.activo = 1
GROUP BY t.id, t.nombre, e.nombre
HAVING COUNT(p.id) = 0;
```

Esperado: 0 filas.

Opciones y respuesta correcta por pregunta:

```sql
SELECT p.id, p.titulo,
       COUNT(r.id) AS opciones,
       SUM(r.correcta) AS correctas
FROM pregunta p
LEFT JOIN respuesta r ON r.pregunta_id = p.id AND r.activo = 1
WHERE p.activo = 1
GROUP BY p.id, p.titulo
HAVING COUNT(r.id) <> 3 OR SUM(r.correcta) <> 1;
```

Esperado: 0 filas.

Temas activos por estación:

```sql
SELECT e.orden, e.nombre, COUNT(t.id) AS temas_activos
FROM estacion e
LEFT JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
WHERE e.activo = 1
GROUP BY e.id, e.orden, e.nombre
HAVING COUNT(t.id) > 4;
```

Esperado: 0 filas.

Configuración:

```sql
SELECT clave, valor FROM configuracion ORDER BY clave;
```

Esperado: 9 filas, con `dificultad_intermedia_habilitada = 0` y
`dificultad_avanzada_habilitada = 0`.

## Trampas conocidas

- El seed usa ids fijos y `ON DUPLICATE KEY UPDATE`; no cambia `activo` al
  reejecutarse. Si el admin desactivó algo, sigue desactivado.
- `configuracion` usa `INSERT IGNORE`: el seed no pisa valores cambiados.
- La colación `utf8mb4_unicode_ci` compara sin distinguir mayúsculas ni
  acentos. Dos nombres "Los Tigres" y "los tigres" son el mismo equipo.
- `intento.ultima_estacion_visitada` es una FK a `estacion.id`, no al
  `orden`. No confundirlos en los pasos siguientes.

## Al terminar

- Anotar en `MEMORY.md` que la base quedó verificada y con qué conteos.
- No hacer commit salvo que se haya corregido un error bloqueante, y en ese
  caso consultar primero.
