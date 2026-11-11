# Paso 11c — Contenido de nivel intermedio y avanzado

> **Origen:** pedido posterior al `paso11`, antes del `paso12`.
> **Tipo:** feat (contenido).
> **Requiere:** `paso11b` aprobado y los documentos de
> `docs/elaboradoChicos/` (recibidos el 11/11/2026).
> **Commit:** `feat: contenido intermedio y avanzado`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Reglas de contenido", decisión 14),
> `docs/escape-room.md`, `bd/seeds/001_contenido_inicial.sql` y
> `docs/prompt-paso11-c.txt`.

## Estado

Implementado y verificado el 11/11/2026. El banco de preguntas se revisó antes
de generar los seeds. El contenido se adaptó de `docs/elaboradoChicos/` y las
preguntas que faltaban se redactaron y quedaron documentadas en
`docs/banco-preguntas-intermedio-avanzado.md`. Los tres seeds se cargaron en la
base real con respaldo previo, se cerró como `abandono` el intento 10 del equipo
Canalla2 (resto de las pruebas manuales) y `intermedio` y `avanzado` se
habilitaron desde `/admin/dificultades`. La base real quedó con 80 preguntas y
240 respuestas activas y los dos niveles en `1`.

## Contexto

La aplicación ya soporta los tres niveles, pero el seed inicial solo carga
`inicial`. Para ofrecer `intermedio` y `avanzado` en la feria hace falta
cobertura completa en las cinco estaciones: al menos una pregunta por tema
activo y cuatro por estación.

Con los 14 temas actuales, el mínimo es:

| Estación | Temas | Mínimo por tema | Falta para 4 |
| --- | --- | --- | --- |
| Redes | 4 | 4 | 0 |
| Hardware | 3 | 3 | 1 |
| Internet | 3 | 3 | 1 |
| Ciberseguridad | 2 | 2 | 2 |
| Sistemas Operativos | 2 | 2 | 2 |
| **Total** | **14** | **14** | **+6** |

Por eso el mínimo real es **20 preguntas por nivel**. El objetivo es cargar
**30 preguntas por nivel** (6 por estación) para que haya sorteo real en las
cinco estaciones.

## Diagnóstico de las fuentes

| Archivo | Qué contiene | Cómo se usa |
| --- | --- | --- |
| `contenido-intermedio.odt` | 8 secciones de mantenimiento y redes (mantenimiento, redes avanzadas, instalaciones, rendimiento, conexiones, herramientas, tipos de mantenimiento, identificación de dispositivos). | Base de `contenido-para-responder-nivel-intermedio.md` y de las preguntas de Redes y Hardware. |
| `ESCAPEROOM-intermedio.odt` | 20 preguntas de intermedio con 3 opciones, agrupadas por temas de redes y mantenimiento. | Banco de preguntas de intermedio para Redes y Hardware. |
| `ESCAPEROOM-avanzado.odt` | 20 preguntas de avanzado (4 por estación) con 3 opciones y la correcta marcada en negrita. | Banco base de avanzado para las cinco estaciones. |
| `pistas-inicial.odt` | 20 preguntas con 2 pistas (fácil y difícil) cada una. | Se unifican en `docs/pistas-del-juego.md`. |
| `pistas-intermedio.odt` | 20 preguntas con 2 pistas (fácil y difícil) cada una. | Se unifican en `docs/pistas-del-juego.md`. |
| `pistas-avanzado.odt` | 20 preguntas con 2 pistas (fácil y difícil) cada una. | Se unifican en `docs/pistas-del-juego.md`. |

### Observación importante

`contenido-intermedio.odt` y `ESCAPEROOM-intermedio.odt` cubren **solo Redes y
Hardware**. No hay material de origen para Internet, Ciberseguridad ni Sistemas
Operativos en nivel intermedio. Esas preguntas se redactan a partir de los
contenidos equivalentes de avanzado y de los conceptos ya presentes en el nivel
inicial, con redacción propia y revisión docente. No se copian preguntas
iniciales para completar cobertura.

`ESCAPEROOM-avanzado.odt` sí cubre las cinco estaciones, pero trae 20 preguntas
en total (4 por estación). Para llegar a 6 por estación se agregan 10 preguntas
nuevas: NAT, WPA3, HDD/SSD, memoria virtual, caché del navegador, parámetros de
URL, ransomware, ingeniería social, proceso/hilo y aplicaciones fuera de la
tienda oficial.

## Entregables

| Archivo | Tipo | Contenido |
| --- | --- | --- |
| `docs/contenido-para-responder-nivel-intermedio.md` | Markdown | Explicaciones básicas para que un participante pueda jugar el nivel intermedio. |
| `docs/contenido-para-responder-nivel-avanzado.md` | Markdown | Explicaciones básicas para que un participante pueda jugar el nivel avanzado. |
| `docs/pistas-del-juego.md` | Markdown | Las 160 pistas (2 por cada una de las 80 preguntas cargadas) más un anexo con las pistas de las preguntas en reserva. |
| `bd/seeds/002_contenido_intermedio.sql` | SQL | Preguntas y respuestas de intermedio. Equivale al `intermedio.sql` del pedido. |
| `bd/seeds/003_contenido_avanzado.sql` | SQL | Preguntas y respuestas de avanzado. Equivale al `avanzado.sql` del pedido. |

