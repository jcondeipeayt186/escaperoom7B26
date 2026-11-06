# Paso 11c — Contenido de nivel intermedio

> **Origen:** pedido posterior al `paso11`, antes del `paso12`.
> **Tipo:** feat (contenido).
> **Requiere:** `paso11b` aprobado y los documentos de contenido que aporte el
> usuario.
> **Commit:** `feat: contenido de nivel intermedio`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Reglas de contenido", decisión 14),
> `docs/escape-room.md` y `bd/seeds/001_contenido_inicial.sql`.

## Estado

El archivo del paso se crea ahora, pero la implementación queda **pendiente**
hasta que el usuario entregue los documentos con las preguntas. El contenido
no se inventa.

## Contexto

La aplicación ya soporta los tres niveles, pero el seed inicial solo carga
`inicial`. Para habilitar `intermedio` en la feria hace falta cobertura
completa: al menos una pregunta por tema activo y cuatro por estación.

Con los temas actuales, el mínimo es:

| Estación | Temas | Mínimo por tema | Falta para 4 |
| --- | --- | --- | --- |
| Redes | 4 | 4 | 0 |
| Hardware | 3 | 3 | 1 |
| Internet | 3 | 3 | 1 |
| Ciberseguridad | 2 | 2 | 2 |
| Sistemas Operativos | 2 | 2 | 2 |
| **Total** | **14** | **14** | **+6** |

Por eso el mínimo real es **20 preguntas**. El objetivo del paso es cargar
**30 preguntas** (6 por estación) para que haya sorteo real en las cinco
estaciones.

## Proceso

1. El usuario entrega los documentos con el contenido.
2. Preparar un **borrador en Markdown** para revisión docente: estación, tema,
   pregunta, tres opciones y cuál es la correcta.
3. Revisado el borrador, generar
   `bd/seeds/002_contenido_intermedio.sql`.
4. Cargar el seed en la base de la feria y habilitar `intermedio` desde
   `/admin/dificultades` (no desde el seed).
5. Verificar cobertura y jugar una partida completa de `intermedio`.

## Alcance

- `bd/seeds/002_contenido_intermedio.sql`:
  - Idempotente, con el mismo patrón que el seed inicial.
  - Ids reservados altos: `1001+` para preguntas y `2001+` para respuestas,
    para no chocar con contenido creado desde `/admin`.
  - No cambia `activo` de filas existentes.
  - No habilita el nivel ni modifica `configuracion`.
  - Tres opciones por pregunta y exactamente una correcta.
- `tests/conftest.py` y `tests/helpers.py`: cargar el seed 001 y el 002.
- `tests/test_seed.py`: conteos nuevos e idempotencia del seed 002.
- `tests/test_admin.py`: adaptar cobertura y toggles al contenido real.
- `tests/test_seleccion.py`: intento `intermedio` con 4 preguntas del nivel,
  al menos una por tema y estables al recargar.
- Documentación de conteos: `README.md`, `AGENTS.md`, `MEMORY.md` y las guías
  de `docs/` que correspondan.

## Fuera de alcance

- Nivel `avanzado`.
- Cambios de esquema.
- Preguntas de otros niveles.
- Modificar `docs/escape-room.md` sin autorización.

## Criterio de aceptación

- El seed 002 deja cobertura completa de `intermedio` en las cinco estaciones.
- Reejecutar el seed no duplica ni reactiva contenido.
- Después del seed, `dificultad_intermedia_habilitada` sigue en `0`.
- El nivel se habilita desde `/admin/dificultades` y aparece en la bienvenida.
- Una partida completa de `intermedio` funciona y entra al ranking de su nivel.
- `pytest -q` pasa dos veces seguidas.

## Verificación

```bash
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Consultas útiles:

```sql
SELECT e.orden, e.nombre, COUNT(p.id) AS preguntas
FROM estacion e
JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.activo = 1 AND p.dificultad = 'intermedio'
WHERE e.activo = 1
GROUP BY e.id
ORDER BY e.orden;

SELECT t.id, t.nombre, COUNT(p.id) AS preguntas
FROM tema t
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.activo = 1 AND p.dificultad = 'intermedio'
WHERE t.activo = 1
GROUP BY t.id
ORDER BY t.id;
```

## Ojo con

- Los scripts de `/docker-entrypoint-initdb.d` y los seeds solo se ejecutan
  una vez si el volumen ya existe.
- No cargar el seed después del `paso12`: ese paso congela el contenido.
- No habilitar `intermedio` con cobertura incompleta.
- No usar preguntas del nivel `inicial` para completar la cobertura.
