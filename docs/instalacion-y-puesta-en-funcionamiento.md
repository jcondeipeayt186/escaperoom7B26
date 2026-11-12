# Instalación y puesta en funcionamiento

Guía para dejar la aplicación del **Escape Room 7.º B 2026** funcionando en un
servidor **Ubuntu** y usarla desde las notebooks conectadas a la misma red.

> Estado: la aplicación Flask **ya está implementada**. Esta guía queda para la
> puesta en marcha del servidor (paso 12) y se puede seguir completa.
>
> **Alcance:** cubre el **escenario A**, con Flask, waitress y MySQL en la misma
> notebook Ubuntu. Para el servidor Linux de la escuela y para la variante con
> la base remota, ver `docs/instalacion-servidor-escuela.md` y el resumen de
> escenarios del `paso12`.

## Contenido

- [1. Cómo queda armado](#1-cómo-queda-armado)
- [2. Requisitos](#2-requisitos)
- [3. Preparar el servidor Ubuntu](#3-preparar-el-servidor-ubuntu)
- [4. Instalar la aplicación](#4-instalar-la-aplicación)
- [5. Configurar la base de datos](#5-configurar-la-base-de-datos)
- [6. Probar la aplicación a mano](#6-probar-la-aplicación-a-mano)
- [7. Dejarla como servicio](#7-dejarla-como-servicio)
- [8. Red y acceso desde las notebooks](#8-red-y-acceso-desde-las-notebooks)
- [9. Uso desde las notebooks](#9-uso-desde-las-notebooks)
- [10. Operación y mantenimiento](#10-operación-y-mantenimiento)
- [11. Seguridad mínima](#11-seguridad-mínima)
- [12. Problemas frecuentes](#12-problemas-frecuentes)
- [13. Si el servidor es una notebook personal](#13-si-el-servidor-es-una-notebook-personal)
- [14. Checklist de instalación](#14-checklist-de-instalación)
- [15. Checklist del día de la feria](#15-checklist-del-día-de-la-feria)

---

## 1. Cómo queda armado

```text
Router / red del aula
├── Servidor Ubuntu
│   ├── MySQL 8 (solo escucha en localhost)
│   └── Flask + waitress en el puerto 8000
├── Notebook 1 → navegador → http://IP-DEL-SERVIDOR:8000
├── Notebook 2 → navegador → http://IP-DEL-SERVIDOR:8000
├── Notebook 3 → navegador → http://IP-DEL-SERVIDOR:8000
└── Televisor   → navegador → http://IP-DEL-SERVIDOR:8000/ranking
```

Ideas clave:

- **Las notebooks no instalan nada.** Solo abren el navegador.
- **El servidor es la autoridad.** Guarda el estado, valida las respuestas y calcula los tiempos.
- **MySQL no se expone a la red.** La app lo consulta desde el mismo servidor.
- **Todo funciona sin Internet.** Solo hace falta la red local del aula.

### Elegir escenario

| Escenario | Dónde corre la app | Dónde corre MySQL | Guía |
| --- | --- | --- | --- |
| **A** | Notebook Ubuntu | Notebook Ubuntu | Este documento |
| **B** | Servidor de la escuela | Servidor de la escuela | `docs/instalacion-servidor-escuela.md` |
| **C** | Notebook Ubuntu | Servidor de la escuela | `docs/instalacion-servidor-escuela.md` |

La recomendación es **A como principal** y **B como respaldo**. El escenario C
solo se usa si se ensayó antes: depende de la red entre la app y la base.

---

## 2. Requisitos

### Servidor

- Ubuntu **24.04 LTS** (recomendado) o 22.04 LTS.
- 2 GB de RAM como mínimo; 4 GB si también se usa como notebook de trabajo.
- 10 GB de disco libre.
- Conexión por cable al router del aula, si es posible.
- IP fija o reserva DHCP.
- Acceso por SSH o teclado y monitor.

> Si el servidor va a ser una **notebook personal**, por ejemplo la del docente, revisar además la sección [13](#13-si-el-servidor-es-una-notebook-personal): energía, tapa, red, actualizaciones automáticas y plan B.

### Notebooks

- Navegador actualizado: Chrome, Chromium, Edge o Firefox.
- Conexión a la misma red que el servidor.
- Nada más: ni Python, ni MySQL, ni la aplicación.

### Televisor

- Un navegador que abra `http://IP-DEL-SERVIDOR:8000/ranking`.
- Pantalla completa y suspensión desactivada.

### Software del servidor

| Programa | Para qué |
| --- | --- |
| `python3`, `python3-venv`, `python3-pip` | Ejecutar la app y crear el entorno virtual. |
| `mysql-server` | Base de datos. |
| `git` | Traer o actualizar el código. |
| `waitress` | Servidor de la app en la feria (se instala con `pip`). |
| `ufw` | Firewall del servidor. |

No hace falta PHP, Apache, Nginx, Docker ni Node.js.

---

## 3. Preparar el servidor Ubuntu

### 3.1 Actualizar el sistema y la zona horaria

```bash
sudo apt update
sudo apt upgrade -y

sudo timedatectl set-timezone America/Argentina/Buenos_Aires
timedatectl
```

La zona horaria importa: los tiempos del juego y el ranking se calculan con las fechas del servidor.

### 3.2 Instalar los paquetes

```bash
sudo apt install -y python3 python3-venv python3-pip mysql-server git ufw
```

Verificar:

```bash
python3 --version
mysql --version
git --version
```

### 3.3 Asegurar MySQL

```bash
sudo systemctl enable --now mysql
sudo systemctl status mysql --no-pager
sudo mysql_secure_installation
```

En `mysql_secure_installation` conviene:

- Definir una clave fuerte para `root`.
- Eliminar usuarios anónimos.
- No permitir el login remoto de `root`.
- Eliminar la base de prueba.
- Recargar privilegios.

Verificar que MySQL escuche solo en localhost:

```bash
sudo ss -tlnp | grep 3306
```

Debería mostrar `127.0.0.1:3306`. Si muestra `0.0.0.0:3306`, revisar `/etc/mysql/mysql.conf.d/mysqld.cnf` y dejar:

```ini
bind-address = 127.0.0.1
```

Después:

```bash
sudo systemctl restart mysql
```

> **Escenario C:** si MySQL va a quedar en el servidor de la escuela y la app en
> la notebook, `bind-address` debe escuchar en la LAN y hay que crear un
> usuario para la IP de la notebook. No seguir esa variante sin leer
> `docs/instalacion-servidor-escuela.md`, sección 5.

### 3.4 Desactivar la suspensión del servidor

Si el servidor es una notebook, tiene que quedar despierto durante toda la feria.

En Ubuntu con escritorio: **Configuración → Energía → Suspender: Nunca**.

En un servidor sin escritorio:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

Para revertirlo:

```bash
sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

---

## 4. Instalar la aplicación

### 4.1 Copiar el proyecto

Destino recomendado: `/opt/escape-room-7b2026`.

```bash
sudo mkdir -p /opt/escape-room-7b2026
sudo chown "$USER":"$USER" /opt/escape-room-7b2026
```

Con Git:

```bash
git clone <URL-DEL-REPOSITORIO> /opt/escape-room-7b2026
```

Desde un pendrive o copia local:

```bash
rsync -av /ruta/al/proyecto/ /opt/escape-room-7b2026/
```

### 4.2 Crear el usuario del servicio

La app no debería correr como `root`. Se crea un usuario de sistema sin login:

```bash
sudo useradd --system --home /opt/escape-room-7b2026 \
  --shell /usr/sbin/nologin escaperoom
```

Si el usuario ya existe, omitir este paso.

### 4.3 Crear el entorno virtual e instalar dependencias

```bash
cd /opt/escape-room-7b2026
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

El `requirements.txt` previsto incluye Flask, PyMySQL, python-dotenv, waitress y pytest.

> **MySQL 8 y PyMySQL:** MySQL 8 usa `caching_sha2_password` por defecto. Para ese método, PyMySQL necesita el extra `rsa`, que instala `cryptography`. Si el `requirements.txt` usa `PyMySQL` a secas, cambiarlo a `PyMySQL[rsa]` o ejecutar `pip install "PyMySQL[rsa]"`. Es la única dependencia extra que puede pedir MySQL 8; consultarlo antes de fijarla en el proyecto.

### 4.4 Crear el archivo `.env`

```bash
cd /opt/escape-room-7b2026
cp .env.example .env
```

Generar la clave de Flask:

```bash
source .venv/bin/activate
python -c "import secrets; print(secrets.token_hex(32))"
```

Generar el hash de la clave del admin:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"
```

Editar `.env`:

```bash
nano .env
```

Contenido de ejemplo:

```dotenv
FLASK_SECRET_KEY=la-clave-generada
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=escaperoom
MYSQL_PASSWORD=una-clave-larga-y-propia
MYSQL_DB=escape_room_7b2026
ADMIN_USER=admin
ADMIN_PASSWORD_HASH=el-hash-generado
```

Si la clave de MySQL tiene espacios o caracteres como `#`, `$`, `!` o comillas, escribirla **entre comillas dobles**:

```dotenv
MYSQL_PASSWORD="una clave con espacios y #"
```

El `.env` se lee tanto por `python-dotenv` como por `systemd` (`EnvironmentFile`). Sin comillas, un `#` puede cortar el valor y un espacio puede separarlo. La misma clave, con comillas simples, va en el `CREATE USER` de 5.2.

Permisos:

```bash
chmod 600 .env
```

No commitear `.env`. El archivo `.env.example` se versiona sin valores reales.

### 4.5 Ajustar permisos del proyecto

```bash
sudo chown -R escaperoom:escaperoom /opt/escape-room-7b2026
sudo chmod 755 /opt/escape-room-7b2026
```

El usuario `escaperoom` necesita leer el código, ejecutar `.venv` y leer `.env`. El `.env` queda con permisos `600`; el resto del proyecto puede quedar con lectura para otros usuarios del servidor, pero sin escritura.

---

## 5. Configurar la base de datos

### 5.1 Crear la base y las tablas

Como `root` de MySQL:

```bash
cd /opt/escape-room-7b2026
sudo mysql < bd/schema.sql
```

Esto crea la base `escape_room_7b2026` y las 12 tablas.

### 5.2 Crear el usuario de la aplicación

```bash
sudo mysql
```

```sql
CREATE USER 'escaperoom'@'localhost'
  IDENTIFIED BY 'una-clave-larga-y-propia';
CREATE USER 'escaperoom'@'127.0.0.1'
  IDENTIFIED BY 'una-clave-larga-y-propia';

GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'127.0.0.1';

-- Permisos para la base de los tests automatizados.
GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'127.0.0.1';

-- Permisos para las bases temporales que crea scripts/restaurar.sh.
GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'127.0.0.1';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'escaperoom'@'localhost';
SHOW GRANTS FOR 'escaperoom'@'127.0.0.1';
EXIT;
```

Se crean **dos cuentas con la misma clave**: `'escaperoom'@'localhost'` para el cliente `mysql` por socket y `'escaperoom'@'127.0.0.1'` para la app, que se conecta por TCP. Si solo se crea la de `localhost`, la conexión puede fallar según cómo resuelva el nombre el servidor MySQL.

Los permisos sobre `escape_room_7b2026_test` y `escape_room_7b2026_restore_%`
son solo para `pytest` y `scripts/restaurar.sh`; no cambian el acceso del
juego. La base real sigue siendo `escape_room_7b2026`.

Usar la misma clave que `MYSQL_PASSWORD` en `.env`. Si la clave tiene espacios, `#`, `$`, comillas o barras, escribirla entre comillas simples en el SQL y entre comillas dobles en `.env` (ver 4.4).

> Si PyMySQL no puede autenticarse con `caching_sha2_password`, se puede crear el usuario con `IDENTIFIED WITH mysql_native_password BY '...'`. Ese plugin está deprecado y no existe en MySQL 8.4 o superior, así que la opción recomendada es instalar `PyMySQL[rsa]`.

### 5.3 Cargar el contenido

```bash
mysql -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

Para cargar **estructura y contenido de una sola vez**:

```bash
mysql -u escaperoom -p < bd/escape_room_7b2026_completa.sql
```

Ese archivo crea las tablas, carga el contenido, habilita los tres niveles y no
trae historial de partidas. **Elimina y vuelve a crear las 12 tablas**, así que
no usarlo sobre una base con partidas sin backup.

Los seeds son **idempotentes**: se pueden ejecutar dos veces sin duplicar filas. Al reejecutarlos se actualizan los textos de preguntas, opciones y descripciones, así que pisan lo que se haya editado desde `/admin`.

### 5.4 Verificar

```bash
mysql -u escaperoom -p -e "
USE escape_room_7b2026;
SELECT 'estaciones' AS tabla, COUNT(*) AS filas FROM estacion
UNION ALL SELECT 'temas', COUNT(*) FROM tema
UNION ALL SELECT 'preguntas', COUNT(*) FROM pregunta
UNION ALL SELECT 'respuestas', COUNT(*) FROM respuesta
UNION ALL SELECT 'configuracion', COUNT(*) FROM configuracion;"
```

Resultado esperado:

| Tabla | Filas |
| --- | --- |
| `estacion` | 5 |
| `tema` | 14 |
| `pregunta` | 80 |
| `respuesta` | 240 |
| `configuracion` | 9 |

---

## 6. Probar la aplicación a mano

Antes de dejarla como servicio, conviene probarla en primer plano.

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom .venv/bin/waitress-serve \
  --call --listen=0.0.0.0:8000 app:create_app
```

En otra terminal del servidor:

```bash
curl http://127.0.0.1:8000/salud
```

Si `/salud` responde bien, probar desde una notebook:

```text
http://IP-DEL-SERVIDOR:8000
```

Para detener la prueba, `Ctrl+C`.

> Para desarrollo se puede usar `flask --app app run --host=0.0.0.0 --debug`, pero **no** para la feria.

---

## 7. Dejarla como servicio

Así arranca sola cuando se enciende el servidor y se reinicia si se cae.

### 7.1 Crear el archivo de servicio

```bash
sudo nano /etc/systemd/system/escape-room.service
```

Contenido:

```ini
[Unit]
Description=Escape Room 7.º B 2026
After=network-online.target mysql.service
Wants=network-online.target

[Service]
Type=simple
User=escaperoom
Group=escaperoom
WorkingDirectory=/opt/escape-room-7b2026
EnvironmentFile=/opt/escape-room-7b2026/.env
ExecStart=/opt/escape-room-7b2026/.venv/bin/waitress-serve --call --listen=0.0.0.0:8000 app:create_app
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 7.2 Activarlo

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now escape-room
sudo systemctl status escape-room --no-pager
```

Ver logs:

```bash
journalctl -u escape-room -f
```

Reiniciar después de un cambio:

```bash
sudo systemctl restart escape-room
```

Detener:

```bash
sudo systemctl stop escape-room
```

### 7.3 Verificar que escucha en la red

```bash
sudo ss -tlnp | grep 8000
curl http://127.0.0.1:8000/
```

Debe aparecer `0.0.0.0:8000` o `*:8000`. Si aparece solo `127.0.0.1:8000`, las notebooks no van a poder entrar.

---

## 8. Red y acceso desde las notebooks

### 8.1 Averiguar la IP del servidor

```bash
hostname -I
ip -4 addr show
```

Ejemplo: `192.168.1.50`. Esa es la dirección que se escribe en las notebooks.

### 8.2 Dejar la IP fija

La forma más segura es **reservar la IP desde el router** usando la MAC del servidor. Así el servidor siempre recibe la misma dirección sin tocar su configuración.

Si no se puede reservar desde el router, se puede configurar una IP fija con Netplan. Antes de aplicar, probar con `sudo netplan try` para no quedarse sin red:

```yaml
# /etc/netplan/50-static.yaml (ejemplo; ajustar interfaz, IP y gateway)
network:
  version: 2
  ethernets:
    enp3s0:
      dhcp4: no
      addresses: [192.168.1.50/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [192.168.1.1]
```

```bash
sudo netplan try
sudo netplan apply
```

No copiar el ejemplo sin revisar el nombre de la interfaz (`ip link`) y la red real.

> **Cuidado con los archivos que ya existen.** Ubuntu suele traer `/etc/netplan/50-cloud-init.yaml` o `00-installer-config.yaml`. Si ya hay un archivo que configura la misma interfaz, agregar otro puede dar un error de YAML duplicado o dejar la red a medias. Revisar primero con `ls /etc/netplan/` y editar ese archivo en lugar de crear uno nuevo. Si el servidor usa `cloud-init`, conviene desactivar la gestión de red de cloud-init antes de aplicar cambios propios.

Si después de aplicar no hay red, reiniciar el servidor y entrar por consola; `netplan try` revierte solo si nadie confirma en 120 segundos.

### 8.3 Abrir el puerto en el firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
sudo ufw enable
sudo ufw status verbose
```

Reemplazar `192.168.1.0/24` por la red del aula. Se puede ver con:

```bash
ip -4 addr show
```

No abrir el puerto `3306`: MySQL solo se usa desde el servidor. La única
excepción es el escenario C (base en el servidor de la escuela y app en la
notebook), y en ese caso se abre **solo para la IP de la notebook**, nunca para
toda la red. Ver `docs/instalacion-servidor-escuela.md`, sección 5.

### 8.4 Probar desde una notebook

1. Conectarse a la misma red Wi-Fi o al mismo switch.
2. Abrir el navegador.
3. Entrar a:

```text
http://192.168.1.50:8000
```

Si no carga:

- Hacer `ping 192.168.1.50` desde la notebook. Si el ping no responde, probar igual en el navegador: algunos routers o firewalls bloquean ICMP aunque el HTTP funcione.
- Verificar que el servidor y la notebook estén en la misma subred.
- Revisar `sudo ufw status`.
- Revisar `sudo ss -tlnp | grep 8000`.
- Confirmar que la red Wi-Fi no tenga **aislamiento de clientes** activado.
- No usar `localhost` en la notebook: `localhost` es la notebook, no el servidor.

### 8.5 Televisor

Abrir:

```text
http://192.168.1.50:8000/ranking
```

Recomendaciones:

- Pantalla completa (`F11`).
- Desactivar el protector de pantalla y la suspensión.
- Zoom al 125 % o 150 % si no se lee a distancia.
- No cerrar la pestaña durante la feria.
- La vista muestra una tabla por nivel y se actualiza sola cada 8 segundos.

Opcional, si el televisor tiene Chromium:

```bash
chromium --kiosk --noerrdialogs --disable-infobars \
  http://192.168.1.50:8000/ranking
```

---

## 9. Uso desde las notebooks

Las notebooks **no necesitan instalar nada**. El flujo es:

1. Abrir el navegador en `http://IP-DEL-SERVIDOR:8000`.
2. Completar **nombre del equipo**, **cantidad de integrantes** (1 a 4) y **dificultad**.
3. Presionar **Iniciar misión**.
4. Anotar el **ID del equipo** que aparece en el HUD.
5. Jugar las 5 estaciones en orden.
6. Usar **Ayuda 1** y **Ayuda 2** si hace falta; las pistas se leen en papel.
7. Enviar las respuestas de cada estación.
8. Al completar el recorrido, ver el resultado y el ranking.

Reglas prácticas:

- **Una notebook por equipo.** Evitar dos pestañas del mismo equipo enviando respuestas.
- **No borrar las cookies** durante la feria: la sesión mantiene el intento.
- Si se cierra el navegador, volver a entrar con el **mismo nombre** y el **ID del equipo**.
- Si el equipo ya tenía un intento activo, la app lo reanuda.
- El audio de los 30 segundos se desbloquea con la primera interacción (clic o tecla) dentro de la estación. Si el navegador lo bloquea, el aviso visual funciona igual.
- No recargar justo después de enviar: esperar la transición.
- El ranking del televisor se actualiza solo; no hay que refrescarlo a mano.

### Administración

El panel está en:

```text
http://IP-DEL-SERVIDOR:8000/admin
```

- No está enlazado desde las pantallas públicas.
- Usa `ADMIN_USER` y `ADMIN_PASSWORD_HASH` de `.env`.
- Conviene entrar desde el servidor o desde una notebook de confianza.
- No compartir la clave con los equipos.

---

## 10. Operación y mantenimiento

### 10.1 Comandos del servicio

```bash
sudo systemctl start escape-room
sudo systemctl stop escape-room
sudo systemctl restart escape-room
sudo systemctl status escape-room --no-pager
journalctl -u escape-room -n 100 --no-pager
```

### 10.2 Actualizar el código

Antes de actualizar, hacer backup de la base.

```bash
sudo systemctl stop escape-room

cd /opt/escape-room-7b2026
sudo git pull
sudo .venv/bin/pip install -r requirements.txt
sudo chown -R escaperoom:escaperoom /opt/escape-room-7b2026

sudo systemctl start escape-room
```

- `sudo git pull` y `sudo .venv/bin/pip install` se usan porque el proyecto lo administra una cuenta distinta de `escaperoom`. Corren como `root` y dejan archivos con ese dueño.
- El `chown` final devuelve todo a `escaperoom`, que es el usuario con el que corre el servicio. Sin ese paso, la app puede quedar sin permiso para leer archivos nuevos o para escribir en `.venv`.
- No usar `sudo -u escaperoom git pull` si `.venv` ya quedó con archivos de `root`: el `pip install` fallaría por permisos.

Si el código se copia a mano, reemplazar los archivos y volver a ajustar permisos:

```bash
sudo chown -R escaperoom:escaperoom /opt/escape-room-7b2026
```

Si cambió el contenido, volver a ejecutar los seeds (son idempotentes):

```bash
mysql -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

### 10.3 Backup de la base

El proyecto incluye `scripts/backup.sh`, que hace lo mismo que los comandos de
esta sección y funciona igual en los escenarios A, B y C:

```bash
cd /opt/escape-room-7b2026
./scripts/backup.sh "$HOME/backups-escaperoom"
```

Para hacerlo a mano, guardar los respaldos **fuera de `/opt/escape-room-7b2026`**, por ejemplo en el home del usuario que administra el servidor. Así no se mezclan con el código ni se pierden si se reemplaza el proyecto.

```bash
mkdir -p "$HOME/backups-escaperoom"

mysqldump -u escaperoom -p \
  --single-transaction \
  --default-character-set=utf8mb4 \
  escape_room_7b2026 \
  > "$HOME/backups-escaperoom/respaldo-$(date +%Y%m%d-%H%M).sql"
```

El archivo queda en `/home/<usuario>/backups-escaperoom/`. Verificar que se creó y que no está vacío:

```bash
ls -lh "$HOME/backups-escaperoom"
```

Guardar una copia fuera del servidor: pendrive y, si hay Internet, almacenamiento en la nube.

### 10.4 Probar la restauración

No alcanza con generar el backup: hay que probar que se restaura. El script lo
hace sobre una base temporal y muestra los conteos:

```bash
cd /opt/escape-room-7b2026
./scripts/restaurar.sh "$HOME/backups-escaperoom/respaldo-AAAAMMDD-HHMM.sql"
```

También se puede hacer a mano:

```bash
sudo mysql -e "
  DROP DATABASE IF EXISTS escape_room_7b2026_restore;
  CREATE DATABASE escape_room_7b2026_restore
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

sudo mysql escape_room_7b2026_restore \
  < "$HOME/backups-escaperoom/respaldo-AAAAMMDD-HHMM.sql"

sudo mysql -e "
  USE escape_room_7b2026_restore;
  SELECT COUNT(*) AS estaciones FROM estacion;
  SELECT COUNT(*) AS preguntas FROM pregunta;"
```

La redirección `<` la resuelve la shell del usuario actual antes de llamar a `sudo`, así que el archivo tiene que ser legible por ese usuario (lo es, porque lo generó él mismo).

Cuando esté conforme, borrar la base de prueba:

```bash
sudo mysql -e "DROP DATABASE escape_room_7b2026_restore;"
```

### 10.5 Congelar el contenido antes de la feria

- Revisar preguntas, opciones y respuestas correctas.
- Revisar también las descripciones de `intermedio` y `avanzado`.
- Confirmar en `/admin/dificultades` qué niveles están habilitados y que la bienvenida los muestre. Al 12/11/2026 están habilitados `inicial`, `intermedio` y `avanzado`.
- Jugar una partida completa de `intermedio` y otra de `avanzado` para confirmar que entran al ranking de su nivel.
- Hacer un backup.
- No cargar contenido nuevo el día de la feria.
- No ejecutar `apt upgrade` el mismo día.

---

## 11. Seguridad mínima

- MySQL escucha solo en `127.0.0.1`. La única excepción es el escenario C, con
  `3306` abierto solo para la IP de la notebook.
- El puerto `3306` no se abre en el firewall, salvo la excepción restringida
  del escenario C.
- La app corre como `escaperoom`, no como `root`.
- `.env` tiene permisos `600` y no se versiona.
- La clave de admin es larga y se guarda como hash, nunca en texto plano.
- `/admin` no se enlaza desde las pantallas públicas.
- El servidor no se expone a Internet: la feria usa la red local.
- Si se instala phpMyAdmin, no exponerlo a Internet y protegerlo con clave.
- Mantener Ubuntu actualizado, pero **no** actualizar el día de la feria.
- Si se usa SSH, preferir claves y deshabilitar el login de `root` por contraseña.

Esta puesta en marcha no incluye HTTPS porque la red es local. Si más adelante se necesita, se puede agregar un proxy inverso con certificado; no es parte del stack actual.

---

## 12. Problemas frecuentes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| `curl: connection refused` en el servidor | El servicio está caído o escucha en otro puerto. | `sudo systemctl status escape-room`, `ss -tlnp \| grep 8000`. |
| En el servidor funciona, en la notebook no | Firewall, IP incorrecta o redes distintas. | `ufw status`, `ping`, revisar subred. |
| La notebook no hace ping al servidor | Wi-Fi con aislamiento de clientes, subred distinta o ICMP bloqueado. | Probar el navegador igual; si tampoco carga, desactivar aislamiento o usar la misma red. |
| `ModuleNotFoundError: No module named 'app'` | `WorkingDirectory` incorrecto. | Corregir el servicio y reiniciar. |
| `Access denied for user 'escaperoom'` | Clave incorrecta o usuario mal creado. | Revisar `.env`, `SHOW GRANTS` y que existan las cuentas `'escaperoom'@'localhost'` y `'escaperoom'@'127.0.0.1'`. |
| `Authentication plugin 'caching_sha2_password'` | Falta el extra `rsa` de PyMySQL. | `pip install "PyMySQL[rsa]"`. |
| `Table 'escape_room_7b2026.estacion' doesn't exist` | No se ejecutó `schema.sql`. | Cargar el esquema y el seed. |
| `Address already in use` | Otro proceso usa el puerto 8000. | `sudo ss -tlnp \| grep 8000`, detener el proceso. |
| El tiempo no coincide | Zona horaria distinta. | `timedatectl`, reiniciar MySQL y la app. |
| El audio no suena | El navegador bloqueó el audio. | Tocar o presionar una tecla dentro de la estación antes del aviso; el aviso visual igual funciona. |
| El ranking no se actualiza | Error de JavaScript o `/ranking/datos`. | Abrir la consola del navegador y revisar la ruta. |
| `502` o la app no responde | MySQL caído o credenciales mal. | `systemctl status mysql`, `journalctl -u escape-room`. |
| El seed duplica datos | Se modificó el seed o los ids fijos. | Usar el seed original idempotente. |
| `Permission denied` al leer `.env` | El usuario del servicio no tiene permisos. | `chown escaperoom:escaperoom .env`, `chmod 600`. |

---

## 13. Si el servidor es una notebook personal

Es perfectamente válido usar una notebook personal como servidor, por ejemplo la del docente. La aplicación es liviana: con 4 GB de RAM alcanza para MySQL, waitress, tres equipos jugando y el televisor. No hace falta un servidor dedicado.

Pero una notebook **no se comporta como un servidor**: se suspende, se cierra la tapa, cambia de red, se usa para otras cosas y se actualiza sola. Esta sección cubre esas diferencias. El resto de la guía se aplica igual.

### 13.1 Qué cambia respecto de un servidor dedicado

| Situación | Qué pasa | Qué hacer |
| --- | --- | --- |
| Se suspende por inactividad o al cerrar la tapa | La app y MySQL dejan de responder; los equipos pierden el intento en curso. | Desactivar suspensión e hibernación (13.2). |
| Cambia de red entre la casa y la escuela | Cambia la IP y las notebooks no encuentran el servidor. | Reservar la IP en el router de la escuela o anotar la nueva (13.3). |
| Se usa para otras tareas | Menos memoria y CPU, ventanas que consumen batería, sincronización de archivos. | Cerrar programas pesados y dedicarla durante la feria (13.5). |
| Se actualiza sola | `unattended-upgrades` o `snap` pueden reiniciar servicios en medio del juego. | Actualizar antes y pausar las actualizaciones durante la feria (13.6). |
| Es un único equipo | Si falla, no hay servicio ni base. | Backup en pendrive y plan B probado (13.7). |
| Está enchufada | La batería funciona como UPS ante un corte breve. | Dejarla enchufada todo el tiempo (13.2). |

### 13.2 Energía, tapa y pantalla

**Enchufada siempre.** La batería actúa como UPS: si se corta la luz un momento, la app sigue. No confiar en ella para cortes largos; el router también se apaga y las notebooks pierden la red.

**Desactivar la suspensión.** Desde la interfaz: **Configuración → Energía → Suspender: Nunca** y **Apagar pantalla: Nunca**. En Ubuntu con GNOME, desde una terminal del escritorio:

```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
gsettings set org.gnome.desktop.session idle-delay 0
```

Estos comandos se ejecutan en la sesión gráfica del usuario de la notebook, no por SSH.

**Cerrar la tapa no debe suspender.** Editar `/etc/systemd/logind.conf`:

```ini
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

```bash
sudo systemctl restart systemd-logind
```

Reiniciar `systemd-logind` puede cerrar la sesión gráfica. Es más seguro reiniciar la notebook después del cambio.

> Si la tapa queda cerrada, la notebook tiene que estar **ventilada y sobre una superficie dura**. Adentro de una mochila se recalienta y se apaga. Lo más simple es dejarla abierta y con la pantalla apagada.

**Modo de ahorro de energía:** desactivarlo. Baja la frecuencia del procesador y puede dormir la placa Wi-Fi. En GNOME se elige **Rendimiento** o **Equilibrado**, nunca **Ahorro de energía**, durante la feria.

**Bloquear la pantalla no es suspender.** El servicio `escape-room` corre con systemd y sigue funcionando aunque la sesión esté bloqueada o el usuario cierre sesión. Lo que corta el juego es **suspender, hibernar o apagar**.

### 13.3 Red

**Preferir cable.** Es más estable que el Wi-Fi del aula y no sufre ahorro de energía ni roaming entre access points. Si solo hay Wi-Fi, conectarse a la misma red que las notebooks y confirmar que no tenga **aislamiento de clientes**.

**Desactivar el ahorro de energía del Wi-Fi.** Con NetworkManager:

```ini
# /etc/NetworkManager/conf.d/wifi-powersave-off.conf
[connection]
wifi.powersave = 2
```

```bash
sudo systemctl restart NetworkManager
```

`2` significa desactivado. El reinicio corta la red unos segundos; hacerlo antes de la feria. También se puede probar con `iw`:

```bash
iw dev wlan0 get power_save
sudo iw dev wlan0 set power_save off
```

El nombre de la interfaz puede ser `wlan0`, `wlp2s0` u otro; se ve con `ip link`. El cambio con `iw` no siempre sobrevive a un reinicio; la configuración de NetworkManager sí.

**IP estable.** Reservar la IP por MAC en el router de la escuela. Si la notebook también se usa en la casa, la IP va a cambiar al volver a la escuela si no hay reserva. Anotar la IP del día y actualizar los accesos de las notebooks y del televisor.

**Nombre de host.** `http://nombre-de-la-notebook.local:8000` puede funcionar con `avahi-daemon`, pero no es confiable desde notebooks con Windows. Para la feria, usar la IP.

**VPN.** Si la notebook tiene una VPN activa, puede desviar el tráfico de la red local y romper el acceso. Verificar con:

```bash
nmcli connection show --active
```

y desconectar la VPN antes de la feria.

**No convertir la notebook en hotspot** salvo que sea una decisión planificada. Si se usa el hotspot de la propia notebook, los equipos se conectan a ella y cambian las reglas de firewall y la IP; es otro esquema de red, no el de esta guía.

**Cambios de subred.** Si la escuela cambia la red (por ejemplo, de `192.168.1.0/24` a `192.168.0.0/24`), hay que actualizar la regla de `ufw` y la IP anotada.

### 13.4 Reloj, hora y zona horaria

El servidor es la autoridad del tiempo: de su reloj salen el contador general, el de estación y el ranking. Si la notebook no tiene Internet, no puede sincronizar por NTP.

Antes de la feria:

```bash
timedatectl
```

Verificar que la hora coincida con un teléfono y que la zona sea `America/Argentina/Buenos_Aires`. Si está mal:

```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

No cambiar la hora ni la zona **durante** el juego: los tiempos ya registrados saltarían y el ranking quedaría raro. Tampoco hace falta apagar NTP si no hay Internet; el intento de sincronización falla sin consecuencias.

### 13.5 Uso durante la feria

**Dedicarla al juego.** Cerrar programas pesados, muchas pestañas del navegador, editores de video, juegos y clientes de sincronización (ownCloud, Nextcloud, Dropbox, Google Drive). La sincronización puede consumir red y bloquear archivos justo cuando se está escribiendo en la base.

> El proyecto se instala en `/opt/escape-room-7b2026`, **fuera** de la carpeta sincronizada. No ejecutar la app desde una carpeta de ownCloud: el cliente puede mover o bloquear archivos mientras corre.

**Si la notebook también es una estación de juego**, no hay problema: el navegador de esa notebook se conecta al mismo servidor. Pero conviene usar un **perfil de navegador distinto** para `/admin` o cerrar la sesión de administración antes de que un equipo use esa notebook. La cookie de admin no debe quedar abierta en una pantalla que usan los estudiantes.

**No apagar ni cerrar la tapa mientras hay equipos jugando.** Si hay que moverla, detener el servicio primero:

```bash
sudo systemctl stop escape-room
```

y volver a arrancarlo cuando esté conectada.

**No desconectar el cable de red ni cambiar de Wi-Fi** en medio de una estación. Los equipos pierden el envío en curso.

**Sonido.** El audio de los 30 segundos lo reproduce el navegador de cada equipo, no el servidor. Si la notebook del docente es también una estación, su audio sale por sus propios parlantes.

**Rendimiento.** MySQL y waitress consumen poco. Si la notebook tiene 4 GB o más, el límite no es la app sino las otras cosas que se abran. Con 2 GB, cerrar todo lo que no sea el navegador.

### 13.6 Actualizaciones automáticas y software

Ubuntu puede instalar actualizaciones y `snap` puede refrescar paquetes sin avisar. Un reinicio de servicio o del sistema en plena feria arruina el juego.

**Actualizar antes**, no el día de la feria. Durante la feria se puede pausar:

```bash
# Pausar los snaps (se libera con: snap refresh --unhold)
sudo snap refresh --hold

# Opcional: frenar las actualizaciones automáticas mientras dure la feria
sudo systemctl stop apt-daily-upgrade.timer
sudo systemctl stop unattended-upgrades
```

Al terminar, volver a habilitarlas:

```bash
sudo systemctl start apt-daily-upgrade.timer
sudo systemctl start unattended-upgrades
sudo snap refresh --unhold
```

No instalar programas nuevos ni actualizar el kernel durante la feria. No hace falta antivirus ni limpiadores en Ubuntu; si hay alguno instalado, no ejecutarlo en ese momento.

### 13.7 Respaldo y plan B

Una notebook personal es un **punto único de falla**: si se rompe, se pierde, se moja o no arranca, no hay juego.

- Hacer backup de la base antes de la feria y al terminar cada día (sección 10.3), y guardarlo en un pendrive **fuera** de la notebook.
- Tener una copia del proyecto (el repositorio o un ZIP) y del `.env` en un lugar seguro. El `.env` tiene claves: no va al repositorio, pero sí conviene una copia en un pendrive cifrado o en un gestor de contraseñas.
- El `.venv` **no es portable** entre máquinas: en la notebook de repuesto se recrea con `python3 -m venv .venv` y `pip install -r requirements.txt`.
- Probar la restauración (sección 10.4) antes de la feria, no el mismo día.
- Si es posible, tener otra notebook con Ubuntu ya preparada y el mismo procedimiento probado. No hace falta que esté encendida: alcanza con que pueda reemplazar a la principal en pocos minutos.
- Si el servidor de la escuela quedó preparado, usarlo como **plan B**: el procedimiento del escenario B está en `docs/instalacion-servidor-escuela.md`. Probar ese escenario antes de la feria, no el mismo día.
- Un UPS chico para el router ayuda a que un corte breve no saque a todos de la red.

### 13.8 Si la notebook tiene Windows

Esta guía asume **Ubuntu**. Si la notebook del docente tiene Windows, las opciones son:

1. Instalar Ubuntu (nativo o en dual boot) y seguir esta guía.
2. Usar una máquina virtual con **red en modo puente** (*bridged*), de modo que tenga su propia IP en la red del aula.

**WSL2 no es recomendable para servir a la LAN**: por defecto usa NAT y las otras notebooks no llegan a la app sin configuraciones adicionales de red y firewall. El stack en sí es el mismo (Python, Flask, MySQL), pero los comandos de systemd, `ufw` y rutas de esta guía no aplican en Windows. Si se opta por Windows nativo, queda fuera del alcance de este documento.

### 13.9 Checklist de la notebook como servidor

- [ ] Enchufada a la corriente y con batería cargada.
- [ ] Suspensión, hibernación y apagado de pantalla desactivados.
- [ ] Cerrar la tapa no suspende (o se deja abierta y ventilada).
- [ ] Conectada por cable o por Wi-Fi estable, sin ahorro de energía.
- [ ] IP reservada en el router o anotada para el día.
- [ ] VPN desconectada.
- [ ] Hora y zona horaria verificadas contra un teléfono.
- [ ] Programas pesados y sincronización de carpetas cerrados.
- [ ] Actualizaciones y `snap` en pausa durante la feria.
- [ ] `/admin` cerrado en el navegador que usan los equipos.
- [ ] Backup en pendrive y restauración probada.
- [ ] Cargador de repuesto y, si se puede, notebook de repuesto preparada.

---

## 14. Checklist de instalación

- [ ] Ubuntu actualizado y con zona horaria `America/Argentina/Buenos_Aires`.
- [ ] `python3`, `python3-venv`, `python3-pip`, `mysql-server`, `git` y `ufw` instalados.
- [ ] MySQL corriendo y escuchando solo en `127.0.0.1:3306` (escenario A).
- [ ] Base `escape_room_7b2026` creada con `bd/schema.sql`.
- [ ] Usuario `escaperoom` con permisos sobre la base real, la de test y las temporales de restauración, en `'localhost'` y en `'127.0.0.1'`.
- [ ] Seeds `001`, `002` y `003` ejecutados y conteos verificados (5/14/80/240/9).
- [ ] Dificultades habilitadas revisadas en `/admin/dificultades`.
- [ ] Proyecto copiado en `/opt/escape-room-7b2026`.
- [ ] `.venv` creado y `requirements.txt` instalado.
- [ ] `.env` con clave de Flask, clave de MySQL y hash del admin.
- [ ] `.env` con permisos `600` y dueño `escaperoom`.
- [ ] Servicio `escape-room` activo y habilitado al arranque.
- [ ] `/salud` responde desde el servidor.
- [ ] `/` responde desde una notebook.
- [ ] Puerto `8000` abierto solo para la red local.
- [ ] IP del servidor fija o reservada.
- [ ] Suspensión del servidor desactivada.
- [ ] Backup generado y restauración probada.

---

## 15. Checklist del día de la feria

- [ ] Servidor encendido y conectado a la red.
- [ ] `sudo systemctl status escape-room` activo.
- [ ] `sudo systemctl status mysql` activo.
- [ ] Notebooks y televisor en la misma red.
- [ ] `/ranking` abierto en el televisor, en pantalla completa.
- [ ] Audio probado en una notebook.
- [ ] Un equipo de prueba completó una estación.
- [ ] El ID del equipo se ve en el HUD.
- [ ] Pistas impresas para los estudiantes.
- [ ] Backup del día anterior a mano.
- [ ] Cargadores y baterías.
- [ ] Nadie va a actualizar el sistema ni el contenido durante la feria.
