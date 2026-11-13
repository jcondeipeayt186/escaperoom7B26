# Paso 12 — La feria con el servidor de Flask

> **Origen:** Pedido 12 de `docs/primeros-pasos.md` (Paso 10).
> **Tipo:** infra (con partes manuales).
> **Requiere:** `paso11g` aprobado y commiteado.
> **Commit:** `docs: feria con flask y respaldo`.
>
> **Antes de empezar:** leé `AGENTS.md` (decisión 65), `README.md`,
> `docs/instalacion-y-puesta-en-funcionamiento.md` y `MEMORY.md`.
>
> **Decisión del 13/11/2026:** la feria del 16/11/2026 se corre con el servidor
> de desarrollo de Flask, `flask --app app run --debug --host=0.0.0.0`, en la
> notebook del docente y con la terminal abierta. Ya está probado para una
> notebook, hasta tres equipos y el televisor en la misma red.
>
> **Waitress y systemd no se usan en la feria.** Quedan como puesta en
> producción posterior en `paso13-waitress-y-systemd-post-feria.md`. Docker
> queda como taller educativo en `paso14-docker-taller-post-feria.md`.

## Contexto

La app, el contenido y los tests están listos. Falta dejarla preparada para el
aula, sin cambios de último momento:

- El contenido congelado.
- Un respaldo probado.
- Un `.env` real, con permisos `600`.
- Un único comando de arranque que funcione en la notebook.
- Un ensayo con tres notebooks y el televisor, sin Internet.

La notebook del docente con Ubuntu 22.04 es el servidor de la feria. El
servidor Linux de la escuela y la variante de base remota se documentan recién
en el `paso13`, para después de la feria.

## Objetivo

Dejar la aplicación congelada, con respaldo probado y un arranque de un solo
comando para la feria del 16/11/2026, usando el servidor de desarrollo de Flask.

## Alcance

- Revisar y congelar el contenido de los tres niveles.
- Generar un volcado de la base y probar la restauración en una base limpia.
- Configurar `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` reales en `.env`.
- Crear `scripts/feria.sh` para levantar la app con un solo comando.
- Probar desde 3 notebooks y el televisor en la misma red.
- Verificar el funcionamiento sin Internet.
- Dejar el checklist del día de la feria.

No cambiar el esquema, no cargar contenido nuevo y no tocar la lógica del juego
en este paso. Si aparece un error bloqueante, se corrige en un commit aparte y
se vuelve a probar.

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
   13/11/2026 están habilitados `inicial`, `intermedio` y `avanzado`.
3. Revisar las descripciones de `intermedio` y `avanzado`, y las explicaciones e
   introducciones del `paso11g`.
4. Jugar una partida completa de `inicial`, una de `intermedio` y una de
   `avanzado` y confirmar que cada una entra al ranking de su nivel.
5. Anotar la fecha de congelamiento y el estado de los niveles.

Las fuentes de contenido son `bd/seeds/001_contenido_inicial.sql`,
`002_contenido_intermedio.sql`, `003_contenido_avanzado.sql` y el archivo
completo `bd/escape_room_7b2026_completa.sql`. Los seeds son idempotentes, pero
al reejecutarlos pisan lo editado desde `/admin`.

## Respaldo

Ya existen `scripts/backup.sh` y `scripts/restaurar.sh`. No se reescriben en
este paso: se prueban.

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

## Script de arranque de la feria

### Archivo nuevo: `scripts/feria.sh`

Crea un entorno virtual propio de la feria en `feria2026/`, instala las
dependencias solo si faltan y levanta Flask escuchando en `0.0.0.0`. No usa
`waitress`, no usa `systemd` y no requiere Internet si el entorno ya está
creado.

Comportamiento:

1. Se ubica en la raíz del proyecto, sin importar desde dónde se lo llame.
2. Falla con un mensaje claro si no existe `.env`.
3. Si `feria2026/bin/python` no existe, crea el entorno con `python3 -m venv`.
4. Prueba `import flask, pymysql, dotenv`. Si falla, instala
   `requirements.txt` en ese entorno.
5. Muestra la IP de la notebook para que las otras se conecten.
6. Ejecuta `feria2026/bin/python -m flask --app app run --debug
   --host=0.0.0.0 "$@"`.

Contenido completo:

```bash
#!/usr/bin/env bash
# Levanta la app para la feria del 16/11/2026 con el servidor de Flask.
#
# Uso:
#   ./scripts/feria.sh
#   ./scripts/feria.sh --port=5001
#
# Requiere python3 y el archivo .env en la raíz del proyecto.
# La primera vez crea el entorno virtual feria2026/ e instala dependencias.
# Después arranca sin instalar nada, aunque no haya Internet.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

ENTORNO="$RAIZ/feria2026"
PYTHON="$ENTORNO/bin/python"

if [ ! -f "$RAIZ/.env" ]; then
  echo "Falta el archivo .env en $RAIZ." >&2
  echo "Copiá .env.example y completá los valores reales antes de arrancar." >&2
  exit 1
fi

if [ ! -x "$PYTHON" ]; then
  echo "Creando el entorno virtual en feria2026/ ..."
  python3 -m venv "$ENTORNO"
fi

if ! "$PYTHON" -c "import flask, pymysql, dotenv" >/dev/null 2>&1; then
  echo "Instalando dependencias en feria2026/ ..."
  "$PYTHON" -m pip install --upgrade pip
  "$PYTHON" -m pip install -r "$RAIZ/requirements.txt"
fi

IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
echo "Servidor de la feria: http://${IP:-IP-DE-LA-NOTEBOOK}:5000"
echo "Abrí esa dirección desde las otras notebooks y el televisor."
echo "Para cerrar, presioná Ctrl+C en esta terminal."

exec "$PYTHON" -m flask --app app run --debug --host=0.0.0.0 "$@"
```