Los nombres `002_...` y `003_...` respetan la numeración de seeds del proyecto.
No se crean archivos sueltos `intermedio.sql` ni `avanzado.sql` para no romper
el orden de carga.

## Mapa de contenido

Se mantienen los **14 temas existentes** para no romper la cobertura de
`inicial`: cada tema activo necesita al menos una pregunta de cada nivel y no
se agregan temas nuevos en este paso. Las preguntas se distribuyen así:

| Estación | Temas existentes | Distribución objetivo (6) |
| --- | --- | --- |
| Redes | IP, Router, Redes de computadoras, WiFi | IP 2, Router 1, Redes de computadoras 2, WiFi 1 |
| Hardware | Procesador, Dispositivos de E/S, Memoria RAM | Procesador 2, Dispositivos de E/S 2, Memoria RAM 2 |
| Internet | Navegadores Web, URL, Conectividad | Navegadores Web 1, URL 1, Conectividad 4 |
| Ciberseguridad | Contraseña, Phishing | Contraseña 3, Phishing 3 |
| Sistemas Operativos | Sistema Operativo, Dispositivos Móviles | Sistema Operativo 4, Dispositivos Móviles 2 |

Resultado final: **14 temas activos**, **80 preguntas** en total (20 `inicial`,
30 `intermedio` y 30 `avanzado`). En `intermedio` y `avanzado` cada estación
tiene **6 preguntas** (4 es el mínimo).

### Criterio de clasificación

- Las preguntas de mantenimiento y almacenamiento se agrupan en los temas de
  Hardware existentes: procesador, dispositivos de E/S y memoria RAM.
- Las preguntas de ataques y propiedades de seguridad se agrupan en
  `Contraseña` y `Phishing`.
- Las preguntas de protocolos y códigos HTTP se agrupan en `Conectividad`,
  `URL` y `Navegadores Web`.
- Las preguntas de procesos y planificación se agrupan en `Sistema Operativo`.

Si más adelante el docente quiere temas separados (por ejemplo,
"Mantenimiento", "Ataques informáticos" o "Procesos"), hay que crear el tema
**y** agregar al menos una pregunta de `inicial` para ese tema. Eso queda fuera
de este paso porque modifica la cobertura del nivel inicial.

## Contenido de las guías

`docs/contenido-para-responder-nivel-intermedio.md` y
`docs/contenido-para-responder-nivel-avanzado.md` son materiales de estudio
para leer antes de jugar o para imprimir en el stand. No se cargan en la
aplicación ni se muestran desde el juego.

Cada guía debe incluir:

- Una introducción breve sobre el nivel y cómo se juega.
- Una sección por estación, en el orden del recorrido.
- Explicaciones con ejemplos cotidianos, sin copiar el enunciado exacto de cada
  pregunta.
- Un glosario mínimo al final.
- Lenguaje claro, en español rioplatense, sin siglas sin explicar.

Las guías **no** reemplazan al banco de preguntas: la única fuente de verdad del
juego sigue siendo la base de datos.

## Pistas del juego

`docs/pistas-del-juego.md` reúne las pistas de los tres niveles:

- 80 preguntas cargadas, 2 pistas por pregunta (fácil y difícil): 160 pistas en
  el cuerpo principal.
- Un anexo **reserva** con las pistas de las preguntas descartadas del banco,
  para no perder el trabajo y poder recuperarlas si se cambia el contenido.
- Agrupadas por nivel y por estación, en el orden del recorrido.
- Se pueden corregir tildes, redundancias y redacción para que se entiendan
  mejor, sin cambiar la idea.
- El archivo es para leer en papel o imprimir. **La app no muestra el texto de
  las pistas**: solo registra la cantidad de ayudas usadas.
- No se crea tabla `pista` ni se cargan las pistas en la base.

## Alcance

### Seeds

`bd/seeds/002_contenido_intermedio.sql`:

- Idempotente, con el mismo patrón que el seed inicial.
- Ids reservados: `1001+` para preguntas y `2001+` para respuestas.
- No crea temas nuevos ni cambia `activo` de filas existentes.
- No habilita el nivel ni modifica `configuracion`.
- Tres opciones por pregunta y exactamente una correcta.

`bd/seeds/003_contenido_avanzado.sql`:

- Idempotente, con el mismo patrón que el seed inicial.
- Ids reservados: `3001+` para preguntas y `4001+` para respuestas.
- No crea temas nuevos ni cambia `activo` de filas existentes.
- No habilita el nivel ni modifica `configuracion`.
- Tres opciones por pregunta y exactamente una correcta.

