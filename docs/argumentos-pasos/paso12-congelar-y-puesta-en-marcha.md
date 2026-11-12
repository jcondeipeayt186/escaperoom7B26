# Paso 12 — Congelar, respaldar y poner en marcha

> **Origen:** Pedido 12 de `docs/primeros-pasos.md` (Paso 10).
> **Tipo:** infra (con partes manuales).
> **Requiere:** `paso11e` aprobado y commiteado.
> **Commit:** `docs: puesta en marcha y respaldo`.
>
> **Antes de empezar:** leé `AGENTS.md`,
> `docs/instalacion-y-puesta-en-funcionamiento.md`,
> `docs/instalacion-servidor-escuela.md` y `MEMORY.md`.
>
> **Docker:** es una alternativa opcional posterior a la feria. Se trata en
> `paso13-docker-taller-post-feria.md` y **no** reemplaza waitress/systemd.

## Contexto

La app y los tests están listos. Falta dejarla preparada para el aula, sin
cambios de último momento.

Hay **dos equipos candidatos** para oficiar de servidor:

1. La notebook del docente con **Ubuntu 22.04**.
2. Un **servidor Linux de la escuela** con MySQL 8 y `sudo` completo. La
   distribución y la versión todavía no están confirmadas.

La idea es dejar la aplicación funcionando en ambos y decidir el día de la
feria cuál usar. La notebook queda como principal y el servidor de la escuela
como respaldo.

Existe además una tercera variante: dejar **solo la base de datos** en el
servidor de la escuela y la app en la notebook.

## Objetivo

Dejar la aplicación congelada, con backup probado y un procedimiento de
arranque que funcione sin Internet, en los tres escenarios posibles.

## Escenarios de despliegue

| | **A — Todo en la notebook** | **B — Todo en el servidor** | **C — Base en la escuela, app en la notebook** |
| --- | --- | --- | --- |
| Flask + waitress | Notebook Ubuntu 22.04 | Servidor de la escuela | Notebook Ubuntu 22.04 |
| MySQL 8 | Notebook | Servidor de la escuela | Servidor de la escuela |
| Dependencia de red entre app y base | Ninguna | Ninguna | Cada request depende de la LAN |
| Punto único de falla | La notebook | El servidor | Dos equipos |
| Permisos necesarios | Locales | `sudo` en el servidor | `sudo` en ambos y abrir `3306` en la LAN |
| Dónde se respalda | Notebook | Servidor | Servidor (o desde la notebook) |
| Complejidad | Baja, ya probada | Media | Alta |
| Riesgo principal | Suspensión o uso indebido de la notebook | Distro vieja, servidor compartido | Corte de red, reloj, MySQL expuesto |

Documentación de cada escenario:

- **A:** `docs/instalacion-y-puesta-en-funcionamiento.md`.
- **B y C:** `docs/instalacion-servidor-escuela.md`.

### Decisión tomada

- **A es el escenario principal**, porque ya está probado y no depende de la
  red entre la app y la base.
- **B es el respaldo**, porque el servidor tiene `sudo` completo y MySQL 8.
- **C se documenta, pero no se improvisa.** Solo se usa si se ensayó antes y
  hay una ventaja concreta, por ejemplo un UPS o respaldos centralizados.

### Restricciones técnicas comunes

| Requisito | Detalle |
| --- | --- |
| Python 3.10 o superior | `pytest 9.2` lo exige; Flask 3.1 acepta 3.9. |
| MySQL 8.0 o MariaDB 10.3 o superior | El ranking usa `ROW_NUMBER() OVER (...)`; el esquema usa columnas generadas y `CHECK`. |
| Misma red | Notebooks y televisor en la misma LAN que el servidor. |
| Puerto `8000` libre | Puerto de waitress. |
| Reloj y zona horaria correctos | La app inserta `NOW(3)` de MySQL: el reloj de la base es la autoridad. |
| `sudo` en el servidor | Sin permisos, B y C no son viables. |
| Sin Internet | Bootstrap, audio y gráficos son locales. |

### Ficha del servidor de la escuela

Completar con los datos reales. La sección 2 de
`docs/instalacion-servidor-escuela.md` tiene los comandos para obtenerlos.

| Dato | Valor |
| --- | --- |
| Distribución y versión | |
| Arquitectura | |
| Python disponible | |
| Motor y versión | |
| Gestor de paquetes | |
| Usuario con `sudo` | |
| IP del servidor | |
| IP fija o DHCP | |
| Firewall | |
| ¿Servidor exclusivo o compartido? | |
| ¿Tiene UPS? | |
| ¿Tiene Internet o mirror interno? | |

Mientras la ficha esté incompleta, el procedimiento de B y C queda **a
validar**. No alcanza con que los comandos sean genéricos: hay que ejecutarlos
en el servidor.

## Alcance