Después de crearlo:

```bash
chmod +x scripts/feria.sh
```

`feria2026/` va al `.gitignore`, igual que `.venv/`. No se commitea.

### Cómo se usa en la feria

```bash
./scripts/feria.sh
```

La terminal queda abierta. No se cierra ni se minimiza: ahí corre el servidor.
Si se cierra, el juego se corta.

## Red y notebook

Checklist previo:

- [ ] Notebook enchufada a corriente.
- [ ] Suspensión y apagado de pantalla desactivados.
- [ ] Tapa abierta y notebook sin moverse.
- [ ] IP de la notebook anotada (`hostname -I`).
- [ ] IP fija o reserva DHCP en el router del aula.
- [ ] Puerto `5000` permitido en la red del aula.
- [ ] Las otras notebooks y el televisor en la misma red.
- [ ] Reloj y zona horaria de la notebook correctos: MySQL es la fuente de
      tiempo.
- [ ] `.env` con permisos `600`.
- [ ] Sin Internet: Bootstrap, audio, imágenes y gráficos son locales.

Si el televisor abre el ranking desde un navegador, la dirección es
`http://IP-DE-LA-NOTEBOOK:5000/ranking`. Conviene dejarlo en pantalla completa y
sin protector de pantalla.

## Criterios de aceptación

- [ ] La app levanta desde cero con `./scripts/feria.sh`.
- [ ] `/salud` responde `200` con `{"estado": "ok", "base": "ok"}`.
- [ ] `/admin` entra con `ADMIN_USER` y la clave real.
- [ ] El contenido está congelado y anotado: `5/14/80/240/9`.
- [ ] `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` son reales y no están
      versionados.
- [ ] El `.env` tiene permisos `600` y no está en Git.
- [ ] `feria2026/` no está en Git y el script no reinstala si ya está todo.
- [ ] El backup se restaura en una base limpia y los conteos coinciden.
- [ ] Los scripts de backup y restauración funcionan.
- [ ] Sin Internet, todo sigue funcionando.
- [ ] La app responde en `0.0.0.0:5000` y se abre desde otra notebook.
- [ ] 3 notebooks juegan a la vez sin errores.
- [ ] El televisor muestra `/ranking` actualizándose.
- [ ] La terminal del servidor queda abierta y visible.

## Verificación

### 1. Arranque

```bash
./scripts/feria.sh
```

En otra terminal:

```bash
curl -i http://127.0.0.1:5000/salud
IP="$(hostname -I | awk '{print $1}')"
curl -i "http://$IP:5000/salud"
```

Los dos deben responder `200`.

### 2. Backup y restauración

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

### 3. Simulacro de feria

1. Levantar la app con `./scripts/feria.sh` en la notebook.
2. Conectar 3 notebooks y un televisor a la misma red.
3. Jugar con 3 equipos a la vez, uno por nivel si se puede.
4. Cortar Internet y repetir una estación.
5. Reiniciar MySQL y confirmar que la app se reconecta.
6. Restaurar el backup en una base limpia.
7. Cronometrar el arranque desde cero con `./scripts/feria.sh`.
8. Confirmar que el ranking del televisor se actualiza solo.

## Día de la feria

Orden recomendado:

1. Encender la notebook y conectarla a la red del aula.
2. Verificar que MySQL esté corriendo.
3. Ejecutar `./scripts/feria.sh`.
4. Abrir `/ranking` en el televisor y dejarlo en pantalla completa.
5. Hacer una partida corta de prueba y borrarla no hace falta: queda como
   intento del equipo de prueba.
6. Anotar la IP y la hora de inicio.
7. No tocar código, seeds ni configuración durante la feria.
8. Si algo falla, cerrar y volver a ejecutar `./scripts/feria.sh`. La base queda
   intacta.

Antes de cerrar el día:

```bash
./scripts/backup.sh /ruta/segura/backups-escaperoom
```

## Trampas conocidas

- El backup no está probado hasta que se restaura.
- Guardar el backup en un pendrive y en la nube, no solo en la notebook.
- `mysqldump --databases` incluye `CREATE DATABASE` y `USE`; los scripts no lo
  usan a propósito.
- No reemplazar el arranque de la feria por waitress ni por Docker.
- No hacer cambios de código el día de la feria.
- Verificar que el audio y Bootstrap sean locales; un CDN que falla deja la
  pantalla rota.
- El reloj de la notebook es la fuente de tiempo: revisarlo.
- Una IP por DHCP puede cambiar entre el ensayo y la feria.
- Cerrar la terminal corta el servidor: dejarla abierta.
- Si `python3 -m venv feria2026` falla, instalar `python3-venv` con `sudo apt
  install python3-venv` y volver a ejecutar el script.
- No restaurar sobre la base real sin backup previo y sin `--force` consciente.
- No commitear `.env`, `feria2026/` ni volcados.

## Al terminar

- Resumir qué se probó, en qué notebooks y con qué resultados.
- Anotar la fecha de congelamiento, la IP de la notebook y los niveles
  habilitados.
- Actualizar `README.md` y `MEMORY.md` con el arranque de la feria.
- Commit: `docs: feria con flask y respaldo`.
