# Escape Room 7.º B 2026

Aplicación web para la Feria de Producciones del IPEATyM 186 Castagnari
(16/11/2026). Equipos de hasta 4 integrantes recorren **5 estaciones** en
orden, responden **4 preguntas por estación** y compiten por completar el
recorrido en el menor tiempo posible.

## Contenido

- [1. Qué es](#1-qué-es)
- [2. Cómo se juega](#2-cómo-se-juega)
- [3. Stack y requisitos](#3-stack-y-requisitos)
- [4. Estructura del proyecto](#4-estructura-del-proyecto)
- [5. Rutas de la aplicación](#5-rutas-de-la-aplicación)
- [6. Modelo de datos](#6-modelo-de-datos)
- [7. Puesta en marcha](#7-puesta-en-marcha)
- [8. Base de datos](#8-base-de-datos)
- [9. Servidor para la feria](#9-servidor-para-la-feria)
- [10. Respaldos y restauración](#10-respaldos-y-restauración)
- [11. Pruebas automatizadas](#11-pruebas-automatizadas)
- [12. Funcionalidad implementada](#12-funcionalidad-implementada)
- [13. Documentación](#13-documentación)

---

## 1. Qué es

Un *escape room* educativo sobre informática. Cada equipo elige un nombre, la
cantidad de integrantes (1 a 4) y una dificultad (`inicial`, `intermedio` o
`avanzado`). Después recorre cinco estaciones temáticas:

1. Redes
2. Hardware
3. Internet
4. Ciberseguridad
5. Sistemas Operativos

Cada estación tiene **4 minutos** y **4 preguntas** del nivel elegido. Para
avanzar hay que responder las 4 correctamente. Dos respuestas incorrectas en
una estación, quedarse sin tiempo o abandonar eliminan al equipo. Al completar
las cinco estaciones el intento entra al ranking de su nivel.

La aplicación está pensada para funcionar **sin Internet**: Bootstrap, el audio
y los gráficos son locales. Solo necesita la red del aula para que las
notebooks y el televisor lleguen al servidor.

## 2. Cómo se juega

1. El equipo entra a `/` y completa nombre, cantidad de integrantes y
   dificultad.
2. Si el nombre ya existe, la app pide el **ID del equipo** (que se muestra
   siempre en el HUD) y continúa con ese equipo.
3. En cada estación ve las 4 preguntas, el tiempo general (sube), el tiempo de
   estación (baja) y el HUD con ayudas, incorrectas y envíos.
4. Las pistas **no se muestran en la app**: los chicos las leen en papel y la
   app solo registra hasta 2 ayudas por estación.
5. Al superar una estación aparece la transición con **Continuar** (prepara la
   siguiente) o **Abandonar**.
6. Al terminar la quinta se muestra el resultado, la posición de nivel, la
   posición general y el ranking completo.
7. El televisor del aula muestra `/ranking`, que se actualiza solo cada 8
   segundos.

## 3. Stack y requisitos

| Componente | Versión / detalle |
| --- | --- |
| Backend | Python **3.10 o superior** + Flask 3.1.3 |
| Base de datos | **MySQL 8.0 o superior** (o MariaDB 10.3+) |
| Driver | PyMySQL 1.2.3 con extra `rsa` para `caching_sha2_password` |
| Servidor de producción | waitress 3.0.2 |
| Frontend | HTML server-rendered con Jinja + Bootstrap local |
| Pruebas | pytest 9.2.0 |
| Audio y gráficos | Archivos locales, sin CDN |

No hacen falta Node.js, React, Docker ni un paso de build. El servidor es la
autoridad del juego: valida respuestas, calcula tiempos y guarda todo en MySQL.
El navegador solo dibuja lo que el servidor devuelve.

> **Python 3.10+** es obligatorio: `pytest 9.2` no instala en 3.9. Flask 3.1
> acepta 3.9, pero el proyecto se prueba con 3.10 o superior.
>
> **MySQL 8.0+** (o MariaDB 10.3+) es obligatorio: el ranking usa
> `ROW_NUMBER() OVER (...)` y el esquema usa columnas generadas y `CHECK`.

## 4. Estructura del proyecto

```text
escaperoom7B26/
├── app/                              # Aplicación Flask
│   ├── __init__.py                   # App factory: lee .env, /salud, errores y filtros de formato
│   ├── db.py                         # Conexión PyMySQL por request y helper transaction()
│   ├── csrf.py                       # Token CSRF por sesión, sin dependencias externas
│   ├── routes/
│   │   ├── __init__.py               # Registro de los cuatro blueprints
│   │   ├── juego.py                  # Bienvenida, identificación, estaciones, transición, final
│   │   ├── ranking.py                # /ranking y /ranking/datos
│   │   ├── estadisticas.py           # /estadisticas
│   │   └── admin.py                  # Login, panel, CRUD, cobertura y dificultades
│   ├── servicios/                    # Lógica de dominio, sin HTML
│   │   ├── configuracion.py          # Parámetros del juego y dificultades habilitadas
│   │   ├── equipos.py                # Identidad, alta y reanudación de intentos
│   │   ├── estaciones.py             # Orden del recorrido y consultas de estaciones
│   │   ├── seleccion.py              # Selección aleatoria congelada en intento_pregunta
│   │   ├── envios.py                 # Envíos, ayudas, abandono y cierre de estación
│   │   ├── tiempos.py                # Contadores calculados desde fechas de MySQL
│   │   ├── ranking.py                # Ranking completo, posición y número de intento
│   │   ├── estadisticas.py           # Agregados de la página pública
│   │   ├── cobertura.py              # Reporte estación × nivel
│   │   ├── admin_tablas.py           # Metadata y listas blancas del CRUD
│   │   ├── admin_consultas.py        # Listados, filtros, orden y paginación
│   │   ├── admin_acciones.py         # Altas, ediciones y bajas lógicas
│   │   └── admin_estadisticas.py     # Métricas y gráficos del panel
│   ├── templates/                    # Plantillas Jinja
│   │   ├── base.html                 # Layout común
│   │   ├── bienvenida.html           # Formulario de equipo
│   │   ├── identificar.html          # Confirmación de ID para equipos existentes
│   │   ├── juego.html                # Pantalla de estación
│   │   ├── _hud.html                 # Equipo, estación, contadores, ayudas, incorrectas y envíos
│   │   ├── estacion.html             # Preguntas y respuestas
│   │   ├── estacion_no_disponible.html # Cobertura insuficiente (503)
│   │   ├── transicion.html           # Resumen y botones Continuar / Abandonar
│   │   ├── final.html                # Resultado, top 10 y ranking filtrable
│   │   ├── eliminado.html            # Motivo de eliminación
│   │   ├── ranking.html              # Vista pública para el televisor
│   │   ├── estadisticas.html         # Agregados de la feria
│   │   ├── _csrf_campo.html          # Campo oculto reutilizable
│   │   ├── 400.html, 404.html, 500.html
│   │   └── admin/                    # panel, listado, formulario, detalle, cobertura,
│   │                                 # dificultades, intentos activos, estadísticas, login
│   ├── static/
│   │   ├── css/publico.css           # Estilos de las pantallas públicas
│   │   ├── css/temporizadores.css    # Contadores y aviso de 30 segundos
│   │   ├── js/juego.js               # Confirmaciones y envío
│   │   ├── js/temporizadores.js      # Cuenta local y sincronización con /juego/estado
│   │   ├── js/ranking.js             # Polling de /ranking/datos cada 8 segundos
│   │   ├── audio/aviso-30s.wav       # Aviso sonoro local
│   │   └── vendor/bootstrap/         # Bootstrap 5 local (CSS, JS y licencia)
│   └── ...
├── bd/
│   ├── schema.sql                    # Crea la base y las 12 tablas (sin contenido)
│   ├── escape_room_7b2026_completa.sql # Instantánea: estructura + contenido + niveles
│   └── seeds/
│       ├── 001_contenido_inicial.sql # 20 preguntas de nivel inicial
│       ├── 002_contenido_intermedio.sql # 30 preguntas de nivel intermedio
│       └── 003_contenido_avanzado.sql # 30 preguntas de nivel avanzado
├── scripts/
│   ├── backup.sh                     # Volcado desde el .env (local o remoto)
│   └── restaurar.sh                  # Restauración segura en una base temporal
├── tests/
│   ├── conftest.py                   # Base de test, seeds y limpieza
│   ├── helpers.py                    # CSRF, POST y datos de juego
│   └── test_*.py                     # 9 archivos: juego, ranking, admin, CSRF, seeds, etc.
├── docs/                             # Requisitos, guías y material de la feria
│   ├── argumentos-pasos/             # Un archivo por paso, con criterios de aceptación
│   ├── instalacion-y-puesta-en-funcionamiento.md # Escenario A (notebook Ubuntu)
│   ├── instalacion-servidor-escuela.md # Escenarios B y C
│   ├── dejar-funcionando-proyecto-luego-clone.md # De clonar a navegar
│   └── ...                           # Requisitos, navegación, pistas, material
├── sql/descripcion-de-la-base-de-datos.md # Modelo explicado para el diagrama E-R
├── requirements.txt                  # Dependencias fijadas
├── pytest.ini                        # testpaths = tests, pythonpath = .
├── .env.example                      # Plantilla de configuración
├── .gitignore                        # Excluye .env, .venv, cachés y respaldos
├── AGENTS.md                         # Decisiones registradas, modelo y convenciones
├── MEMORY.md                         # Estado actual del proyecto
├── README.md                         # Este archivo
├── opencode.json                     # Configuración del agente de desarrollo
├── skills-lock.json                  # Skills del agente
└── .agents/                          # Skills locales del agente
```

### 4.1 Qué hace cada servicio

| Módulo | Responsabilidad |
| --- | --- |
| `configuracion.py` | Lee `configuracion`, valida parámetros y expone las dificultades habilitadas. |
| `equipos.py` | Normaliza nombres, crea equipos, pide el ID si el nombre existe y reanuda o crea intentos. |
| `estaciones.py` | Define el recorrido por `orden` y valida que exista una estación activa con `orden = 1`. |
| `seleccion.py` | Sortea 4 preguntas del nivel con al menos una por tema y las congela en `intento_pregunta`. |
| `envios.py` | Registra envíos, respuestas, incorrectas, ayudas, abandono, tiempo agotado y cierre de la quinta estación. |
| `tiempos.py` | Calcula los contadores con `TIMESTAMPDIFF` desde las fechas de MySQL y marca el aviso de 30 segundos. |
| `ranking.py` | Arma el ranking de intentos completos con posición general y posición por nivel. |
| `estadisticas.py` | Calcula los agregados públicos sin nombres de equipos ni respuestas correctas. |
| `cobertura.py` | Verifica que cada tema activo tenga al menos una pregunta del nivel y 4 por estación. |
| `admin_tablas.py` | Define tablas, campos, filtros y listas blancas de orden para el panel. |
| `admin_consultas.py` | Resuelve listados, búsqueda, filtros, orden y paginación en el servidor. |
| `admin_acciones.py` | Valida y ejecuta altas, ediciones y bajas lógicas; bloquea los históricos. |
| `admin_estadisticas.py` | Calcula métricas y series para las barras CSS del panel. |

## 5. Rutas de la aplicación

| Método | Ruta | Para qué | Login |
| --- | --- | --- | --- |
| `GET` | `/` | Bienvenida: nombre, integrantes y dificultad. | No |
| `POST` | `/` | Crea el equipo y el intento, o deriva a identificación. | No |
| `GET/POST` | `/equipo/identificar` | Pide el ID del equipo cuando el nombre ya existe. | No |
| `GET` | `/juego` | Redirige a la estación actual del intento. | No |
| `GET` | `/juego/estado` | JSON con contadores y hora del servidor (polling). | No |
| `GET` | `/juego/estacion/<orden>` | Muestra la estación con sus 4 preguntas. | No |
| `POST` | `/juego/estacion/<orden>/responder` | Registra el envío y evalúa la estación. | No |
| `POST` | `/juego/estacion/<orden>/ayuda` | Suma una ayuda (sin mostrar la pista). | No |
| `POST` | `/juego/estacion/<orden>/abandonar` | Cierra el intento como abandono. | No |
| `POST` | `/juego/estacion/<orden>/finalizar` | Cierra el intento por respuestas incorrectas. | No |
| `GET` | `/juego/transicion/<orden>` | Resumen de la estación superada. | No |
| `POST` | `/juego/transicion/<orden>/continuar` | Prepara la estación siguiente. | No |
| `POST` | `/juego/transicion/<orden>/abandonar` | Abandona desde la transición (1 a 4). | No |
| `GET` | `/juego/final` | Resultado y ranking del intento completado. | No |
| `GET` | `/juego/eliminado` | Motivo de la eliminación y resumen. | No |
| `GET` | `/ranking` | Ranking público por nivel para el televisor. | No |
| `GET` | `/ranking/datos` | JSON agrupado por nivel para el polling. | No |
| `GET` | `/estadisticas` | Agregados públicos de la feria. | No |
| `GET` | `/salud` | Comprueba la app y la conexión a MySQL. | No |
| `GET/POST` | `/admin`, `/admin/login`, `/admin/logout` | Login y cierre de sesión del panel. | No |
| `GET` | `/admin/` | Panel con cards y estado del juego. | Sí |
| `GET/POST` | `/admin/<tabla>`, `.../nuevo`, `.../<id>`, `.../<id>/editar`, `.../<id>/desactivar` | CRUD con filtros, orden y baja lógica. | Sí |
| `GET` | `/admin/cobertura`, `/admin/intentos-activos`, `/admin/estadisticas` | Reportes y métricas. | Sí |
| `GET/POST` | `/admin/dificultades` | Habilita o deshabilita `intermedio` y `avanzado`. | Sí |

Las rutas `/admin/*` no están enlazadas desde ninguna página pública y todas
salvo el login exigen sesión.

## 6. Modelo de datos

La base `escape_room_7b2026` tiene **12 tablas** y se puede agrupar así:

| Grupo | Tablas | Para qué |
| --- | --- | --- |
| Contenido | `estacion`, `tema`, `pregunta`, `respuesta` | Árbol de contenido con borrado lógico (`activo`). |
| Equipos e intentos | `equipo`, `intento` | Identidad del equipo y cada partida con su dificultad y estado final. |
| Detalle de la partida | `intento_estacion`, `intento_envio`, `intento_pregunta`, `respuesta_elegida`, `incorrecta` | Tiempos por estación, envíos, selección congelada y todas las respuestas elegidas. |
| Configuración | `configuracion` | Parámetros del juego y dificultades habilitadas. |

Las **9 claves** de `configuracion` son:

- `duracion_estacion_segundos` (240)
- `max_ayudas_estacion` (2)
- `max_envios_estacion` (2)
- `max_respuestas_incorrectas` (2)
- `max_integrantes_equipo` (4)
- `max_temas_por_estacion` (4)
- `preguntas_por_estacion` (4)
- `dificultad_intermedia_habilitada` (`0` o `1`)
- `dificultad_avanzada_habilitada` (`0` o `1`)

Reglas que el código respeta:

- `equipo`, `intento`, `respuesta_elegida` e `incorrecta` son **históricos**:
  no se borran.
- `estacion`, `tema`, `pregunta` y `respuesta` usan **borrado lógico**.
- `intento.se_completo_ok` es una columna generada desde `finalizado`.
- Solo los intentos `finalizado = 'completo'` entran al ranking.
- La selección de preguntas queda congelada en `intento_pregunta`: recargar no
  la cambia.
- Los tiempos se calculan con `NOW(3)` de MySQL: el reloj del servidor de base
  es la autoridad.

El detalle completo está en `sql/descripcion-de-la-base-de-datos.md`.

## 7. Puesta en marcha

Resumen para una máquina con Ubuntu/Debian, Python 3.10+ y MySQL 8.0+. La guía
paso a paso, desde el clonado hasta recorrer la app, está en
`docs/dejar-funcionando-proyecto-luego-clone.md`.

```bash
git clone <URL-DEL-REPOSITORIO> escaperoom7B26
cd escaperoom7B26

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
chmod 600 .env
# Editar .env: ver la sección 7.1
```

### 7.1 Configurar `.env`

Generar la clave de Flask y el hash del panel **con el entorno activado**:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"
```

Completar `.env`:

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

- No dejar `FLASK_SECRET_KEY` con el valor de ejemplo: la app no arranca.
- Si una clave tiene espacios, `#`, `$` o comillas, escribirla entre comillas
  dobles.
- `.env` no se versiona y debe quedar con permisos `600`.
- `ADMIN_PASSWORD_HASH` contiene `$`: **no** ejecutar `source .env` en scripts
  de shell. Los scripts del proyecto lo leen línea por línea.

### 7.2 Crear la base y el usuario

```bash
sudo mysql < bd/schema.sql
```

Crear el usuario de la aplicación (misma clave que `MYSQL_PASSWORD`):

```sql
CREATE USER 'escaperoom'@'localhost'
  IDENTIFIED BY 'una-clave-larga-y-propia';
CREATE USER 'escaperoom'@'127.0.0.1'
  IDENTIFIED BY 'una-clave-larga-y-propia';

GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'127.0.0.1';

-- Solo para pytest.
GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'127.0.0.1';

-- Solo para scripts/restaurar.sh (bases temporales).
GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'127.0.0.1';

FLUSH PRIVILEGES;
EXIT;
```

### 7.3 Cargar el contenido

```bash
mysql -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

Los seeds son idempotentes y no habilitan `intermedio` ni `avanzado`: eso se
hace desde `/admin/dificultades` cuando la cobertura está completa (ver
sección 8).

### 7.4 Levantar y comprobar

```bash
source .venv/bin/activate
flask --app app run --debug
```

- Aplicación: <http://127.0.0.1:5000>
- Salud: <http://127.0.0.1:5000/salud> → `200` con
  `{"estado": "ok", "base": "ok"}`
- Panel: <http://127.0.0.1:5000/admin> con `ADMIN_USER` y la clave elegida.

`flask run --debug` es solo para desarrollo. Para la feria se usa waitress
(sección 9).

## 8. Base de datos

El esquema y los tres seeds ya están disponibles:

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
```

El contenido queda en 5 estaciones, 14 temas y 80 preguntas (20 `inicial`,
30 `intermedio` y 30 `avanzado`) con 3 opciones cada una. Los seeds son
idempotentes: se pueden volver a ejecutar sin duplicar filas y no reactivan
contenido desactivado desde `/admin`. Tampoco habilitan los niveles ni tocan
`configuracion`: `intermedio` y `avanzado` se habilitan desde
`/admin/dificultades` cuando la cobertura está completa.

Para cargar **estructura y contenido de una sola vez**:

```bash
mysql -u <usuario> -p < bd/escape_room_7b2026_completa.sql
```

Ese archivo es una instantánea generada desde `bd/schema.sql` y los tres
seeds. Deja las 5 estaciones, 14 temas, 80 preguntas, 240 respuestas y las tres
dificultades habilitadas, sin equipos ni intentos. **Elimina y vuelve a crear
las 12 tablas**, así que hay que hacer backup antes de usarlo sobre una base
con partidas. La fuente de verdad sigue siendo `bd/schema.sql` más los seeds:
si cambia el contenido, hay que regenerar el archivo completo.

Conteos esperados después de cargar el contenido:

| Tabla | Filas |
| --- | --- |
| `estacion` | 5 |
| `tema` | 14 |
| `pregunta` | 80 |
| `respuesta` | 240 |
| `configuracion` | 9 |

## 9. Servidor para la feria

Para que las notebooks y el televisor entren por la red, waitress debe escuchar
en `0.0.0.0:8000` y el firewall debe permitir el puerto solo en la red del
aula. Resumen del escenario principal (notebook Ubuntu):

```bash
sudo mkdir -p /opt/escape-room-7b2026
sudo rsync -a --exclude .venv --exclude .env ./ /opt/escape-room-7b2026/
cd /opt/escape-room-7b2026
sudo -u escaperoom python3 -m venv .venv
sudo -u escaperoom .venv/bin/pip install -r requirements.txt
sudo -u escaperoom cp .env.example .env
sudo -u escaperoom chmod 600 .env
```

Servicio systemd `/etc/systemd/system/escape-room.service`:

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
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
```

Desde una notebook de la misma red: `http://IP-DEL-SERVIDOR:8000`. El
procedimiento completo (usuario, permisos, firewall, audio, plan B en el
servidor de la escuela y variante con base remota) está en
`docs/instalacion-y-puesta-en-funcionamiento.md` y
`docs/instalacion-servidor-escuela.md`.

## 10. Respaldos y restauración

Los scripts leen la conexión del `.env` y funcionan con MySQL local o remoto:

```bash
./scripts/backup.sh "$HOME/backups-escaperoom"
./scripts/restaurar.sh "$HOME/backups-escaperoom/respaldo-AAAAMMDD-HHMMSS.sql"
```

`backup.sh` genera un volcado sin `CREATE DATABASE` ni `USE` (no usa
`--databases`) y con permisos `600`. `restaurar.sh` crea una base temporal
`..._restore_...`, restaura, muestra los conteos y se niega a pisar la base
real o una base existente sin `--force`.

El detalle operativo está en `docs/instalacion-y-puesta-en-funcionamiento.md`
(secciones 10.3 y 10.4) y en `docs/instalacion-servidor-escuela.md`
(sección 6).

## 11. Pruebas automatizadas

La suite usa una base MySQL independiente. Al iniciar la sesión de pytest se
elimina y se vuelve a crear `escape_room_7b2026_test` (o la que indique
`TEST_MYSQL_DB`), se carga `bd/schema.sql` y los tres seeds de contenido, y
antes y después de cada test se limpian las tablas y se vuelven a ejecutar los
seeds. La base de desarrollo nunca se toca: el nombre debe terminar en `_test`
y ser distinto de `MYSQL_DB`. El usuario de MySQL necesita permisos `CREATE` y
`DROP` sobre esa base.

```bash
source .venv/bin/activate
pytest -q
```

La configuración está en `pytest.ini` (`testpaths = tests` y
`pythonpath = .`). Al terminar, la base de test queda creada y con los seeds.

## 12. Funcionalidad implementada

| Área | Qué está implementado |
| --- | --- |
| Bienvenida e identidad | Formulario con nombre, integrantes (1–4) y dificultades habilitadas. Nombre único; si existe, pide el ID del equipo y no lo duplica. Reanuda el intento activo o crea uno nuevo. |
| Selección de preguntas | 4 preguntas del nivel, al menos una por tema activo, sorteadas y congeladas en `intento_pregunta`. Con más de 4 temas se eligen 4 temas al azar. Recargar no cambia nada. |
| Estaciones y envíos | 5 estaciones en orden, sin saltos por URL. Cada envío exige una opción por pregunta y guarda las 4 respuestas en `respuesta_elegida` y las falladas en `incorrecta`. |
| Reglas de eliminación | 2 incorrectas acumuladas, 2 envíos sin completar, tiempo agotado o abandono cierran el intento con el motivo correspondiente. Con el segundo envío fallido solo queda **Finalizar juego**. |
| Ayudas | Hasta 2 por estación, con confirmación. La app no muestra el texto de la pista; solo suma en `intento_estacion.ayudas` y `intento.cantidad_ayudas`. |
| Temporizadores | General ascendente y estación descendente desde 4:00, calculados con fechas de MySQL. Polling cada 10 segundos y al volver a la pestaña. Aviso visual y sonoro a los 30 segundos. |
| Transición y final | Continuar prepara la siguiente estación y arranca su cronómetro. La quinta cierra el intento como `completo` con el tiempo congelado. El final muestra resultado, top 10 del nivel y ranking completo con filtros. |
| Ranking público | Una tabla por nivel, actualizada cada 8 segundos por polling. Si falla la conexión conserva las tablas y muestra **Reconectando…**. Solo intentos completos. |
| Estadísticas públicas | Agregados sin nombres de equipos ni respuestas correctas: equipos, integrantes, intentos, tiempo promedio y porcentaje de aciertos. |
| Administración | Login, panel con 12 tablas, CRUD con filtros y baja lógica, cobertura estación × nivel, toggles de dificultad, intentos activos y estadísticas con filtros. |
| Seguridad | Respuestas correctas solo en el servidor, CSRF en todos los POST, sesión de admin separada, `.env` fuera de Git y sin credenciales en el HTML. |

Para el detalle pantalla por pantalla, ver `docs/navegacion-por-app.md`.

## 13. Documentación

- `docs/proyectoEscapeRoom-7B.md` — título y reseña breve del proyecto.
- `docs/escape-room.md` — requisitos funcionales y contenido inicial.
- `docs/primeros-pasos.md` — hoja de ruta y guion de pedidos, paso a paso.
- `docs/argumentos-pasos/` — un archivo por paso (`paso00` a `paso12`, más `paso11b`, `paso11c`, `paso11d` y el `paso13` opcional de Docker post-feria), listo para usar con `/feature`. Incluye el índice y los criterios de aceptación.
- `docs/navegacion-por-app.md` — pantallas, rutas, elementos y objetivos.
- `docs/tecnologias.md` — stack explicado: frontend, backend, base de datos y herramientas.
- `docs/instalacion-y-puesta-en-funcionamiento.md` — instalación en Ubuntu y uso desde las notebooks (escenario A).
- `docs/instalacion-servidor-escuela.md` — servidor Linux de la escuela (escenario B) y base remota con la app en la notebook (escenario C).
- `docs/dejar-funcionando-proyecto-luego-clone.md` — de un repositorio recién clonado a la app funcionando en el navegador.
- `docs/ayuda-al-probar.md` — estado de la base y comandos rápidos para probar el juego.
- `sql/descripcion-de-la-base-de-datos.md` — modelo de datos, tablas y consultas.
- `docs/banco-preguntas-intermedio-avanzado.md` — 60 preguntas de `intermedio` y `avanzado` con sus opciones y pistas.
- `docs/contenido-para-responder-nivel-intermedio.md` — guía de estudio del nivel intermedio.
- `docs/contenido-para-responder-nivel-avanzado.md` — guía de estudio del nivel avanzado.
- `docs/pistas-del-juego.md` — las 160 pistas de las preguntas cargadas, más un anexo con las pistas de las preguntas en reserva.
- `AGENTS.md` — decisiones registradas, modelo de datos y convenciones.
- `MEMORY.md` — estado actual del proyecto y verificaciones realizadas.