- Revisar y congelar el contenido de los tres niveles.
- Generar un volcado de la base y probar la restauración en una base limpia.
- Documentar el arranque con waitress en `0.0.0.0`.
- Configurar `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` reales.
- Probar desde 3 notebooks y el televisor en A y en B.
- Verificar el funcionamiento sin Internet.
- Dejar scripts de backup y restauración que funcionen en A, B y C.
- Elegir qué niveles se ofrecen en la feria.

No cambiar el esquema, no cargar contenido nuevo y no tocar la lógica del
juego en este paso. Si aparece un error bloqueante, se corrige en un commit
aparte y se vuelve a probar.

## Contenido a congelar

Estado esperado del contenido:

| Tabla | Filas |
| --- | --- |
| `estacion` | 5 |
| `tema` | 14 |
| `pregunta` | 80 |
| `respuesta` | 240 |
| `configuracion` | 9 |

Preguntas por nivel:

- `inicial`: 20 (4 por estación).
- `intermedio`: 30 (6 por estación).
- `avanzado`: 30 (6 por estación).

Antes de congelar:

1. Revisar en `/admin/cobertura` que las tres columnas estén en verde.
2. Revisar en `/admin/dificultades` qué niveles quedan habilitados. Al
   12/11/2026 están habilitados `inicial`, `intermedio` y `avanzado`.
3. Revisar las descripciones de `intermedio` y `avanzado`; las 20 preguntas de
   `inicial` no llevan descripción.
4. Jugar una partida completa de `inicial`, una de `intermedio` y una de
   `avanzado` y confirmar que cada una entra al ranking de su nivel.
5. Anotar la fecha de congelamiento y el estado de los niveles.

Las fuentes de contenido son `bd/seeds/001_contenido_inicial.sql`,
`002_contenido_intermedio.sql`, `003_contenido_avanzado.sql` y el archivo
completo `bd/escape_room_7b2026_completa.sql` (elimina y recrea las 12 tablas).
Los seeds son idempotentes, pero al reejecutarlos pisan lo editado desde
`/admin`.

## Scripts

Ya existen `scripts/backup.sh` y `scripts/restaurar.sh`.

### `scripts/backup.sh`

- Lee `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DB`
  del `.env` o de `ENV_FILE`.
- No usa `source .env`: `ADMIN_PASSWORD_HASH` contiene `$` y rompería la shell.
- Usa `mysqldump --single-transaction --default-character-set=utf8mb4` y
  agrega `--no-tablespaces` cuando la herramienta lo soporta; no usa
  `--databases`.
- Genera `respaldo-<base>-AAAAMMDD-HHMMSS.sql` con permisos `600`.
- Falla si el archivo queda vacío.

```bash
./scripts/backup.sh                     # $HOME/backups-escaperoom
./scripts/backup.sh /var/backups/escaperoom
```

Funciona igual en A, B y C porque respeta `MYSQL_HOST` y `MYSQL_PORT`.

### `scripts/restaurar.sh`

- Recibe un volcado y, opcionalmente, la base destino.
- Sin destino, crea `<MYSQL_DB>_restore_AAAAMMDD-HHMMSS`.
- Se niega a pisar `MYSQL_DB` o una base existente sin `--force`.
- Rechaza volcados con `CREATE DATABASE` o `USE` sin `--force`.
- Restaura en `utf8mb4` y muestra los conteos al final.

```bash
./scripts/restaurar.sh /ruta/al/respaldo.sql
./scripts/restaurar.sh /ruta/al/respaldo.sql escape_room_7b2026_restore_test
./scripts/restaurar.sh /ruta/al/respaldo.sql escape_room_7b2026 --force
```

Nunca commitear el volcado, el `.env` ni los archivos de `bd/backups/`.

## Arranque

- Usar waitress, no el servidor de desarrollo.
- Escuchar en `0.0.0.0:8000` para que se conecten las notebooks.
- Dejar el proceso estable con systemd.
- `.env` con valores reales, permisos `600`, fuera de Git.
- En B, ajustar el servicio al nombre del motor (`mysql.service` o
  `mysqld.service`) y a la distribución.
- En C, la notebook corre la app y apunta `MYSQL_HOST` a la IP del servidor de
  la escuela; el `3306` se abre solo para la IP de la notebook.

El procedimiento completo está en:

- A: `docs/instalacion-y-puesta-en-funcionamiento.md`, secciones 4 a 8.
- B y C: `docs/instalacion-servidor-escuela.md`, secciones 4 y 5.

## Criterios de aceptación

### Comunes a los tres escenarios

- [ ] La app levanta desde cero con los comandos documentados.
- [ ] `/salud` responde `200` con `{"estado": "ok", "base": "ok"}`.
- [ ] `/admin` entra con `ADMIN_USER` y la clave real.
- [ ] El contenido está congelado y anotado: `5/14/80/240/9`.
- [ ] `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` son reales y no están
      versionados.
- [ ] El `.env` tiene permisos `600` y no está en Git.
- [ ] El backup se restaura en una base limpia y los conteos coinciden.
- [ ] Los scripts de backup y restauración funcionan.
- [ ] Sin Internet, todo sigue funcionando: Bootstrap, audio y gráficos
      locales.
