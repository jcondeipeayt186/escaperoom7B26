# Dejar funcionando el proyecto luego de clonarlo

Guía paso a paso para pasar de un repositorio recién clonado a la aplicación
funcionando en el navegador, en una máquina con **Ubuntu/Debian**. Cubre
MySQL, la base de datos, el entorno virtual de Python, el archivo `.env`, la
ejecución local, el recorrido de la app y, al final, cómo dejarla como servidor
para la feria.

> El **escenario principal** es la notebook Ubuntu con todo instalado. El
> **escenario B** (servidor Linux de la escuela) y el **C** (base remota) están
> en `docs/instalacion-servidor-escuela.md`. El detalle de waitress,
> systemd, firewall y operación durante la feria está en
> `docs/instalacion-y-puesta-en-funcionamiento.md`.

## Contenido

- [0. Antes de empezar](#0-antes-de-empezar)
- [1. Resumen rápido](#1-resumen-rápido)
- [2. Requisitos](#2-requisitos)
- [3. Instalar MySQL y Python](#3-instalar-mysql-y-python)
- [4. Clonar el proyecto](#4-clonar-el-proyecto)
- [5. Crear el entorno virtual de Python](#5-crear-el-entorno-virtual-de-python)
- [6. Crear el archivo .env](#6-crear-el-archivo-env)
- [7. Preparar la base de datos](#7-preparar-la-base-de-datos)
- [8. Levantar la aplicación](#8-levantar-la-aplicación)
- [9. Correr las pruebas automatizadas](#9-correr-las-pruebas-automatizadas)
- [10. Acceder desde otra máquina de la red](#10-acceder-desde-otra-máquina-de-la-red)
- [11. Dejarlo como servidor de la feria](#11-dejarlo-como-servidor-de-la-feria)
- [12. Problemas frecuentes](#12-problemas-frecuentes)
- [13. Checklist final](#13-checklist-final)

---

## 0. Antes de empezar

Qué se necesita:

- Una máquina con **Ubuntu 22.04 o 24.04** (o Debian reciente) y un usuario
  con `sudo`.
- **Conexión a Internet solo para instalar** paquetes y dependencias. Después
  la app funciona sin Internet.
- Alrededor de **1 GB libre** para Python, MySQL, el entorno virtual y la base.
- El **nombre o la URL del repositorio** que provee el docente. En esta guía
  aparece como `<URL-DEL-REPOSITORIO>`.

Convenciones:

- Todos los comandos se ejecutan **desde la raíz del proyecto**, donde están
  `requirements.txt`, `bd/` y `app/`.
- Los comandos que empiezan con `sudo` piden la clave del usuario de Linux.
- Los comandos con `mysql -u escaperoom -p` piden la clave **de MySQL** que se
  elige en la sección 7.2.
- Cada vez que se abre una terminal nueva hay que activar el entorno con
  `source .venv/bin/activate`.
- Si algo falla, la sección 12 tiene los errores más comunes.

---

## 1. Resumen rápido

Para quien ya tiene MySQL y Python instalados y solo quiere los comandos:

```bash
cd ruta/al/proyecto

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
chmod 600 .env
# Editar .env con los datos reales (ver sección 6)

sudo mysql < bd/schema.sql
sudo mysql < bd/seeds/001_contenido_inicial.sql
sudo mysql < bd/seeds/002_contenido_intermedio.sql
sudo mysql < bd/seeds/003_contenido_avanzado.sql
# Crear el usuario de la app (ver sección 7.2)

flask --app app run --debug
```

Abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) y comprobar [http://127.0.0.1:5000/salud](http://127.0.0.1:5000/salud).

---

## 2. Requisitos

- **Ubuntu 22.04 o 24.04** (también sirve Debian reciente).
- **Python 3.10 o superior** con `venv` y `pip`.
- **MySQL 8.0 o superior** (o MariaDB 10.3 o superior).
- **git** para clonar el repositorio.
- No hace falta Apache, Nginx, PHP, Docker ni Node.js.

Verificar lo que ya está instalado:

```bash
python3 --version
mysql --version
git --version
```

Los mínimos son **Python 3.10** (`pytest 9.2` no instala en 3.9) y **MySQL
8.0** (o MariaDB 10.3). Si `python3 --version` muestra 3.9 o menos, instalar
una versión más nueva antes de seguir. Si `mysql --version` muestra 5.7,
actualizar el motor: el ranking usa `ROW_NUMBER() OVER (...)`.

---

## 3. Instalar MySQL y Python

Actualizar el sistema e instalar los paquetes:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server git
```

Habilitar MySQL para que arranque con el sistema y verificar que esté activo:

```bash
sudo systemctl enable --now mysql
sudo systemctl status mysql --no-pager
```

La salida debe incluir `active (running)`. También se puede comprobar el puerto:

```bash
sudo ss -tlnp | grep 3306
```

Debe escuchar en `127.0.0.1:3306`. La aplicación se conecta desde la misma
máquina, así que MySQL **no** necesita estar expuesto a la red.

> En Ubuntu, el usuario `root` de MySQL suele entrar con `sudo mysql` sin
> contraseña (autenticación por socket). Es lo que usan los comandos de esta
> guía para crear la base y el usuario de la aplicación.

---

## 4. Clonar el proyecto

Elegir una carpeta de trabajo y clonar el repositorio desde GitHub:

```bash
git clone <URL-DEL-REPOSITORIO> escaperoom7B26
cd escaperoom7B26
```

La URL la provee el docente o figura en la página del repositorio (botón
**Code**). Si el proyecto llega como ZIP o copia desde un pendrive, alcanza con
descomprimirlo o copiarlo y entrar a la carpeta.

Los comandos siguientes se ejecutan siempre desde la raíz del proyecto, donde
están `requirements.txt`, `bd/` y `app/`. Para confirmar que se está en el
lugar correcto:

```bash
ls requirements.txt bd/schema.sql app/__init__.py
```

El `.env` y el entorno `.venv` **no vienen** en el repositorio: se crean en las
secciones 5 y 6.

---

## 5. Crear el entorno virtual de Python

El entorno virtual guarda las dependencias del proyecto sin mezclarlas con las
del sistema. Se crea una sola vez por máquina.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

El prompt debería mostrar `(.venv)` adelante. Para salir del entorno:

```bash
deactivate
```

Cada vez que se abra una terminal nueva hay que volver a activarlo:

```bash
source .venv/bin/activate
```

Dependencias que instala `requirements.txt`:


| Paquete         | Para qué                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `Flask`         | Framework web.                                                             |
| `PyMySQL[rsa]`  | Conexión a MySQL 8 (incluye `cryptography` para `caching_sha2_password`). |
| `python-dotenv` | Leer el archivo `.env`.                                                    |
| `pytest`        | Pruebas automatizadas.                                                     |
| `waitress`      | Servidor para la puesta en producción.                                    |

> El `.venv` **no es portable** entre máquinas: si se copia el proyecto a otra
> computadora, hay que volver a crear el entorno y reinstalar las dependencias.

---

## 6. Crear el archivo `.env`

El proyecto lee la configuración de un archivo `.env` en la raíz. Ese archivo
tiene claves, así que **no se versiona**. El repositorio incluye
`.env.example` como plantilla.

```bash
cp .env.example .env
chmod 600 .env
```

Los comandos `python` de esta sección se ejecutan **con el entorno virtual
activado** (`source .venv/bin/activate`), porque usan paquetes instalados por
`requirements.txt`.

Generar la clave de Flask:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generar el hash de la clave del panel de administración:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"
```

Reemplazar `CAMBIA-ESTA-CLAVE` por la clave real que se va a usar en `/admin`.
La salida es un hash largo: eso es lo que se pega en `.env`.

Editar el archivo:

```bash
nano .env
```

Variables que usa la aplicación:


| Variable              | Obligatoria          | Ejemplo              | Para qué                   |
| ----------------------- | ---------------------- | ---------------------- | ----------------------------- |
| `FLASK_SECRET_KEY`    | Sí                  | `3f9c...`            | Firma la sesión de Flask.  |
| `MYSQL_HOST`          | Sí                  | `127.0.0.1`          | Host de MySQL.              |
| `MYSQL_PORT`          | Sí                  | `3306`               | Puerto de MySQL.            |
| `MYSQL_USER`          | Sí                  | `escaperoom`         | Usuario de la base.         |
| `MYSQL_PASSWORD`      | No (puede ir vacía) | `una-clave-larga`    | Clave de ese usuario.       |
| `MYSQL_DB`            | Sí                  | `escape_room_7b2026` | Nombre de la base.          |
| `ADMIN_USER`          | Para `/admin`        | `admin`              | Usuario del panel.          |
| `ADMIN_PASSWORD_HASH` | Para `/admin`        | `scrypt:...`         | Hash de la clave del panel. |

Ejemplo de `.env` completo:

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

Reglas importantes:

- **No dejar** `FLASK_SECRET_KEY` con el valor de ejemplo: la aplicación se
  niega a arrancar si detecta `cambiar-por-una-clave-larga-y-aleatoria`.
- Si una clave tiene espacios o caracteres como `#`, `$`, `!` o comillas,
  escribirla **entre comillas dobles**:

  ```dotenv
  MYSQL_PASSWORD="una clave con espacios y #"
  ```
- `.env` debe quedar con permisos `600` y nunca subirse al repositorio.
- Si se cambia una clave, reiniciar el servidor de Flask para que la tome.

Opcional: los tests usan una base aparte. Por defecto es
`escape_room_7b2026_test`, pero se puede cambiar con `TEST_MYSQL_DB` (debe
terminar en `_test` y ser distinta de `MYSQL_DB`).

```dotenv
TEST_MYSQL_DB=escape_room_7b2026_test
```

---

## 7. Preparar la base de datos

### 7.1 Crear las tablas

El esquema crea la base `escape_room_7b2026` y las 12 tablas. Se ejecuta una
sola vez:

```bash
sudo mysql < bd/schema.sql
```

### 7.2 Crear el usuario de la aplicación

La aplicación no debería usar `root`. Se crea un usuario propio con permisos
solo sobre las bases del proyecto: la real, la de los tests y las temporales
que usa `scripts/restaurar.sh`. Entrar a MySQL como `root`:

```bash
sudo mysql
```

Ejecutar el siguiente SQL, cambiando `una-clave-larga-y-propia` por la misma
clave que se pone en `MYSQL_PASSWORD`:

```sql
CREATE USER 'escaperoom'@'localhost'
  IDENTIFIED BY 'una-clave-larga-y-propia';
CREATE USER 'escaperoom'@'127.0.0.1'
  IDENTIFIED BY 'una-clave-larga-y-propia';

GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'127.0.0.1';

-- Permisos para la base que usan los tests automatizados.
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
EXIT;
```

Se crean dos cuentas con la misma clave: `'escaperoom'@'localhost'` para el
cliente `mysql` por socket y `'escaperoom'@'127.0.0.1'` para la aplicación, que
se conecta por TCP. Si solo se crea una, la conexión puede fallar según cómo
resuelva el nombre MySQL.

> Si la clave tiene espacios, `#`, `$`, comillas o barras, escribirla entre
> comillas simples en el SQL y entre comillas dobles en `.env`.

> Si se cambia `TEST_MYSQL_DB`, otorgar los mismos permisos sobre esa base.

> El permiso `escape\_room\_7b2026\_restore\_%` lo usa `scripts/restaurar.sh`
> para crear una base temporal al probar un respaldo. No es la base real.

### 7.3 Cargar el contenido

Los tres seeds cargan las 5 estaciones, 14 temas, 80 preguntas (20 `inicial`,
30 `intermedio` y 30 `avanzado`), 240 respuestas y la configuración del juego.
Son **idempotentes**: se pueden ejecutar más de una vez sin duplicar filas.

```bash
mysql -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

Para cargar todo de una sola vez, con estructura, contenido y los tres niveles
habilitados:

```bash
mysql -u escaperoom -p < bd/escape_room_7b2026_completa.sql
```

Ese archivo elimina y vuelve a crear las 12 tablas, así que borra equipos e
intentos si la base ya se usó. Es una instantánea generada desde `bd/schema.sql`
y los seeds: si cambia el contenido, hay que regenerarla.

Cuando pida la clave, ingresar la misma de `MYSQL_PASSWORD`.

### 7.4 Verificar

```bash
mysql -u escaperoom -p -e "
USE escape_room_7b2026;
SELECT 'estacion' AS tabla, COUNT(*) AS filas FROM estacion
UNION ALL SELECT 'tema', COUNT(*) FROM tema
UNION ALL SELECT 'pregunta', COUNT(*) FROM pregunta
UNION ALL SELECT 'respuesta', COUNT(*) FROM respuesta
UNION ALL SELECT 'configuracion', COUNT(*) FROM configuracion;"
```

Resultado esperado:


| Tabla           | Filas |
| ----------------- | ------- |
| `estacion`      | 5     |
| `tema`          | 14    |
| `pregunta`      | 80    |
| `respuesta`     | 240   |
| `configuracion` | 9     |

Si los conteos no coinciden, revisar que los seeds se hayan ejecutado completos
y sin errores.

---

## 8. Levantar la aplicación

Con el entorno virtual activado y desde la raíz del proyecto:

```bash
source .venv/bin/activate
flask --app app run --debug
```

La aplicación queda en [http://127.0.0.1:5000](http://127.0.0.1:5000). Para detenerla, `Ctrl+C`.

Comprobar que responde y que ve la base:

```bash
curl -i http://127.0.0.1:5000/salud
```

Respuesta esperada: `200` con

```json
{"estado": "ok", "base": "ok"}
```

Si devuelve `503`, el problema está en MySQL o en las credenciales del `.env`,
no en el juego.

También se puede abrir el panel de administración en
[http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin) con `ADMIN_USER` y la clave cuyo hash se cargó en
`ADMIN_PASSWORD_HASH`.

### 8.1 Recorrer la aplicación

Con el servidor levantado, hacer este recorrido mínimo antes de dar la
instalación por buena:

1. Abrir [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Debe aparecer la
   bienvenida con nombre, cantidad de integrantes y dificultad.
2. Completar un equipo de prueba (por ejemplo, `Prueba`, 3 integrantes,
   `Inicial`) y enviar. Debe entrar a la estación 1 con 4 preguntas de 3
   opciones, el HUD y los dos contadores.
3. Comprobar que el contador general sube y el de la estación baja desde
   `04:00`. Recargar la página no debe reiniciar ninguno de los dos ni cambiar
   las preguntas.
4. Responder el formulario. La app registra el envío y muestra si la estación
   se superó o cuántas incorrectas quedan. No hace falta completar las 5
   estaciones para esta prueba.
5. Abrir [http://127.0.0.1:5000/ranking](http://127.0.0.1:5000/ranking): debe
   mostrar una tabla por nivel y actualizarse sola.
6. Abrir [http://127.0.0.1:5000/estadisticas](http://127.0.0.1:5000/estadisticas):
   debe mostrar los agregados, sin nombres de equipos.
7. Entrar a [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin),
   autenticarse y revisar `/admin/cobertura` y `/admin/intentos-activos`.

Si algún paso falla, revisar la sección 12 antes de seguir. Para una partida
completa de prueba conviene usar `/admin` para ver el equipo, el intento y las
respuestas registradas.

> `flask run --debug` es solo para desarrollo. Para la feria se usa waitress,
> como se explica en la sección 11.

---

## 9. Correr las pruebas automatizadas

Con el entorno virtual activado y el `.env` configurado:

```bash
pytest
```

Los tests usan una base **independiente** (`escape_room_7b2026_test` por
defecto): la crean, cargan el esquema y los tres seeds, y la limpian entre
pruebas. No
tocan la base real de la feria. Por eso el usuario de MySQL necesita permiso
para crear y borrar esa base (ver sección 7.2).

Para ver el detalle de cada prueba:

```bash
pytest -v
```

Si falla la conexión, revisar que MySQL esté activo, que el usuario exista y
que `MYSQL_*` en `.env` sea correcto.

---

## 10. Acceder desde otra máquina de la red

Por defecto Flask escucha solo en `127.0.0.1`, así que únicamente se puede abrir
desde la misma máquina. Para probar desde otra notebook o el televisor:

```bash
flask --app app run --debug --host=0.0.0.0
```

Averiguar la IP de esta máquina:

```bash
hostname -I
```

Desde la otra máquina, abrir:

```text
http://IP-DE-ESTA-MAQUINA:5000
```

Por ejemplo, `http://192.168.1.50:5000`. La vista del ranking para el televisor
está en `http://IP-DE-ESTA-MAQUINA:5000/ranking`.

Tener en cuenta:

- Las dos máquinas deben estar en la misma red.
- Si hay firewall, habilitar el puerto `5000` solo para la red local.
- No usar `localhost` desde la otra máquina: `localhost` es esa máquina, no
  esta.
- Para la feria, el procedimiento completo con waitress en el puerto `8000`,
  systemd y firewall está en `docs/instalacion-y-puesta-en-funcionamiento.md`.

---

## 11. Dejarlo como servidor de la feria

Hasta acá la app corre con el servidor de desarrollo y solo desde la misma
máquina. Para la feria conviene dejarla como servicio: arranca sola al encender
la notebook y escucha en la red para que entren las demás notebooks y el
televisor.

Esta sección es el camino mínimo del **escenario A** (todo en la notebook). El
detalle de permisos, firewall, audio, plan B en el servidor de la escuela y
variante con base remota está en
`docs/instalacion-y-puesta-en-funcionamiento.md` y
`docs/instalacion-servidor-escuela.md`.

### 11.1 Copiar el proyecto y crear el usuario

```bash
sudo mkdir -p /opt/escape-room-7b2026
sudo rsync -a --exclude .venv --exclude .env \
  ./ /opt/escape-room-7b2026/

sudo useradd --system --home /opt/escape-room-7b2026 \
  --shell /usr/sbin/nologin escaperoom
sudo chown -R escaperoom:escaperoom /opt/escape-room-7b2026
```

No copiar `.venv` ni `.env` desde otra máquina: el entorno virtual no es
portable y el `.env` se arma de nuevo.

### 11.2 Entorno virtual, dependencias y `.env`

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom python3 -m venv .venv
sudo -u escaperoom .venv/bin/pip install -r requirements.txt

sudo -u escaperoom cp .env.example .env
sudo -u escaperoom chmod 600 .env
sudo -u escaperoom nano .env
```

Completar el `.env` como en la sección 6, con los valores reales. La base y el
usuario se crean igual que en la sección 7, pero desde `/opt/escape-room-7b2026`:

```bash
cd /opt/escape-room-7b2026
sudo mysql < bd/schema.sql
sudo mysql < bd/seeds/001_contenido_inicial.sql
sudo mysql < bd/seeds/002_contenido_intermedio.sql
sudo mysql < bd/seeds/003_contenido_avanzado.sql
```

### 11.3 Probar waitress a mano

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom .venv/bin/waitress-serve \
  --call --listen=127.0.0.1:8000 app:create_app
```

En otra terminal:

```bash
curl -i http://127.0.0.1:8000/salud
```

Debe devolver `200` con `{"estado": "ok", "base": "ok"}`. Detener con `Ctrl+C`.

### 11.4 Servicio systemd

Crear `/etc/systemd/system/escape-room.service`:

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now escape-room
sudo systemctl status escape-room --no-pager
```

Ver logs y reiniciar después de un cambio:

```bash
journalctl -u escape-room -f
sudo systemctl restart escape-room
```

### 11.5 Firewall y acceso desde las notebooks

Abrir `8000` solo para la red del aula:

```bash
sudo ufw allow OpenSSH
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
sudo ufw enable
sudo ufw status verbose
```

Reemplazar `192.168.1.0/24` por la red real (`ip -4 addr show`).

Averiguar la IP y anotarla; conviene reservarla en el router:

```bash
hostname -I
```

Desde una notebook de la misma red:

```text
http://IP-DE-LA-NOTEBOOK:8000
http://IP-DE-LA-NOTEBOOK:8000/ranking
```

Comprobar también que el equipo que corre MySQL tiene la hora y la zona horaria
correctas: los tiempos del juego salen de `NOW(3)` de MySQL.

### 11.6 Antes de la feria

- Generar un respaldo con `./scripts/backup.sh` y **probarlo** con
  `./scripts/restaurar.sh` (sección 10 del `README.md`).
- Copiar el respaldo a un pendrive **fuera** de la notebook.
- Probar desde 3 notebooks y el televisor, sin Internet.
- Desactivar la suspensión de la notebook y pausar actualizaciones automáticas.
- No cambiar el código, el esquema ni el contenido el día de la feria.

---

## 12. Problemas frecuentes


| Síntoma                                        | Causa probable                                       | Solución                                                                            |
| ------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| `mysql: command not found`                      | MySQL no está instalado.                            | `sudo apt install mysql-server`.                                                     |
| `Can't connect to local MySQL server`           | MySQL está apagado.                                 | `sudo systemctl start mysql` y verificar con `systemctl status mysql`.               |
| `Access denied for user 'escaperoom'`           | Clave incorrecta o usuario inexistente.              | Revisar `MYSQL_PASSWORD`, repetir los `CREATE USER` y `GRANT`.                       |
| `Unknown database 'escape_room_7b2026'`         | No se ejecutó `bd/schema.sql`.                      | `sudo mysql < bd/schema.sql`.                                                        |
| La app arranca pero `/salud` devuelve `503`     | MySQL caído o credenciales mal.                     | Probar `mysql -u escaperoom -p -e "SELECT 1"` y revisar `.env`.                      |
| `Falta la variable de entorno ...`              | Falta una clave en `.env`.                           | Completar `FLASK_SECRET_KEY`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER` o `MYSQL_DB`. |
| `FLASK_SECRET_KEY tiene el valor de ejemplo`    | No se cambió la clave de la plantilla.              | Generar una nueva con `secrets.token_hex(32)`.                                       |
| `No module named 'flask'`                       | El entorno virtual no está activado.                | `source .venv/bin/activate`.                                                         |
| `No module named 'app'`                         | Se ejecutó el comando desde otra carpeta.           | Entrar a la raíz del proyecto, donde está `app/`.                                  |
| `Authentication plugin 'caching_sha2_password'` | Falta el extra `rsa` de PyMySQL.                     | `pip install "PyMySQL[rsa]"` o reinstalar `requirements.txt`.                        |
| `Address already in use`                        | Otro proceso usa el puerto `5000` u `8000`.        | Cerrarlo o usar `flask --app app run --debug --port=5001`.                            |
| `Table ... doesn't exist`                       | Falta el esquema o algún seed.                          | Ejecutar `bd/schema.sql` y después los tres seeds.                                         |
| El seed duplica datos                           | Se modificó un seed o los ids fijos.                | Usar los seeds originales, que son idempotentes.                                           |
| `pytest` falla al crear la base de test         | El usuario no tiene permiso para crear/borrar bases. | Otorgar permisos sobre `escape_room_7b2026_test.*` (sección 7.2).                   |
| El panel `/admin` no acepta la clave            | `ADMIN_PASSWORD_HASH` no corresponde a la clave.     | Regenerar el hash y reiniciar Flask.                                                 |
| El servicio no arranca o se reinicia solo       | Error en `.env` o en el `ExecStart`.                 | `sudo journalctl -u escape-room -n 50` y probar waitress a mano (sección 11.3).       |
| Las notebooks no entran pero `curl` local sí     | waitress escucha en `127.0.0.1` o el firewall bloquea. | Usar `--listen=0.0.0.0:8000` y abrir `8000` en `ufw` (sección 11.5).                 |
| El ranking muestra tiempos raros                | Reloj del equipo que corre MySQL desfasado.          | `timedatectl`, sincronizar la hora y reiniciar MySQL.                                |

---

## 13. Checklist final

- [ ]  MySQL instalado y activo (`systemctl status mysql`).
- [ ]  Proyecto clonado y ubicado en la raíz correcta.
- [ ]  `.venv` creado con `python3 -m venv .venv`.
- [ ]  `pip install -r requirements.txt` sin errores.
- [ ]  `.env` creado desde `.env.example`, completo y con permisos `600`.
- [ ]  `FLASK_SECRET_KEY` y `ADMIN_PASSWORD_HASH` generados de verdad.
- [ ]  Base creada con `bd/schema.sql`.
- [ ]  Usuario de MySQL creado para `'localhost'` y `'127.0.0.1'`, con permisos sobre la base real, la de test y las temporales de restauración.
- [ ]  Seeds cargados y conteos verificados (`5/14/80/240/9`).
- [ ]  `flask --app app run --debug` levanta sin errores.
- [ ]  `/salud` responde `200` con `{"estado": "ok", "base": "ok"}`.
- [ ]  `/admin` permite entrar con `ADMIN_USER` y la clave elegida.
- [ ]  `pytest` termina correctamente.
- [ ]  Se recorrió la app en el navegador: bienvenida, estación 1, `/ranking`,
       `/estadisticas` y `/admin` (sección 8.1).
- [ ]  Si se prueba desde otra máquina, se usó `--host=0.0.0.0` y la IP correcta.
- [ ]  Servicio `escape-room` habilitado y escuchando en `0.0.0.0:8000`
       (sección 11).
- [ ]  `8000` abierto solo para la red del aula y `3306` cerrado al exterior.
- [ ]  Backup generado y **restaurado** en una base de prueba.

Con esto el proyecto queda funcionando y navegable. Para el detalle completo de
la puesta en marcha durante la feria (audio, suspensión, plan B en el servidor
de la escuela y variante con base remota), continuar con
`docs/instalacion-y-puesta-en-funcionamiento.md` y
`docs/instalacion-servidor-escuela.md`.