### Pruebas y documentación

- `tests/conftest.py` y `tests/helpers.py`: cargar el seed 001, el 002 y el 003.
- `tests/test_seed.py`: conteos nuevos e idempotencia de los seeds 002 y 003.
- `tests/test_admin.py`: adaptar cobertura y toggles al contenido real de los
  tres niveles.
- `tests/test_seleccion.py`: intentos `intermedio` y `avanzado` con 4 preguntas
  del nivel, al menos una por tema y estables al recargar.
- `tests/test_bienvenida.py`: la bienvenida ofrece los niveles habilitados.
- Documentación de conteos: `README.md`, `AGENTS.md`, `MEMORY.md` y las guías
  de `docs/` que correspondan.

## Proceso

1. Convertir los `.odt` con `pandoc` y normalizar el texto (tildes, listas,
   opciones A/B/C).
2. Armar el borrador de las dos guías y del archivo de pistas.
3. Armar el banco de preguntas en Markdown para revisión docente: estación,
   tema, pregunta, tres opciones y cuál es la correcta.
4. Revisado el borrador, generar
   `bd/seeds/002_contenido_intermedio.sql` y
   `bd/seeds/003_contenido_avanzado.sql`.
5. Cargar ambos seeds en la base de la feria.
6. Verificar cobertura y habilitar `intermedio` y `avanzado` desde
   `/admin/dificultades` (nunca desde los seeds).
7. Jugar una partida completa de cada nivel y confirmar que entran al ranking
   de su nivel.

## Fuera de alcance

- Modificar `docs/escape-room.md` sin autorización.
- Cambios de esquema.
- Crear una tabla `pista` o cargar pistas en la aplicación.
- Mostrar pistas en las pantallas de juego.
- Cambiar tiempos, reglas, ayudas o envíos.
- Agregar dependencias o CDN.
- Duplicar preguntas del nivel inicial para completar cobertura.
- Reemplazar los documentos de `docs/elaboradoChicos/`: son la fuente y no se
  editan.

## Criterio de aceptación

- Los seeds 002 y 003 dejan cobertura completa de `intermedio` y `avanzado` en
  las cinco estaciones.
- Reejecutar cada seed no duplica ni reactiva contenido.
- Después de los seeds, `dificultad_intermedia_habilitada` y
  `dificultad_avanzada_habilitada` siguen en `0`.
- Cada nivel se habilita desde `/admin/dificultades` y aparece en la bienvenida.
- Una partida completa de `intermedio` y otra de `avanzado` funcionan y entran
  al ranking de su nivel.
- Cada tema activo tiene al menos una pregunta de cada nivel y cada estación
  tiene 4 como mínimo (objetivo: 6).
- `docs/pistas-del-juego.md` contiene las 160 pistas de las preguntas cargadas
  y la app no las muestra.
- `pytest -q` pasa dos veces seguidas con 88 tests.

## Verificación

Sobre una base limpia, cargar primero el contenido inicial:

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Consultas útiles:

```sql
SELECT e.orden, e.nombre, p.dificultad, COUNT(p.id) AS preguntas
FROM estacion e
JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.activo = 1 AND p.dificultad IN ('intermedio', 'avanzado')
WHERE e.activo = 1
GROUP BY e.id, e.orden, e.nombre, p.dificultad
ORDER BY e.orden, p.dificultad;

SELECT t.id, t.nombre, p.dificultad, COUNT(p.id) AS preguntas
FROM tema t
LEFT JOIN pregunta p ON p.tema_id = t.id
     AND p.activo = 1 AND p.dificultad IN ('intermedio', 'avanzado')
WHERE t.activo = 1
GROUP BY t.id, t.nombre, p.dificultad
ORDER BY t.id, p.dificultad;
```

## Ojo con

- `contenido-intermedio.odt` y `ESCAPEROOM-intermedio.odt` no cubren Internet,
  Ciberseguridad ni Sistemas Operativos. Esas preguntas se redactan y se
  revisan; no se copian del nivel inicial.
- `ESCAPEROOM-avanzado.odt` trae 4 preguntas por estación. Si no se agregan las
  2 restantes, la cobertura mínima se cumple, pero el sorteo queda pobre.
- Los temas nuevos no se agregan en este paso. Si el docente los quiere, hay
  que sumar una pregunta de `inicial` por cada tema para no romper la
  cobertura del nivel inicial.
- Los ids de preguntas y respuestas son altos para no chocar con el contenido
  creado desde `/admin`.
- Los scripts de `/docker-entrypoint-initdb.d` y los seeds solo se ejecutan una
  vez si el volumen ya existe.
- No cargar los seeds después del `paso12`: ese paso congela el contenido.
- No habilitar un nivel con cobertura incompleta.
- No usar preguntas del nivel `inicial` para completar la cobertura.
- Las pistas son material impreso: la app solo registra las ayudas.