- [ ] El reloj del equipo que corre MySQL está en hora.

### Escenario A — notebook

- [ ] waitress escucha en `0.0.0.0:8000`.
- [ ] 3 notebooks juegan a la vez sin errores.
- [ ] El televisor muestra `/ranking` actualizándose.
- [ ] Suspensión y tapa cerrada desactivadas.
- [ ] IP fija o reserva DHCP anotada.

### Escenario B — servidor de la escuela

- [ ] Ficha del servidor completa (sección anterior).
- [ ] Python 3.10+ y MySQL 8.0+ verificados.
- [ ] Servicio systemd habilitado con `Restart=always`.
- [ ] `8000` abierto solo para la red del aula.
- [ ] `3306` cerrado al exterior.
- [ ] 3 notebooks y el televisor funcionan contra el servidor.
- [ ] Reinicio del servidor: la app vuelve sola.

### Escenario C — base remota

- [ ] Usuario `'escaperoom'@'IP-NOTEBOOK'`, nunca `'%'`.
- [ ] `3306` abierto solo para la IP de la notebook.
- [ ] Conexión remota probada con `nc` y con `mysql`.
- [ ] Corte de red probado: la app falla de forma visible, no inventa
      resultados.
- [ ] Reinicio de MySQL probado: la app se reconecta.
- [ ] Procedimiento de vuelta a A escrito y probado.

## Verificación

### 1. Backup y restauración

```bash
./scripts/backup.sh /tmp/backups-escaperoom
./scripts/restaurar.sh /tmp/backups-escaperoom/respaldo-....sql
```

En la base restaurada, los conteos deben ser `5/14/80/240/9`.

Probar además que `restaurar.sh` se niega a pisar la base real:

```bash
./scripts/restaurar.sh /tmp/backups-escaperoom/respaldo-....sql
# y luego, sin --force:
./scripts/restaurar.sh /tmp/backups-escaperoom/respaldo-....sql escape_room_7b2026
```

El segundo comando debe terminar con error y sin cambios.

### 2. Simulacro A

1. Levantar waitress en la notebook.
2. Conectar 3 notebooks y un televisor.
3. Jugar con 3 equipos a la vez.
4. Cortar Internet y repetir una estación.
5. Reiniciar MySQL y confirmar que la app se reconecta.
6. Restaurar el backup en una base limpia.
7. Cronometrar el arranque desde cero.

### 3. Simulacro B

1. Repetir los pasos anteriores contra el servidor de la escuela.
2. Reiniciar el servidor y confirmar que el servicio vuelve solo.
3. Probar desde una notebook con la IP real del servidor.

### 4. Simulacro C

Solo si se decide usar C:

1. Jugar una estación completa con la base remota.
2. Cortar la red de la notebook y confirmar que la app falla de forma visible.
3. Restaurar la red y continuar.
4. Reiniciar MySQL en el servidor y confirmar la reconexión.
5. Volver a A siguiendo el procedimiento escrito.

## Trampas conocidas

- El backup no está probado hasta que se restaura.
- Guardar el backup en un pendrive y en la nube, no solo en el servidor.
- `mysqldump --databases` incluye `CREATE DATABASE` y `USE`; los scripts no lo
  usan a propósito.
- No dejar el servidor de desarrollo de Flask para la feria.
- No hacer cambios de código el día de la feria.
- Verificar que el audio y Bootstrap sean locales; un CDN que falla deja la
  pantalla rota.
- El reloj del equipo que corre MySQL es la fuente de tiempo: revisarlo.
- Una distribución vieja puede traer Python 3.6 u 8 y MySQL 5.7; verificar
  antes de prometer el escenario B.
- Abrir `3306` a toda la red es un riesgo innecesario: en C va solo la IP de la
  notebook.
- Un servidor compartido que se reinicia o actualiza solo puede cortar la
  feria. Confirmar la política antes.
- Una IP por DHCP puede cambiar entre el ensayo y la feria.
- En C, el respaldo debe quedar en el servidor y copiarse afuera; si se pierde
  el servidor, se pierde todo.
- No restaurar sobre la base real sin backup previo y sin `--force` consciente.

## Día de la feria

Orden recomendado:

1. Usar **A** como principal.
2. Tener **B** listo como respaldo.
3. Usar **C** solo si se ensayó y A y B no son viables.

Árbol de decisión:

```text
¿La notebook arranca y tiene la app probada?
├── Sí → usar A.
└── No
    ├── ¿El servidor de la escuela tiene la app instalada y probada?
    │   ├── Sí → usar B.
    │   └── No → reinstalar A en otra notebook o resolver el servidor.
    └── ¿Se ensayó C con corte de red y reloj?
        ├── Sí → usar C solo si A y B no son viables.
        └── No → no usar C.
```

## Al terminar

- Resumir qué escenarios quedaron probados, en qué equipos y con qué
  resultados.
- Anotar la ficha del servidor de la escuela y la fecha de congelamiento.
- Actualizar `MEMORY.md` con el estado final.
- Commit: `docs: puesta en marcha y respaldo`.
