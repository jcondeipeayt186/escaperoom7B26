
Perfecto. Plan final confirmado (sigo en modo plan, así que no voy a crear ni modificar nada todavía):

## Archivos a crear/modificar cuando cambies a un agente de implementación

### 1. `docs/dejar-funcionando-proyecto-luego-clone.md` (nuevo)

Guía pensada para alguien que clona el repo en una máquina limpia:

1. **Requisitos**: Ubuntu/Debian, Python 3.10+, MySQL 8, git.
2. **Instalar MySQL y Python**: `apt install python3 python3-venv python3-pip mysql-server git`, habilitar MySQL y verificar.
3. **Clonar y entrar** al proyecto.
4. **Entorno virtual**: `python3 -m venv .venv`, activar, `pip install -r requirements.txt`; aclarar que `.venv` no se copia.
5. **`.env`**: `cp .env.example .env`, tabla variable por variable, cómo generar `FLASK_SECRET_KEY` y `ADMIN_PASSWORD_HASH`, comillas, `chmod 600` y por qué no se versiona.
6. **Base de datos**: cargar `bd/schema.sql` como root, crear el usuario para `'localhost'` y `'127.0.0.1'`, permisos incluido crear/borrar `escape_room_7b2026_test`, cargar el seed y verificar `5/14/20/60/9`.
7. **Levantar la app**: `flask --app app run --debug`, `http://127.0.0.1:5000`, `/salud` y `/admin`.
8. **Pruebas**: `pytest`, con la aclaración de que usa `escape_room_7b2026_test` y nunca la base real.
9. **Acceso desde otras máquinas**: `--host=0.0.0.0`, IP con `hostname -I`, y derivación a `docs/instalacion-y-puesta-en-funcionamiento.md` para waitress/systemd/firewall.
10. **Problemas frecuentes**: MySQL apagado, `Access denied`, base inexistente, seed sin cargar, variable faltante, puerto ocupado.
11. **Checklist final**.

### 2. `.env.example` (nuevo)

Con las 8 claves reales que lee `app/__init__.py` y valores de ejemplo seguros:

```dotenv
FLASK_SECRET_KEY=cambiar-por-una-clave-larga-y-aleatoria
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=escaperoom
MYSQL_PASSWORD=cambiar-esta-clave
MYSQL_DB=escape_room_7b2026
ADMIN_USER=admin
ADMIN_PASSWORD_HASH=cambiar-por-el-hash-generado
```

### 3. `.gitignore` (nuevo)

`.env`, `.venv/`, `.venv2/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.log`.

### 4. `README.md` (edición mínima)

Agregar `docs/dejar-funcionando-proyecto-luego-clone.md` a la lista de documentación.

## Nota

El `README.md` dice que “todavía no hay tests”, pero `tests/` ya existe y `pytest.ini` está configurado. En la guía nueva lo voy a documentar como está (los tests existen y corren). Si querés, en la implementación también corrijo esa frase del README.

Para que lo implemente, cambiá a un agente de implementación (por ejemplo el agente normal de OpenCode) y decile que aplique este plan.



Listo. Implementé lo planificado sin tocar los tests ni la frase del README sobre `pytest`.

## Cambios

**Nuevo: `docs/dejar-funcionando-proyecto-luego-clone.md`**
Guía completa para partir de un clon y dejar la app funcionando:

- Requisitos e instalación de MySQL/Python en Ubuntu/Debian.
- Clonado del proyecto.
- Creación y activación del entorno virtual, con `pip install -r requirements.txt`.
- Creación del `.env`: las 8 variables, cómo generar `FLASK_SECRET_KEY` y `ADMIN_PASSWORD_HASH`, comillas y `chmod 600`.
- Base de datos: `bd/schema.sql`, creación del usuario para `'localhost'` y `'127.0.0.1'`, permisos para la base real y la de tests, seed idempotente y verificación de conteos `5/14/20/60/9`.
- Levantar con `flask --app app run --debug`, probar `/salud` y `/admin`.
- `pytest` usando `escape_room_7b2026_test` sin tocar la base real.
- Acceso desde otra máquina con `--host=0.0.0.0`.
- Tabla de problemas frecuentes y checklist final.

**Nuevo: `.env.example`**
Plantilla con las variables reales que lee `app/__init__.py`, más `TEST_MYSQL_DB` opcional comentada.

**Nuevo: `.gitignore`**
Ignora `.env`, `.venv/`, `.venv2/`, `__pycache__/`, `.pytest_cache/`, logs y respaldos.

**Editado: `README.md`**
Se agregó el enlace a la nueva guía en la lista de documentación. No se tocó nada de los tests.

**Editado: `MEMORY.md`**
Se registró el estado nuevo del proyecto.

## Verificación hecha

- `create_app()` importa y valida la configuración correctamente.
- `pytest --collect-only` detectó 76 tests, así que la guía describe el estado real.

No ejecuté la suite completa para no crear/modificar la base de test sin necesidad.



Perfecto. Queda definido así:

- **Estructura:** `paso12` único + anexo nuevo.
- **Principal:** notebook Ubuntu 22.04 (escenario A).
- **Respaldo:** servidor de la escuela (escenario B), con `sudo` completo y MySQL 8.
- **Alternativa documentada:** MySQL en la escuela + app en la notebook (escenario C), sin improvisarla el día de la feria.

## Plan final de implementación

### 1. `docs/argumentos-pasos/paso12-congelar-y-puesta-en-marcha.md`

Reescribirlo para que sea el tronco común:

- Corregir `Requiere:` a `paso11d`.
- Agregar **“Escenarios de despliegue”** con A, B y C, y la matriz de decisión.
- Agregar una **ficha del servidor de la escuela** para completar con los datos reales.
- Actualizar el alcance al contenido actual: **80 preguntas**, tres niveles y decisión de qué niveles ofrecer.
- Actualizar los conteos esperados a **`5/14/80/240/9`** y mencionar `bd/escape_room_7b2026_completa.sql`.
- Detallar los scripts de backup/restauración.
- Separar criterios de aceptación **comunes** y **por escenario**.
- Simulacro para A y B; C solo si se elige.
- Agregar un **árbol de decisión para el día de la feria** y un “go/no-go”.
- Ampliar trampas conocidas: distro vieja, Python menor a 3.10, MySQL/MariaDB incompatible, abrir `3306`, reloj, servidor compartido, IP DHCP, backups en el equipo equivocado.

### 2. `docs/instalacion-servidor-escuela.md` (nuevo)

Anexo para B y C:

- **Recolección de datos** del servidor (distro, versión, arquitectura, Python, MySQL, systemd, red, firewall, permisos).
- **Detección del sistema** y tabla de equivalencias `apt` / `dnf` / `zypper` / `pacman`.
- **Escenario B completo:** instalar dependencias, venv, `.env`, esquema, seeds, waitress, systemd, firewall `8000`, IP y verificación.
- **Escenario C completo:**
  - En la escuela: `bind-address`, usuario `'escaperoom'@'IP-notebook'`, grants, firewall `3306` solo para la notebook, reloj, backups.
  - En la notebook: `.env` con `MYSQL_HOST` remoto, waitress, systemd y verificación.
  - Pruebas y permisos para la base `_test`.
  - Seguridad: no usar `'%'`, no exponer `3306` a toda la red, TLS opcional.
- **Problemas frecuentes** de conexión remota y distros no Ubuntu.
- **Checklist B** y **checklist C**.

### 3. `docs/instalacion-y-puesta-en-funcionamiento.md`

- Aclarar al inicio que cubre el **escenario A** en Ubuntu/notebook.
- Agregar la tabla “Elegir escenario” y el enlace al anexo.
- Ajustar la frase “No abrir el puerto `3306`” para exceptuar el escenario C con reglas restrictivas.
- Mantener el resto de la guía, que ya está probada.

### 4. `docs/primeros-pasos.md`

- Actualizar el **Pedido 12** con el alcance ampliado, como exige la regla de sincronización de `docs/argumentos-pasos/README.md`.

### 5. Scripts nuevos

- `scripts/backup.sh`
  - Lee `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DB` del `.env`.
  - Usa `mysqldump --single-transaction --no-tablespaces --default-character-set=utf8mb4`, sin `--databases`.
  - Genera el archivo con fecha y hora, verifica que no esté vacío y nunca lo commitea.
- `scripts/restaurar.sh`
  - Recibe el volcado y el nombre de la base destino.
  - Se niega a pisar `MYSQL_DB` sin `--force`.
  - Crea la base con `utf8mb4`, restaura y verifica conteos.
- Ambos funcionan igual en A, B y C porque usan `MYSQL_HOST` y `MYSQL_PORT`.

### 6. Enlaces y memoria

- Agregar el anexo a la lista de documentación de `README.md`.
- Actualizar `MEMORY.md` al terminar, con el escenario probado y la fecha de congelamiento.
- Commit: `docs: puesta en marcha y respaldo`.

### 7. Verificación que voy a dejar indicada

- Scripts validados con `bash -n` y probados contra una base temporal, sin tocar la base real.
- Backup real de solo lectura y restauración en `escape_room_7b2026_restore_test`.
- Conteos `5/14/80/240/9`.
- Simulacro A: 3 notebooks, televisor, sin Internet, reinicio de MySQL.
- Simulacro B: mismo procedimiento en el servidor de la escuela.
- Simulacro C: solo si se decide usarlo, con prueba de corte de red y reloj.

## Pendiente

Falta la **distro y versión del servidor de la escuela**. Si me pasás la salida del bloque de comandos que te dejé, ajusto el anexo a esa distro con comandos concretos. Si no, lo dejo con detección automática y una ficha para completar en el servidor.

Cuando quieras que lo implemente, cambiá a un agente de implementación y decile que aplique este plan. Yo sigo en modo plan y no puedo modificar archivos.


Terminé el **Paso 12** y su anexo. Resumen de lo que quedó en disco:

## Documentación

- **`docs/argumentos-pasos/paso12-congelar-y-puesta-en-marcha.md`** (reescrito): tronco común con la matriz de escenarios **A/B/C**, restricciones técnicas (Python 3.10+, MySQL 8.0+/MariaDB 10.3+, reloj de MySQL como autoridad, misma LAN, `sudo`), ficha del servidor a completar, conteos congelados `5/14/80/240/9`, criterios de aceptación por escenario, simulacros, trampas y árbol de decisión para la feria.
- **`docs/instalacion-servidor-escuela.md`** (nuevo): recolección de datos del servidor, equivalencias `apt`/`dnf`/`zypper`/`pacman`, **escenario B** completo (usuario de servicio, venv, `.env`, esquema, seeds, waitress, systemd, firewall, IP fija) y **escenario C** completo (`bind-address`, usuario `'escaperoom'@'IP-NOTEBOOK'`, grants, `3306` solo a la notebook, reloj, backups y vuelta a A).
- **`docs/instalacion-y-puesta-en-funcionamiento.md`**: queda como guía del escenario A, con tabla de escenarios, excepción restringida de `3306`, enlaces a los scripts y los grants de `_test` y `_restore_`.
- Actualizados **`docs/primeros-pasos.md`** (Pedido 12), **`README.md`** (anexo + sección “Respaldos y restauración”), **`docs/dejar-funcionando-proyecto-luego-clone.md`** (conteos y tres seeds) y **`MEMORY.md`**.

## Scripts (probados)

- `scripts/backup.sh`: lee el `.env` sin `source` (por los `$` de `ADMIN_PASSWORD_HASH`), sin `--databases`, y agrega `--no-tablespaces` solo si la herramienta lo soporta.
- `scripts/restaurar.sh`: restaura en `<MYSQL_DB>_restore_AAAAMMDD-HHMMSS`, muestra conteos y **se niega** a pisar la base real sin `--force` (verificado: código de salida `1`).

Verificación real ejecutada: respaldo generado → restaurado en `escape_room_7b2026_restore_paso12` con `5/14/80/240/9` → base temporal eliminada → base real intacta. También comprobé que el grant comodín `escape\_room\_7b2026\_restore\_%` permite crear y borrar esas bases (con un usuario temporal que después eliminé).

## Pendientes

1. **Ficha del servidor de la escuela**: falta la salida de `/etc/os-release` y `mysql --version` para adaptar los comandos del escenario B/C a su distribución. Hasta entonces ese anexo es “procedimiento a validar”.
2. **Simulacros A y B** en el aula (3 notebooks + televisor, sin Internet).
3. **Commit**: no hay repositorio git en este directorio, así que los cambios quedan como archivos en disco. Si querés, inicializo el repo o me indicás dónde está.

No modifiqué ni ejecuté los tests.



Voy a proponerte el plan antes de tocar nada. Revisé el repo real para que el scaffolding sea exacto (12 tablas, 4 blueprints, 13 módulos de servicio, 30 plantillas, 9 archivos de test).

## Plan propuesto

### 1. `README.md` — nueva estructura

1. **Título + qué es** (feria, 5 estaciones, 3 niveles) y **cómo se juega** en 6 líneas.
2. **Stack y requisitos**: Flask 3.1.3, PyMySQL, waitress, Bootstrap local, MySQL 8.0+/MariaDB 10.3+, Python **3.10+** (hoy dice “Python 3” y `pytest 9.2` exige 3.10).
3. **Scaffolding anotado** — árbol completo con un comentario por archivo/directorio:
   ```text
   app/__init__.py       app factory, config desde .env, /salud, errores, filtros de formato
   app/db.py             conexión PyMySQL por request + transaction()
   app/csrf.py           token CSRF por sesión
   app/routes/           juego, ranking, estadisticas, admin
   app/servicios/        lógica de dominio (13 módulos)
   app/templates/        Jinja (público + admin/)
   app/static/           css, js, audio/aviso-30s.wav, vendor/bootstrap
   bd/                   schema.sql, los 3 seeds y la base completa
   scripts/              backup.sh, restaurar.sh
   tests/                conftest, helpers y 9 archivos de prueba
   ...
   ```
4. **Qué hace cada módulo de `app/servicios/`** (tabla): `equipos`, `seleccion`, `envios`, `tiempos`, `ranking`, `estadisticas`, `cobertura`, `configuracion`, `estaciones`, `admin_tablas/consultas/acciones/estadisticas`.
5. **Rutas principales** (tabla: método, ruta, para qué, si exige login).
6. **Modelo de datos en 4 grupos**: contenido (5 tablas), históricos (4), detalle de partida (3), `configuracion` (9 claves).
7. **Base de datos**: se mantiene lo que ya está (seeds, archivo completo, advertencia de que borra las 12 tablas).
8. **Puesta en marcha**: resumen de 6 comandos + enlace a la guía completa.
9. **Servidor para la feria**: waitress en `0.0.0.0:8000`, systemd, enlace al escenario A/B.
10. **Respaldos y restauración** (se mantiene).
11. **Pruebas** (se mantiene).
12. **Documentación** (índice actual, revisado).
13. **Funcionalidad implementada**: propongo **condensarla** en una tabla por área (bienvenida, juego, temporizadores, ranking, admin, CSRF) con enlaces a `docs/navegacion-por-app.md`, en lugar de las ~150 líneas actuales.

### 2. `docs/dejar-funcionando-proyecto-luego-clone.md` — de cero a navegador

Se conserva la estructura actual y se agrega/ajusta:

- **Sección 0 “Antes de empezar”**: qué se necesita (Ubuntu 22.04/24.04, `sudo`, Internet solo para instalar, ~1 GB libre).
- **Clonar desde GitHub**: `git clone <URL>` + alternativa ZIP/pendrive. Hoy el placeholder no explica de dónde sale la URL.
- **Verificación de versiones** antes de instalar, con el mínimo explícito (`Python 3.10+`, `MySQL 8.0+`).
- **Base de datos**: aclarar que `schema.sql` y los seeds ya traen `CREATE DATABASE`/`USE`, y que el usuario debe tener permisos sobre la base; dejar “todo de una vez” como opción.
- **Sección “Recorrer la aplicación”** (nueva): abrir `/`, crear un equipo de prueba, jugar la estación 1, comprobar HUD y contadores, ver `/ranking`, `/estadisticas` y entrar a `/admin`. Es lo que hoy falta: llegar hasta “usar el navegador”.
- **Sección final “Dejarlo como servidor de la feria”** (nueva y breve): copiar a `/opt`, usuario `escaperoom`, venv, `.env` real, servicio systemd con waitress en `0.0.0.0:8000`, firewall `8000`, abrir desde otra notebook; enlace al detalle de `docs/instalacion-y-puesta-en-funcionamiento.md`. Así la guía llega de “clonado” a “servidor andando” sin obligar a saltar a otro documento.
- Ajustar la frase “permisos solo sobre las bases del proyecto” (hoy los grants incluyen `_test` y `_restore_`).

### 3. Correcciones chicas de consistencia (opcionales, las incluyo salvo que digas que no)

- `bd/seeds/001_contenido_inicial.sql` dice en la cabecera “no hay preguntas de intermedio ni avanzado todavía” (quedó viejo).
- README: “Flujo implementado hasta el paso 11” → “Funcionalidad implementada” (el 12 ya está hecho).
- README: “Requiere Python 3 y MySQL 8” → “Python 3.10+ y MySQL 8.0+”.

### Qué NO voy a hacer

- No toco tests, esquema, seeds (más allá de la cabecera), `app/` ni `MEMORY.md` sin avisar.
- No invento la URL del repositorio.

## Necesito que definas

1. **URL real de GitHub** o dejo `<URL-DEL-REPOSITORIO>` en las dos guías que la usan.
2. **README**: ¿condenso el bloque “Flujo implementado” en una tabla (mi recomendación) o lo dejo completo?
3. **Guía de clonado**: ¿la cierro con la sección de servidor para la feria (waitress/systemd resumido) o la dejo solo en desarrollo y que derive a `docs/instalacion-y-puesta-en-funcionamiento.md`?


Listo. Cerré el trabajo pendiente de documentación.

## Qué quedó hecho

**`README.md` (reescrito completo)**

- Índice con 13 secciones y andamiaje comentado de todo el repo (app, servicios, plantillas, estáticos, bd, scripts, tests, docs).
- Tabla de responsabilidad por servicio y tabla de rutas públicas + admin con su login.
- Modelo de datos en 4 grupos, con las 9 claves de `configuracion`.
- Puesta en marcha: entorno virtual, `.env`, usuario de MySQL y permisos (base real, `_test` y temporales `_restore_`), carga de seeds y de la instantánea completa.
- Servidor de feria (waitress + systemd + ufw), respaldos con los scripts, pruebas y tabla resumen de funcionalidad por área (reemplaza la vieja sección "Flujo implementado hasta el paso 11").
- Índice de documentación.

**`docs/dejar-funcionando-proyecto-luego-clone.md` (ampliada)**

- Nueva §0 con requisitos y convenciones.
- Clonado explícito desde GitHub (`<URL-DEL-REPOSITORIO>`) y verificación de la raíz.
- Mínimos de versión (Python 3.10+, MySQL 8.0+/MariaDB 10.3+).
- Nueva §8.1 con recorrido de la app en el navegador.
- Nueva §11 "Dejarlo como servidor de la feria" (rsync, usuario de servicio, venv, `.env`, waitress, systemd, ufw, IP, checklist).
- Problemas frecuentes y checklist renumerados a 12 y 13, con filas nuevas (servicio, firewall, reloj de MySQL).

**Correcciones de consistencia**

- Cabecera obsoleta del seed `bd/seeds/001_contenido_inicial.sql`.
- Estado obsoleto de `docs/navegacion-por-app.md`.

**`MEMORY.md`** actualizado con esta entrada y con el "Próximo paso" corregido (queda la ficha del servidor de la escuela y los simulacros A/B, más una partida de `intermedio` y otra de `avanzado` antes de la feria).

## Verificación

- Bloques de código balanceados en los tres documentos.
- Anclas internas resueltas y archivos enlazados existentes.
- No se modificaron ni ejecutaron los tests.

Queda pendiente, cuando me pases los datos del servidor de la escuela (`/etc/os-release` y `mysql --version`), completar la ficha en el `paso12` y en `docs/instalacion-servidor-escuela.md`.



Listo. Creé el paso en `docs/argumentos-pasos/paso11e-agregarimagenes.md`.

## Qué incluye

- **Uso de las imágenes**: `LogoCasta.png` como favicon, logo de la bienvenida, logo del ranking y logo del pie; `frente-cole.png` como foto de portada de la página inicial.
- **Derivados optimizados** en `app/static/img/`: logo de 256 px, favicon PNG de 32 px, `favicon.ico`, ícono de iOS de 180 px y foto JPEG de 1600 px. Presupuesto total menor a 200 KB.
- **Comandos de preparación** con ImageMagick (`convert`/`magick`) y una alternativa con Pillow, aclarando que Pillow **no** se agrega a `requirements.txt`.
- **Cambios exactos** en `base.html` (favicon, hoja `institucional.css` y pie con logo), `bienvenida.html` (logo y foto) y `ranking.html` (logo junto al título).
- **Estilos responsive** en `app/static/css/institucional.css` y `publico.css`, pensados para móvil y televisor.
- **Accesibilidad y rendimiento**: `alt`, `width`/`height`, `loading="lazy"` solo donde corresponde, sin CDN y todo servido desde `app/static/`.
- **Tests nuevos** para `tests/test_publico.py` y verificación manual en móvil, TV y sin red.
- **Criterios de aceptación, fuera de alcance y trampas** (no usar `docs/img/` como `src`, no copiar los originales de 5,4 MB, aplanar transparencias, caché del favicon, etc.).

También actualicé el índice de `docs/argumentos-pasos/README.md`, la ruta sugerida y el `paso12` para que requiera el `paso11e`. `MEMORY.md` quedó con la entrada del paso pendiente y el próximo paso actualizado.

## Aclaración importante

No pude **ver** las imágenes: el modelo no admite entrada de imágenes. Las medidas y composiciones del paso se basan en los metadatos reales:

- `LogoCasta.png`: 1746 × 1738, PNG con transparencia.
- `frente-cole.png`: 3840 × 2880, PNG con transparencia, relación 4:3.

Por eso el paso incluye una revisión visual obligatoria en el navegador antes de darlo por terminado. Si al implementarlo la foto o el logo se ven recortados o fuera de proporción, se ajustan el `max-width`, el `clamp()` o el recorte sin cambiar el resto del plan.

El paso quedó **documentado y pendiente**: no modifiqué código de la aplicación ni los tests.



Listo. Apliqué los tres ajustes y actualicé la documentación.

## Cambios

**1. Tiempo total del HUD en `MM:SS`**

- `app/templates/_hud.html`: el contador general pasó de `hhmmss` a `mmss`.
- `app/static/js/temporizadores.js`: unifiqué `formatoGeneral()` y `formatoEstacion()` en `formatoContador()`, así ambos contadores se dibujan igual entre sincronizaciones.
- La pantalla final, el ranking y las estadísticas conservan `HH:MM:SS`.

**2. Barras de “Tiempo promedio por estación”**

- `app/servicios/estadisticas.py` lee `duracion_estacion_segundos` con `duracion_estacion(leer_configuracion())` (respaldo 240) y calcula cada barra como `min(100, round(promedio * 100 / duracion))`.
- Ahora el 100 % equivale a los 4 minutos máximos de una estación; ya no se escala al promedio mayor.
- `app/templates/estadisticas.html` muestra la referencia `(04:00)` y expone `duracion_estacion` en el resumen.

**3. Navegación pública**

- `/ranking`: enlaces a **Inicio** y **Estadísticas**.
- `/estadisticas`: enlaces a **Inicio** y **Ranking**.
- Estilos nuevos `.publico__nav` en `app/static/css/publico.css`.

## Pruebas y documentación

- Agregué `test_hud_muestra_el_tiempo_general_en_mm_ss`, `test_navegacion_publica_entre_ranking_y_estadisticas` y aserciones de ancho `25/62/100 %` en `tests/test_publico.py`.
- `pytest -q` pasó dos veces seguidas: **96 tests**.
- Actualicé `docs/navegacion-por-app.md`, `AGENTS.md` (decisión 64), `MEMORY.md` y la nota histórica del `paso05`.

No modifiqué `bd/` ni la base real.


Listo. Actualicé la guía y todos los documentos que presentaban waitress como requisito de la feria.

## Cambios

**Guía principal** — `docs/guia-de-estudio-para-estudiantes.md`

- §9 (intro), §9.1 paso 6, §9.2 paso 6 y el comando de Windows usan ahora `flask --app app run --debug --host=0.0.0.0`.
- §9.4 suma el error «Desde otra notebook no abre la app».
- §9.5 reescrita: no hace falta waitress ni systemd; Flask muestra la IP de la notebook, los equipos de la misma red juegan sin Internet, la terminal queda abierta y el puerto `5000` habilitado. Incluye checklist y aclara que `--debug` es solo para la red del aula.
- §8.5 rotula la guía de waitress/systemd como **post-feria**.

**Resto de la documentación**

- `README.md`: §7.4 y §9 explican que la feria usa Flask con `--host=0.0.0.0`; waitress/systemd quedan como producción posterior.
- `docs/tecnologias.md`: tabla del stack, §3.4, comandos de feria, diagrama de una petición y «Qué evitar» alineados.
- `docs/dejar-funcionando-proyecto-luego-clone.md`: nota inicial, aviso de §8.1, viñeta de la sección 10 y sección 11 retitulada «Dejar como servidor permanente (después de la feria)».
- `docs/instalacion-y-puesta-en-funcionamiento.md`: alcance y §6 aclaran que la feria usa Flask; §15 adapta el checklist.
- `docs/instalacion-servidor-escuela.md` y `docs/argumentos-pasos/paso12-congelar-y-puesta-en-marcha.md`: encuadre post-feria, arranque, criterio de aceptación y simulacro A.
- `AGENTS.md`: decisión 65 y comando de feria en la sección de comandos.
- `MEMORY.md`: entrada nueva con el estado y la decisión.

## Verificación

- Enlaces internos y bloques de código verificados en los 9 archivos editados (todos balanceados, sin enlaces rotos).
- No quedan frases que digan que la feria usa waitress o que prohíban el servidor de desarrollo en la feria.
- Solo cambios de documentación: no toqué `app/`, `tests/`, `bd/` ni la base real; no volví a correr `pytest` (la última corrida sigue en 96 tests).

Dejé intacto `docs/primeros-pasos.md`, porque es el registro histórico de los pedidos y menciona waitress como plan original. Si querés que también lo actualice, avisame.


Perfecto, quedan confirmadas las cuatro decisiones. Plan cerrado:

## Decisiones confirmadas


| Tema        | Decisión                                                                                                                                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contenido   | Redacto las **80 explicaciones** y las **14 introducciones**, y en el `paso11g` quedan las tablas completas para que las revises antes de cargar la base real.                                  |
| Transición | Se muestra **enunciado + respuesta correcta + explicación**. Se matiza en `AGENTS.md`: la respuesta correcta sigue prohibida en la estación, pero se muestra en la transición ya completada. |
| Script      | Solo `scripts/feria.sh`; Windows sigue con los comandos manuales de la guía.                                                                                                                   |
| Reparto     | Congelado y backup en el nuevo `paso12`; waitress/systemd, escenarios A/B/C y firewall en el `paso13`.                                                                                          |

## Archivos que se van a tocar

**Crear**

- `docs/argumentos-pasos/paso11g-explicaciones-en-transicion.md`
- `docs/argumentos-pasos/paso12-feria-con-flask.md`
- `docs/argumentos-pasos/paso13-waitress-y-systemd-post-feria.md` (renombre del actual `paso12`)
- `docs/argumentos-pasos/paso14-docker-taller-post-feria.md` (renombre del actual `paso13`)
- `bd/migraciones/20261113_explicaciones-e-introducciones.sql`
- `scripts/feria.sh`

**Modificar**

- `bd/schema.sql`, los tres seeds y `bd/escape_room_7b2026_completa.sql`
- `app/servicios/estaciones.py`, `app/routes/juego.py`, `app/templates/transicion.html`
- `app/servicios/admin_tablas.py` y el CSS de la transición
- `tests/test_seed.py`, `tests/test_reglas_juego.py`, `tests/test_admin.py`
- `docs/escape-room.md`, `sql/descripcion-de-la-base-de-datos.md`, `docs/navegacion-por-app.md`
- `docs/argumentos-pasos/README.md`, `docs/primeros-pasos.md`
- `README.md`, `AGENTS.md`, `MEMORY.md`, `docs/tecnologias.md`
- `docs/guia-de-estudio-para-estudiantes.md`, `docs/dejar-funcionando-proyecto-luego-clone.md`
- `docs/instalacion-y-puesta-en-funcionamiento.md`, `docs/instalacion-servidor-escuela.md`
- `.gitignore` (agregar `feria2026/`)

## Detalles técnicos que quedan fijados

- `tema.introduccion TEXT NULL` y `pregunta.explicacion TEXT NULL`, migración idempotente.
- El bloque de transición agrupa por tema, respeta el orden de `intento_pregunta.orden` y omite textos vacíos.
- La consulta lee el último envío con `respuestas_correctas = 4` y no filtra `activo`.
- `feria2026/` es el entorno virtual del script; se crea solo si falta, instala dependencias solo si faltan, exige `.env` y arranca con `--host=0.0.0.0`.
- La suite estimada pasa de 96 a ~101 tests y se corre dos veces.

## Siguiente paso

Estoy en modo Plan, así que no creé ni modifiqué archivos. Para ejecutarlo, **pasá a un agente de implementación (Build)** y arrancamos por el `paso11g`; después la renumeración 12/13/14 y el script.

Si querés, antes de implementar te armo el texto completo de las 94 explicaciones/introducciones en la conversación para que las revises, sin escribir archivos.



No puedo escribir archivos mientras sigo en **modo Plan**. Para hacerlo, cambiá a un agente de implementación (**Build**) y lo ejecuto de una sola vez.

Cuando estés en Build, voy a crear/modificar **solo archivos dentro de `docs/argumentos-pasos/`**:


| Acción             | Archivo                                                                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Crear               | `paso11g-explicaciones-en-transicion.md` — con las 80 explicaciones y las 14 introducciones completas, para revisar antes de implementar. |
| Crear               | `paso12-feria-con-flask.md` — congelado, backup, `scripts/feria.sh` embebido y checklist de la feria.                                     |
| Renombrar y ajustar | `paso12-congelar-y-puesta-en-marcha.md` → `paso13-waitress-y-systemd-post-feria.md`, marcado como opcional y posterior al 16/11.          |
| Renombrar y ajustar | `paso13-docker-taller-post-feria.md` → `paso14-docker-taller-post-feria.md`, actualizando sus referencias internas.                       |

No voy a tocar nada más: ni `bd/`, ni `app/`, ni `tests/`, ni `scripts/`, ni `README.md`, ni `AGENTS.md`, ni `MEMORY.md`. Tampoco ejecuto el `paso11g`; solo dejo su documento listo para que luego lo pidas con `/feature`.

Una aclaración: al renombrar los pasos, el índice `docs/argumentos-pasos/README.md` va a quedar temporalmente desactualizado. Si querés, cuando pases a Build también actualizo **solo ese índice** por ser parte de la carpeta de pasos; si preferís que no se toque nada fuera de los `.md` de pasos, lo dejo para cuando ejecutemos cada paso.



Listo. Dejé armados los documentos de los pasos, sin tocar código, seeds, migraciones ni scripts.

## Archivos en `docs/argumentos-pasos/`

**Nuevo — `paso11g-explicaciones-en-transicion.md`** (515 líneas)

- Propone `tema.introduccion` y `pregunta.explicacion`, la migración `bd/migraciones/20261113_explicaciones-e-introducciones.sql`, el cambio en `schema.sql` y la regeneración de `bd/escape_room_7b2026_completa.sql`.
- Contiene el borrador completo para revisión: **14 introducciones** y **80 explicaciones** (20 inicial, 30 intermedio, 30 avanzado), en texto plano, sin `;`, sin comillas simples y sin HTML.
- Define `obtener_aprendizaje_estacion()`, el pase en las dos ramas de `transicion()`, la card de la transición con **enunciado + respuesta elegida + explicación**, y los campos en `/admin`.
- Los conteos siguen en `5/14/80/240/9`; la respuesta correcta solo aparece después de completar la estación.

**Nuevo — `paso12-feria-con-flask.md`**

- Feria del 16/11 con `flask --app app run --debug --host=0.0.0.0`.
- Contenido congelado, `.env`, backup/restauración y checklist de red/notebook.
- Incluye el contenido completo de `scripts/feria.sh`: crea `feria2026/`, instala dependencias solo si faltan y arranca Flask en `0.0.0.0:5000`.
- Simulacro con 3 notebooks y el televisor, y runbook del día de la feria.

**Nuevo — `paso13-waitress-y-systemd-post-feria.md`**

- Ahora es opcional y posterior a la feria.
- Conserva los escenarios A/B/C, la ficha del servidor, waitress en `8000`, systemd con `Restart=always` y las verificaciones.

**Renombrado — `paso14-docker-taller-post-feria.md`**

- Antiguo `paso13` de Docker, con referencias actualizadas a `paso12` y `paso13`.

**Actualizado — `README.md`**

- Índice y tabla de ruta: `11g → 12 → 13 → 14`.
- Bloque G incluye `11g`; H es waitress/systemd; I es Docker.

## Verificación hecha sobre los documentos

- Introducciones: 14. Explicaciones: 20 + 30 + 30.
- Ningún texto propuesto tiene `;`, `'` ni `<`, y ninguno supera los 600 caracteres.
- Tablas markdown bien formadas.

## Pendiente

- `paso11g` **no se ejecutó**: queda para cuando lo pidas con `/feature @docs/argumentos-pasos/paso11g-explicaciones-en-transicion.md`.
- No actualicé `MEMORY.md`, `README.md` raíz ni `AGENTS.md`, según lo acordado.
- Quedaron referencias viejas fuera de esta carpeta que hay que sincronizar al implementar: `docs/guia-de-estudio-para-estudiantes.md` (líneas 359-360), `docs/instalacion-servidor-escuela.md` (línea 3), `docs/primeros-pasos.md` (Pedido 12) y `MEMORY.md`.
- Sigue pendiente la ficha real del servidor de la escuela para los escenarios B y C del `paso13`.


`paso11g` ya estaba implementado; en esta pasada verifiqué el estado completo y cerré la documentación que faltaba.

## Verificación realizada

- **Esquema**: `tema.introduccion` y `pregunta.explicacion` existen en `bd/schema.sql`.
- **Migración**: `bd/migraciones/20261113_explicaciones-e-introducciones.sql` es idempotente (usa `information_schema` + `PREPARE`) y se aplicó dos veces sin error.
- **Contenido en la base real** (con respaldo previo y sin intentos activos):
  - `5` estaciones, `14` temas, `80` preguntas, `240` respuestas, `9` claves de configuración.
  - `14/14` introducciones cargadas.
  - `inicial 20/20`, `intermedio 30/30`, `avanzado 30/30` explicaciones.
  - `0` intentos activos.
- **Pantalla**: `transicion.html` muestra la card **Lo que aprendieron** con las introducciones por tema y, por pregunta, enunciado, respuesta elegida y explicación. La estación no contiene ni la explicación ni la respuesta correcta.
- **Admin**: ambos campos se editan como `textarea` opcionales y persisten; la baja lógica los conserva.
- **Pruebas**: `pytest -q` ejecutado dos veces seguidas → **105 passed** en ambas.

## Documentación actualizada

- `AGENTS.md`: modelo de datos, flujo de transición, decisión **66**, pruebas y regla de "Qué no hacer".
- `MEMORY.md`: entrada del `paso11g` con conteos, respaldo y estado real.
- `docs/guia-de-estudio-para-estudiantes.md`: card de aprendizaje y mapa de pasos actualizado.
- `docs/argumentos-pasos/README.md`: `paso11g` en **hecho**.
- `docs/argumentos-pasos/paso11g-explicaciones-en-transicion.md`: estado, criterios de aceptación marcados y total de tests.
- Corregí referencias antiguas a `paso12-congelar-y-puesta-en-marcha.md` y `paso13-docker-taller-post-feria.md` en la guía, `docs/instalacion-servidor-escuela.md` y `MEMORY.md`.

## Pendientes que no bloquean

- Revisión visual manual en móvil de la transición (el layout es una columna y no tapa los botones).
- Completa la ficha del servidor de la escuela (distribución y versión) para el `paso12`/`paso13`.
- No hay commit porque el directorio **no es un repositorio git**.


# Plan del `paso12` — Feria con el servidor de Flask

No modifiqué ningún archivo. Solo hice verificaciones de lectura sobre el proyecto y la base real.

## 0. Estado actual verificado


| Control                        | Resultado                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------- |
| Contenido                      | `5` estaciones, `14` temas, `80` preguntas, `240` respuestas, `9` claves de configuración        |
| Preguntas por nivel            | `inicial 20`, `intermedio 30`, `avanzado 30`                                                      |
| Niveles habilitados            | `intermedio = 1`, `avanzado = 1`; `inicial` siempre disponible                                    |
| Introducciones / explicaciones | `14/14` y `80/80`                                                                                 |
| Intentos activos               | `0`                                                                                               |
| `.env`                         | Existe, permisos `600`, valores reales: secreto de 64 caracteres, hash `scrypt`, usuario `jconde` |
| `.gitignore`                   | **No** incluye `feria2026/`                                                                       |
| `scripts/feria.sh`             | **No existe**                                                                                     |
| `feria2026/`                   | **No existe**                                                                                     |
| Entorno                        | MySQL `8.0.46`, Python `3.10.12`, Ubuntu 22.04                                                    |
| Git                            | **No hay repositorio Git**, así que el commit del paso no se puede crear                         |
| IP de este entorno             | `192.168.1.29` (puede no ser la IP de la notebook de la feria)                                    |
| Última suite                  | `105 passed` según `MEMORY.md`; se vuelve a correr al final                                      |

## 1. Enfoque general

El paso es **infra + documentación**, no de código de la app. La idea es:

1. Congelar el contenido que ya está cargado y verificado.
2. Probar de verdad el respaldo y la restauración.
3. Confirmar que el `.env` real está bien y no se versiona.
4. Crear `scripts/feria.sh` como único comando de arranque.
5. Probar el arranque local y dejar el ensayo de 3 notebooks + televisor como checklist manual.
6. Documentar el día de la feria.

**No se toca** `app/`, `tests/`, `bd/`, `requirements.txt`, el esquema ni la lógica del juego. Tampoco se reescriben `scripts/backup.sh` ni `scripts/restaurar.sh`: se usan y se prueban.

## 2. Fases de implementación

### Fase 1 — Congelar el contenido

- Reconfirmar por SQL los conteos `5/14/80/240/9` y que no haya intentos con `fecha_fin IS NULL`.
- Revisar en `/admin/cobertura` que las tres columnas estén en verde.
- Revisar en `/admin/dificultades` que estén habilitados los tres niveles.
- Revisar descripciones de `intermedio`/`avanzado` y las introducciones/explicaciones del `paso11g`.
- Jugar una partida completa de cada nivel y confirmar que cada una entra al ranking de su nivel.
- Anotar **fecha de congelamiento**, niveles habilitados y resultado.

**Regla importante:** después de congelar no se vuelven a ejecutar los seeds, porque pisan lo editado desde `/admin`. Si hay que cambiar contenido, se hace antes de congelar, con backup previo y volviendo a probar.

### Fase 2 — Backup y restauración reales

Usar los scripts existentes, sin reescribirlos:

```bash
./scripts/backup.sh /tmp/opencode/backups-feria
./scripts/restaurar.sh /tmp/opencode/backups-feria/respaldo-....sql
```

Verificar:

- El volcado se crea con permisos `600` y no está vacío.
- La restauración crea una base `_restore_...` y devuelve `5/14/80/240/9`.
- También se verifican `14` introducciones, `80` explicaciones y los niveles en `1`.
- `restaurar.sh` **se niega** a pisar `escape_room_7b2026` sin `--force`.
- La base temporal de prueba se elimina al terminar.
- El respaldo se copia además a un pendrive o a la nube. No alcanza con dejarlo solo en la notebook.

### Fase 3 — `.env` real

El `.env` actual ya parece real y tiene permisos `600`. El plan es **verificarlo, no sobreescribirlo**:

- Confirmar que `FLASK_SECRET_KEY` no es el placeholder y tiene longitud suficiente.
- Confirmar que `ADMIN_PASSWORD_HASH` es un hash `scrypt` y que el login de `/admin` funciona con la clave real.
- Confirmar que no está versionado (no hay Git, pero `.gitignore` ya lo excluye).
- Verificar que el usuario de MySQL tenga permisos para la base real, `_test` y `_restore_%`.

Si se decide rotar el secreto o el hash, se hace **antes** de la feria: rotar `FLASK_SECRET_KEY` invalida las sesiones de los equipos y los obliga a reingresar el ID.

### Fase 4 — Crear `scripts/feria.sh`

Archivo nuevo con el contenido del paso, más algunos refuerzos sin cambiar el comportamiento:

- Verificar que exista `python3` y que `python3 -m venv` funcione; si falla, mensaje claro sobre `python3-venv`.
- Crear `feria2026/` solo si no existe.
- Probar `import flask, pymysql, dotenv`; instalar `requirements.txt` solo si falta algo.
- Detectar la IP con `hostname -I` **sin que un fallo corte el script** (`|| true`).
- Mostrar todas las IPs o al menos la primera, con la aclaración de que hay que usar la de la red del aula.
- Avisar si `.env` no tiene permisos `600`.
- Ejecutar al final:
  ```bash
  exec "$PYTHON" -m flask --app app run --debug --host=0.0.0.0 "$@"
  ```
- Quedar ejecutable con `chmod 755`.

También:

- Agregar `feria2026/` a `.gitignore`.
- Crear el entorno **ahora**, con Internet, para que el día de la feria no haya que instalar nada.
- Verificar que una segunda ejecución **no reinstale** dependencias.
- Probar `bash -n scripts/feria.sh` y, si está disponible, `shellcheck`.

### Fase 5 — Prueba local de arranque

- Levantar con `./scripts/feria.sh`.
- Probar `/salud` en `127.0.0.1:5000` y en la IP de red.
- Probar `/ranking`, `/estadisticas` y el login de `/admin`.
- Reiniciar y confirmar que no reinstala y que la app vuelve a levantar.
- Correr `pytest -q` y confirmar que sigue en **105 tests**.
- Verificar que no haya referencias a CDN ni recursos externos.

### Fase 6 — Ensayo con 3 notebooks y televisor

Checklist manual:

- Notebook enchufada, sin suspensión ni apagado de pantalla.
- IP anotada y, si se puede, reserva DHCP o IP fija.
- Puerto `5000` permitido en la red del aula.
- Las 3 notebooks y el televisor en la misma red.
- Reloj y zona horaria correctos: MySQL es la fuente de tiempo.
- `.env` con permisos `600`.
- Sin Internet: Bootstrap, audio, imágenes y gráficos locales.
- 3 equipos jugando a la vez, idealmente uno por nivel.
- Televisor con `/ranking` en pantalla completa y actualizándose.
- Cortar Internet y repetir una estación.
- Reiniciar MySQL y confirmar que la app se reconecta.
- Cronometrar el arranque desde cero.

Si no se consiguen físicamente las 3 notebooks y el televisor, **no voy a declarar el criterio como cumplido**: queda documentado como verificación manual pendiente, con la prueba local y el checklist listos.

### Fase 7 — Cierre documental

- Actualizar `README.md`, la guía de instalación, la guía de estudiantes y `MEMORY.md`.
- Marcar el `paso12` como `hecho` en el índice y en su archivo.
- Dejar anotado que no se pudo hacer el commit por no haber repositorio Git.

## 3. Archivos que se van a modificar


| Archivo                                           | Tipo                       | Qué cambia                                                                                                                                                                                             |
| --------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/feria.sh`                                | **Nuevo**                  | Script de arranque con venv `feria2026/`, chequeo de `.env`, IP y Flask en `0.0.0.0:5000`.                                                                                                              |
| `.gitignore`                                      | Modificado                 | Agrega `feria2026/`.                                                                                                                                                                                    |
| `README.md`                                       | Modificado                 | Sección 9: `./scripts/feria.sh` como arranque recomendado, primer arranque con Internet, arranques posteriores sin Internet, terminal abierta, puerto `5000`. Sección 10: respaldo probado y destino. |
| `docs/instalacion-y-puesta-en-funcionamiento.md`  | Modificado                 | §10.3/§10.4 con la prueba real de backup/restauración, §10.5 con fecha de congelamiento, §13.5 y §15 con `./scripts/feria.sh` y el checklist del día.                                            |
| `docs/guia-de-estudio-para-estudiantes.md`        | Modificado                 | §9: mencionar `./scripts/feria.sh` como atajo, manteniendo el comando manual para entender qué hace.                                                                                                  |
| `docs/tecnologias.md`                             | Modificado, si corresponde | Agregar `./scripts/feria.sh` al comando de arranque de la feria.                                                                                                                                        |
| `docs/dejar-funcionando-proyecto-luego-clone.md`  | Modificado, si corresponde | Mencionar el script en la puesta en marcha de la feria.                                                                                                                                                 |
| `docs/argumentos-pasos/paso12-feria-con-flask.md` | Modificado                 | Agregar `## Estado`, marcar criterios cumplidos y anotar resultados reales (fecha, IP, niveles, backup, ensayo).                                                                                        |
| `docs/argumentos-pasos/README.md`                 | Modificado                 | `paso12` pasa de `pendiente` a `hecho`.                                                                                                                                                                 |
| `docs/primeros-pasos.md`                          | Modificado, opcional       | El Pedido 12 todavía dice “documentar el arranque con waitress”; corregirlo para que la feria sea con Flask y waitress quede post-feria.                                                             |
| `AGENTS.md`                                       | Modificado                 | Decisiones 67 y 68, comandos, estructura, pruebas y “Qué no hacer”.                                                                                                                                  |
| `MEMORY.md`                                       | Modificado                 | Entrada nueva del paso, fecha, estado de la feria, respaldo, IP, niveles y próximo paso.                                                                                                               |

**No se modifican:** `app/`, `tests/`, `bd/`, `requirements.txt`, `scripts/backup.sh`, `scripts/restaurar.sh`, `.env.example` ni la base real (salvo la prueba de restauración en una base temporal).

## 4. Casos límite y decisiones que necesito de vos

1. **¿Rotamos el secreto y el hash del `.env`?**
   Recomendación: **no**, porque ya son reales, el `.env` está en `600` y no está versionado. Rotar el secreto obliga a todos los equipos a reingresar el ID.
2. **¿Las partidas de congelamiento se juegan en la base real o en una base descartable?**
   Recomendación: en una base descartable restaurada del backup, para que el ranking real de la feria arranque limpio. Si se juegan en la real, quedan intentos históricos con un equipo de prueba.
3. **¿El equipo de prueba queda en el ranking?**
   Recomendación: dejarlo como intento histórico, con un nombre claro tipo `PRUEBA FERIA`, y no borrarlo. No conviene borrar filas históricas. Si querés que no aparezca, se juega en la base descartable.
4. **¿Se puede hacer el ensayo físico con 3 notebooks y el televisor?**
   Si no se puede, lo dejo como verificación manual pendiente y hago solo la prueba local + `curl` desde otra máquina. No voy a marcar ese criterio como cumplido sin haberlo hecho.
5. **¿Mantenemos `--debug` o agregamos `--no-reload`?**
   Recomendación: mantener exactamente `--debug`, como pide la decisión 65. `--no-reload` daría más estabilidad, pero se aparta del comando acordado.
6. **¿Creamos `feria2026/` ahora o el día de la feria?**
   Recomendación: crearlo ahora, con Internet, para que el día de la feria no dependa de `pip`. El script igualmente lo crea solo si falta.
7. **¿Dónde guardamos el backup?**
   Recomendación: `$HOME/backups-escaperoom` o `/tmp/opencode/backups-feria`, más una copia en pendrive/nube. Evitar `bd/backups/` como único lugar porque está ignorado y se puede perder con el proyecto.
8. **¿Seguimos con `MYSQL_USER=jconde` o creamos un usuario `escaperoom`?**
   Recomendación: para la feria, dejar `jconde` que ya funciona. Crear el usuario dedicado queda para la puesta en producción posterior.
9. **¿El `.gitignore` solo agrega `feria2026/` o también otros artefactos de la feria?**
   Recomendación: solo `feria2026/`. Los backups ya están cubiertos por `bd/backups/` y no se van a guardar ahí.
10. **¿Actualizamos el checklist en `docs/instalacion-y-puesta-en-funcionamiento.md` §15 o creamos `docs/checklist-feria.md`?**
    Recomendación: actualizar el §15 existente, para no sumar otro archivo.
11. **¿Corregimos `docs/primeros-pasos.md` (Pedido 12) que todavía habla de waitress?**
    Recomendación: sí, es una corrección mínima de coherencia con la decisión 65.

## 5. Qué actualizaría en `AGENTS.md`

- **Decisión 67 — Arranque de la feria con `scripts/feria.sh`:**

  - venv propio en `feria2026/`, ignorado por Git;
  - `.env` real con permisos `600`;
  - no usa `source .env` por los `$` del hash;
  - crea el entorno e instala solo si falta;
  - muestra la IP y levanta Flask en `0.0.0.0:5000`;
  - no usa waitress, systemd ni Docker;
  - primer arranque con Internet, siguientes sin Internet;
  - terminal abierta durante toda la feria.
- **Decisión 68 — Congelamiento y respaldo de la feria:**

  - fecha de congelamiento y conteos `5/14/80/240/9`;
  - los seeds no se reejecutan después de congelar;
  - backup generado y **restaurado** en base temporal antes de la feria;
  - el respaldo se guarda también fuera de la notebook;
  - no se restaura sobre la base real sin `--force` consciente;
  - las partidas de prueba quedan como históricas o se juegan en base descartable.
- **Comandos:** agregar

  ```bash
  chmod +x scripts/feria.sh
  ./scripts/feria.sh
  ```
- **Estructura:** agregar `scripts/feria.sh`, `scripts/backup.sh` y `scripts/restaurar.sh` al árbol sugerido.
- **Pruebas y verificación:** agregar bullets para:

  - arranque con `./scripts/feria.sh`;
  - `/salud` en local y en red;
  - segunda ejecución sin reinstalar;
  - `feria2026/` ignorado;
  - backup restaurado con `5/14/80/240/9`;
  - negativa de `restaurar.sh` a pisar la base real;
  - `./scripts/feria.sh` sin CDN ni recursos externos.
- **Qué no hacer:** agregar

  - no versionar `feria2026/`;
  - no reejecutar seeds después de congelar;
  - no dejar el único backup en la notebook;
  - no reemplazar el arranque de la feria por waitress ni Docker.

## 6. Qué actualizaría en `MEMORY.md`

Al principio, una entrada nueva con:

- Fecha del paso y fecha de congelamiento.
- Conteos `5/14/80/240/9`, niveles habilitados y `0` intentos activos.
- `.env` real, `600`, sin rotación (o con rotación, si se decide).
- `scripts/feria.sh` creado, `feria2026/` creado e ignorado.
- IP de la notebook, puerto `5000` y tiempo de arranque medido.
- Ruta del backup, base temporal usada y resultado de la restauración.
- Resultado del ensayo con 3 notebooks y televisor, o “pendiente manual”.
- `pytest` con 105 tests.
- Documentos actualizados.
- Aclaración de que no se pudo hacer el commit por no haber repositorio Git.

En **“Próximo paso”**, pasar al `paso13` (waitress y systemd post-feria), dejando claro que la feria del 16/11/2026 se corre con Flask y que la ficha del servidor de la escuela sigue pendiente para los escenarios B/C del `paso13`.

## 7. Orden de ejecución propuesto

1. Reconfirmar base y contenido.
2. Congelar y jugar las partidas de prueba.
3. Backup y restauración.
4. Verificar `.env`.
5. Crear `scripts/feria.sh` y `feria2026/`.
6. Prueba local de arranque y `/salud`.
7. Ensayo físico o checklist manual.
8. Actualizar documentación, `AGENTS.md` y `MEMORY.md`.
9. Correr `pytest -q` una última vez.

## 8. Lo que necesito antes de empezar

- Tu aprobación del plan.
- Respuesta a las decisiones 1 a 11, sobre todo:
  - rotar o no `.env`;
  - base real o descartable para las partidas de congelamiento;
  - si hay o no ensayo físico con 3 notebooks y televisor;
  - si mantengo `--debug` tal cual.

Con eso apruebo el arranque y recién ahí empiezo a crear `scripts/feria.sh` y a tocar los archivos de documentación.



Listo. Cerré el `paso12` y dejé todo verificado.

## Qué quedó hecho

**Estado y congelamiento**

- Base real `escape_room_7b2026` intacta: `5/14/80/240/9`, `inicial 20` / `intermedio 30` / `avanzado 30`, ambos niveles avanzados en `1`, `0` intentos activos, 14 introducciones y 80 explicaciones.
- Partidas de control por nivel jugadas en la base descartable `escape_room_7b2026_ensayo` (cada una entró a su ranking) y base eliminada. El ranking real quedó limpio.
- `.env` verificado: modo `600`, secreto de 64 caracteres, hash `scrypt` válido, `MYSQL_USER=jconde`, `MYSQL_DB=escape_room_7b2026`. No se rotó.

**Arranque de la feria**

- `scripts/feria.sh` (755): valida `.env` y `python3`, avisa si `.env` no está en `600`, crea `feria2026/`, instala solo si faltan `flask`/`pymysql`/`dotenv`, muestra la IP con el puerto real y ejecuta `python -m flask --app app run --debug --host=0.0.0.0`.
- Primer arranque: 13 s (instaló). Segundo: 2 s sin reinstalar.
- `/salud` `200` en `127.0.0.1` y en la IP de red; `/ranking` y `/estadisticas` `200`.
- `feria2026/` agregado a `.gitignore`.

**Respaldo y restauración**

- Respaldo real `respaldo-escape_room_7b2026-20261114-233156.sql` (68 KB, `600`) vía `scripts/backup.sh`.
- Restaurado en una base limpia: `5/14/80/240/9`, 14 introducciones, 80 explicaciones. `restaurar.sh` rechaza la base real sin `--force` (exit 1).
- **Bug corregido** en `scripts/restaurar.sh`: el nombre por defecto de la base temporal usaba guion (`AAAAMMDD-HHMMSS`) y la validación solo admite `[a-z0-9_]`. Ahora es `<MYSQL_DB>_restore_AAAAMMDD_HHMMSS`, con referencias actualizadas en `README.md`, `docs/instalacion-servidor-escuela.md` y el `paso12`. Los nombres de archivo de respaldo conservan el guion, que es correcto.

**Documentación**

- Actualizados: `README.md` (§7.4, §9, §10), `docs/instalacion-y-puesta-en-funcionamiento.md` (encabezado, respaldo, checklist y día de la feria), `docs/guia-de-estudio-para-estudiantes.md` (§9), `docs/tecnologias.md`, `docs/dejar-funcionando-proyecto-luego-clone.md`, `docs/primeros-pasos.md` (Pedido 12 y Paso 10), `docs/argumentos-pasos/paso12-feria-con-flask.md` (estado, resultado y aceptación), `docs/argumentos-pasos/README.md` (`paso12` = hecho), `AGENTS.md` (estructura, decisiones 67/68, comandos, pruebas y “Qué no hacer”) y `MEMORY.md` (fecha 14/11, entrada nueva y próximo paso).

**Verificación**

- `pytest -q` → **105 passed**.
- 0 enlaces relativos roto en los documentos tocados.
- No se tocaron `app/`, `tests/`, `bd/` ni el esquema.

## Pendiente operativo

1. Copiar el respaldo a un pendrive o a la nube (hoy está fuera del repo, en `/tmp/opencode/backups-feria/`).
2. Opcional: repetir `./scripts/feria.sh` en la notebook de la feria.
3. Sin repositorio Git en el directorio, **no se pudo crear el commit** `docs: feria con flask y respaldo`. Queda anotado en el `paso12` y en `MEMORY.md`.
4. El `paso13` (waitress + systemd) sigue esperando la ficha del servidor de la escuela (distro/versión).



Perfecto, tomo las seis recomendaciones. Este es el plan cerrado.

## 1. Documento nuevo: `docs/material-de-estudio-y-control.md`

Se genera leyendo la base real **solo en lectura** (14 introducciones, 80 preguntas, 240 opciones). No se toca esquema, seeds ni contenido.

Estructura:

```markdown
# Material de estudio y control — Escape Room 7.º B 2026

> Documento para estudiar y controlar el contenido del juego.
> Contiene las respuestas correctas: no se enlaza desde la app
> y no se usa durante la partida.

## Cómo usar este material
## Contenido (índice por estación)

## Estación 1: Redes
### Tema: IP
Introducción (texto de `tema.introduccion`).

#### Nivel inicial
1. **¿Qué significa IP?**
   - Internet personal
   - **Internet Protocol** ✅
   - Información privada
   *Explicación:* texto de `pregunta.explicacion`.
...
## Anexo: cobertura estación × tema × nivel
```

- Orden: estación → tema → nivel (`inicial`, `intermedio`, `avanzado`), porque la introducción aplica a los tres niveles.
- La correcta va en negrita con ✅ y la explicación debajo.
- Anexo final con la tabla de control: temas y preguntas por estación, más totales (`5/14/80`, `20/30/30`).
- Nota de mantenimiento: si se edita contenido en `/admin`, hay que regenerar el MD y los PDFs.

## 2. Documento de proceso: `docs/como-se-hizo-el-proyecto.md`

Con el relato que pasaste, ordenado así:

1. Punto de partida: documento con la idea, las reglas y los formularios del nivel inicial, más el prototipo del ranking.
2. Ampliación de reglas para sacar ambigüedades y `docs/escape-room.md` como fuente de verdad.
3. `AGENTS.md` + `MEMORY.md`: reglas permanentes y estado persistente; cómo interactúan.
4. Comando `/feature` (`.opencode/commands/feature.md`): reglas que se aplican a cada pedido.
5. Guion de pasos en `docs/argumentos-pasos/` y su `README.md`.
6. Ciclo real: `/feature pasoNN.md` en plan → revisión de dudas → build → verificación → commit indicado.
7. Ajustes menores en build después de probar la app.
8. Resultado: Flask + MySQL, 105 tests, contenido congelado y feria del 16/11/2026.
   Incluye tabla de pasos con estado final.

## 3. Enlaces y decisiones

- `README.md`: sumar ambos documentos al índice y una sección corta **Documentación en PDF**.
- `docs/guia-de-estudio-para-estudiantes.md`: enlazar el material en §8.3 y el proceso en §8.6, con la advertencia de respuestas.
- `AGENTS.md`: decisión nueva (material con respuestas, para estudio y control, fuera de la app; PDFs versionados en `docs/pdf/` y regenerables con el script) y `docs/pdf/` en el árbol de estructura.
- `MEMORY.md`: entrada del 15/11/2026 y próximo paso actualizado.

## 4. PDFs: `scripts/generar-pdfs.sh` + `docs/pdf/`

- **Herramientas ya instaladas:** `pandoc` + Chrome headless. Sin dependencias nuevas.
- **Pipeline por archivo:** `pandoc -f gfm` → HTML autocontenido con CSS de impresión A4 → `google-chrome --headless=new --print-to-pdf`.
- **CSS de impresión:** A4, márgenes, tipografía legible, tablas con bordes y sin cortar filas, bloques de código con salto de línea, `base href` para que las imágenes relativas de `navegacion-capturas.md` y los pasos salgan bien.
- **Salida espejada:** `docs/pdf/README.pdf`, `docs/pdf/AGENTS.pdf`, `docs/pdf/docs/guia-de-estudio-para-estudiantes.pdf`, `docs/pdf/docs/argumentos-pasos/paso01-esqueleto-flask.pdf`, `docs/pdf/sql/descripcion-de-la-base-de-datos.pdf`, etc.
- **Índice:** `docs/pdf/00-indice.pdf` con títulos y enlaces a los 45 PDFs.
- **Alcance:** los 45 MD de documentación (docs, `README.md`, `sql/` y también `AGENTS.md` y `MEMORY.md`). Quedan afuera `.agents/`, `.opencode/` y `.pytest_cache/`.
- **Script:** acepta archivos puntuales o sin argumentos para generar todo; crea el índice solo; limpia temporales; avisa si falta `pandoc` o Chrome.

## 5. Verificación

- `pdfinfo`: 46 PDFs (45 + índice), todos con al menos 1 página y tamaño mayor a 5 KB.
- `pdftotext`: el material nuevo contiene las 14 introducciones y las 80 explicaciones; `navegacion-capturas` sale con sus imágenes.
- El índice lista los 45 archivos y todos los destinos existen.
- No quedan archivos temporales ni procesos de Chrome colgados.
- `pytest -q` al final como sanidad (no cambia código, pero confirma que no se rompió nada).
- Informe de peso total de `docs/pdf/` para decidir si conviene comprimir.

## Notas

- Los PDFs suman peso (las capturas son ~5 MB), por eso van a `docs/pdf/` versionado, como elegiste.
- El material contiene respuestas: no se enlaza desde la app y queda advertido arriba de todo.
- Sin Git en el directorio, no habrá commit; queda anotado en `MEMORY.md`.
- Si preferís otro nombre para el documento (`docs/material-de-estudio-y-control.md`), decímelo antes de empezar.

Está listo para ejecutar, pero sigo en modo plan. **Cambiá a modo build** y lo implemento en ese orden.



Terminé lo que quedaba del plan.

## Qué completé en esta última tanda

**`docs/guia-de-estudio-para-estudiantes.md`**

- §8.1: nueva fila “Entender cómo se hizo el proyecto”.
- §8.3: agregué `docs/material-de-estudio-y-control.md` marcado 🔴, con la advertencia de que contiene todas las respuestas y que no se lee si se va a jugar.
- §8.6: agregué `docs/como-se-hizo-el-proyecto.md` como documentación de proceso.
- §12: documenté `docs/pdf/` (un PDF por `.md` con la ruta espejada + `00-indice.pdf`), el script `./scripts/generar-pdfs.sh` y la aclaración de que incluye el material con respuestas.

**`MEMORY.md`**

- Fecha actualizada a 15/11/2026 y entrada nueva con el material de estudio, el documento de proceso, el pipeline de PDFs, las verificaciones y el resultado de `pytest`.
- “Próximo paso” ahora recuerda regenerar los PDFs si cambia un `.md` o el contenido desde `/admin`.

**PDFs regenerados** (los que habían quedado viejos por las ediciones): `AGENTS.pdf`, `README.pdf`, `guia-de-estudio-para-estudiantes.pdf`, `MEMORY.pdf` y el índice.

## Verificación

- **48 archivos en `docs/pdf/`**: 47 PDFs + `00-indice.pdf`, 16 MB.
- **Ningún PDF desactualizado** respecto de su `.md` de origen.
- **0 enlaces internos rotos** en todos los `.md` del proyecto.
- El índice lista los documentos nuevos (“Cómo se hizo el proyecto”, “Material de estudio y control…”).
- La app **no referencia** el material con respuestas ni el documento de proceso (`grep` en `app/` sin resultados).
- **`pytest -q`: 105 passed** (57 s).
- La base real no se tocó.

## Pendiente (no depende del código)

- **No hay repositorio Git**, así que no se pueden crear los commits (`docs: feria con flask y respaldo`, ni el de los documentos/PDFs).
- Copiar el respaldo `respaldo-escape_room_7b2026-20261114-233156.sql` a un pendrive o a la nube: hoy sigue solo en la notebook.
- La ficha del servidor de la escuela (distribución y versión) para el `paso13` posterior a la feria.


Listo. Actualicé el documento y regeneré su PDF.

## Cambios en `sql/descripcion-de-la-base-de-datos.md`

**Parte 1 (cómo está pensada la base)**

- Nuevo párrafo: cada tema guarda `introduccion` y cada pregunta guarda `explicacion`; son texto plano, no son pistas, no se usan durante la partida y se leen solo en la card **Lo que aprendieron** de la transición, con la estación completada.

**Parte 2 (detalle de tablas)**

- `tema`: fila nueva `introduccion` · `TEXT` · nulo sí · `NULL` · “texto plano que presenta el tema en la transición… no se muestra en la estación”. Aclaración de que los 14 temas activos tienen introducción cargada.
- `pregunta`: fila nueva `explicacion` · `TEXT` · nulo sí · `NULL` · “justifica la respuesta correcta… no se envía a la estación”. Aclaración de las 80 preguntas con explicación (20/30/30).

**“Reglas que la base no impone”**

- La estación nunca recibe la explicación ni la respuesta correcta.
- La transición muestra la respuesta que el equipo eligió en `respuesta_elegida`, no la que hoy esté marcada como `correcta`.

Ambas columnas coinciden con `bd/schema.sql` y con la migración `bd/migraciones/20261113_explicaciones-e-introducciones.sql`.

## PDF

- `docs/pdf/sql/descripcion-de-la-base-de-datos.pdf` regenerado con `./scripts/generar-pdfs.sh`: **6 páginas, A4**, y el texto extraído ya incluye `introduccion` y `explicacion`.
- El índice `docs/pdf/00-indice.pdf` se regeneró en la misma corrida.
- No quedan PDFs desactualizados respecto de su `.md` y hay **0 enlaces internos rotos**.

También dejé registrada la actualización en `MEMORY.md` (y regeneré su PDF). No toqué código, base de datos ni tests; la suite sigue en 105 pruebas pasadas de la corrida anterior.

Nota: no pude leer el PDF que adjuntaste (no tengo soporte de entrada para PDFs), así que verifiqué contra el esquema real y regeneré el archivo desde el `.md` actualizado.



Decisión cerrada: **600 preguntas, 2400 respuestas y 600 pistas**. Te dejo el plan definitivo.

## Alcance final


| Concepto                   | Cantidad                                  |
| ---------------------------- | ------------------------------------------- |
| Estaciones                 | 5                                         |
| Temas                      | 10 (2 por estación, máximo permitido 4) |
| Preguntas por tema y nivel | 20                                        |
| Preguntas totales          | 600 (200 por nivel)                       |
| Respuestas                 | 2400 (4 por pregunta, 1 correcta)         |
| Introducciones de tema     | 10                                        |
| Explicaciones              | 600                                       |
| Pistas en papel            | 600 (1 por pregunta)                      |

Cada estación sortea sus 4 preguntas de un banco de 40 por nivel, garantizando al menos 1 de cada uno de sus 2 temas. Rejugabilidad enorme.

## Cómo queda la base

- Nombre: `escape_room_redes_2026`. La base original no se toca.
- Esquema: se reutiliza `bd/schema.sql` con el nombre reemplazado. **No** se duplica el archivo.
- Seeds: `bd/contenido/redes-extendidas/001_inicial.sql`, `002_intermedio.sql`, `003_avanzado.sql` + `README.md`.
- IDs desde 1 (es otra base, no hay riesgo de choque): estaciones 1–5, temas 1–10, preguntas 1–600, respuestas 1–2400.
- `configuracion`: las mismas 9 claves. Los 240 segundos de estación quedan igual, ajustables desde `/admin` si en el aula ves que el contenido extendido necesita más aire.
- Jugar: `MYSQL_DB=escape_room_redes_2026 ./scripts/feria.sh`
- **Cero cambios de código**: la app ya es agnóstica al contenido y el título queda "Escape Room 7.º B 2026" como pediste.

## Barra de calidad de una pregunta

Para que veas el nivel que voy a mantener, este es el molde:

> **Tema:** Direccionamiento IP · **Nivel:** intermedio
> **Título:** ¿Qué indica la máscara 255.255.255.0 junto a una dirección IPv4?
> **Descripción:** La máscara acompaña a la dirección IP y marca dónde termina la parte de red.
> **Opciones:** a) Que los tres primeros octetos identifican la red y el último al equipo ✅ · b) Que el equipo puede usar cualquier dirección de Internet · c) Que la red admite 254 redes distintas · d) Que la dirección es privada y no sale a Internet
> **Explicación:** La máscara 255.255.255.0 tiene 24 bits en 1, así que los tres primeros octetos identifican la red y el último identifica al equipo. Por eso esa red admite 254 hosts utilizables. No indica si la dirección es privada ni limita la salida a Internet.
> **Pista:** Contá cuántos octetos quedan fijados por la máscara y cuántos libres.

Todos los textos sin `;`, sin HTML, en rioplatense, y sin nombrar ni parafrasear la respuesta correcta en la descripción.

## Entrega por etapas

600 preguntas con explicación y pista no salen de una sola pasada con calidad pareja. Propongo 15 tandas de contenido, cada una con verificación:

1. **Infraestructura**: crear la base, cargar esquema, estaciones, temas, configuración y cobertura en rojo. Verificar que `/admin/cobertura` y `/admin/dificultades` responden.
2. **Estación 1, nivel inicial** (40 preguntas): cargar y jugar una partida real de esa estación.
3. **Estaciones 2 a 5, nivel inicial** (160): nivel `inicial` completo y habilitable.
4. **Nivel intermedio**, estación por estación (4 tandas de 40).
5. **Nivel avanzado**, estación por estación (4 tandas de 40).
6. **Pistas** de las 600 preguntas, en documento aparte.
7. **Cierre**: documento de estudio generado desde la base, guía de adaptación, README/AGENTS/MEMORY, PDFs y `pytest`.

Te reporto al final de cada tanda qué quedó cargado. Si alguna tanda no te convence, se corrige ahí y no arrastro el error a las siguientes.

## Documentos nuevos

1. `docs/material/conexiones-de-redes-extendidas/material-de-estudio-y-control.md` — **generado desde la base en solo lectura**, no escrito a mano, como el actual. 10 introducciones y 600 preguntas con la correcta en ✅, la explicación y el anexo de cobertura. Contiene respuestas: no se enlaza desde la app.
2. `docs/material/conexiones-de-redes-extendidas/pistas-del-juego-redes.md` — las 600 pistas numeradas por estación y nivel, sin revelar la respuesta.
3. `docs/material/como-adaptar-el-escape-room.md` — la guía de adaptación: qué es fijo y qué es variable, cómo se arma un seed, cómo se crea una base paralela, cómo se verifica la cobertura, cómo se prueba una partida completa y los errores típicos. Usa este escenario como ejemplo real.

Los tres entran solos al índice de PDFs porque `generar-pdfs.sh` recorre todo `.md`.

## Verificación al cerrar

- `pytest -q` sigue en verde (los tests cargan solo `bd/seeds/`, así que no los afecta).
- Cobertura verde en las 5 estaciones para los 3 niveles.
- Una partida completa por nivel en la base nueva.
- Backup y restauración del esquema nuevo, sin tocar `escape_room_7b2026`.
- Confirmar que el HTML de la estación no contiene respuestas correctas.

## Antes de arrancar necesito dos cosas

1. **Cambiá de agente a modo build**, porque en plan mode no puedo crear ni modificar archivos.
2. Dos permisos chicos, que son archivos nuevos:
   - `scripts/redes.sh`, un ayudante que crea la base `escape_room_redes_2026` desde `bd/schema.sql` con el nombre reemplazado y carga los tres seeds de forma idempotente. Si preferís, en vez de script lo dejo documentado como tres comandos `mysql` en el README.
   - El nombre `pistas-del-juego-redes.md` para el documento de pistas, o el que vos quieras.

Un aviso honesto sobre el tamaño: 600 preguntas es un trabajo largo, del orden de 15 tandas. Voy a ir tanda por tanda y a avisarte el avance, sin bloquearme esperando confirmación de cada una salvo que algo no cierre.



Entendido, y es la restricción más importante: **el escape room que ya funciona no se toca**. Lo dejo explícito.

## Garantías de aislamiento

No modifico:

- `app/` completo (rutas, servicios, plantillas, estáticos) — sin excepción.
- `tests/`, `scripts/`.
- `bd/schema.sql`, `bd/seeds/001–003`, `bd/escape_room_7b2026_completa.sql`, `bd/migraciones/`.
- La base `escape_room_7b2026` ni su contenido.

`bd/schema.sql` solo se **lee** para crear la base nueva con el nombre reemplazado; el archivo queda intacto. El juego de la feria sigue funcionando exactamente igual con `./scripts/feria.sh` y `pytest` sigue en 105 pruebas.

Todo lo nuevo vive en dos lugares:

```
bd/contenido/redes-extendidas/
  001_inicial.sql
  002_intermedio.sql
  003_avanzado.sql
  README.md          # los comandos de carga
docs/material/
  conexiones-de-redes-extendidas/material-de-estudio-y-control.md
  conexiones-de-redes-extendidas/pistas-del-juego-redes.md
  como-adaptar-el-escape-room.md
```

## Comandos documentados, sin script

En `bd/contenido/redes-extendidas/README.md`, cuatro líneas (esquema + 3 seeds), con cada seed llevando su propio `USE escape_room_redes_2026;` como los actuales:

```bash
sed 's/escape_room_7b2026/escape_room_redes_2026/g' bd/schema.sql | mysql -u <usuario> -p
mysql -u <usuario> -p < bd/contenido/redes-extendidas/001_inicial.sql
mysql -u <usuario> -p < bd/contenido/redes-extendidas/002_intermedio.sql
mysql -u <usuario> -p < bd/contenido/redes-extendidas/003_avanzado.sql
```

Y para jugar: `MYSQL_DB=escape_room_redes_2026 ./scripts/feria.sh`

Se lo deja documentado también en la guía de adaptación, que es el otro lugar donde alguien va a buscarlo.

## Un detalle que conviene saber

Al cambiar de base con la misma sesión de navegador, la cookie puede traer un `intento_id` que no existe en la base nueva. Para probar el escenario de redes conviene abrir una ventana privada o cerrar sesión antes. Lo dejo anotado en el README del contenido, porque es la clase de cosa que hace perder diez minutos en el aula.

## PDFs sin tocar los existentes

`generar-pdfs.sh` acepta archivos como argumento, así que lo corro **solo con los tres documentos nuevos**. Eso deja intactos los PDFs actuales, pero reescribe `docs/pdf/00-indice.pdf` para sumar las tres entradas nuevas. Si preferís que el índice tampoco se toque, me avisás y no regenero PDFs: los `.md` quedan y los PDFs se generan cuando vos quieras.

## Lo único que me falta decidir

¿Puedo agregar una sección corta al `README.md` principal (y a `MEMORY.md`) que diga que existe este segundo contenido y cómo se carga?

- **Sí**: quedan dos párrafos, sin tocar nada de lo existente, y el proyecto siguiente encuentra el escenario de redes.
- **No**: todo queda aislado en `bd/contenido/redes-extendidas/README.md` y `docs/material/`, y quien no sepa de la carpeta no se entera.

Yo recomiendo que sí, porque `AGENTS.md` ya pide mantener `MEMORY.md` al día y sin esa nota la segunda base queda invisible. Pero es tu llamada y no la hago sin tu ok.

Con eso resuelto, el plan queda cerrado: 5 estaciones, 10 temas, 600 preguntas, 2400 respuestas, 600 pistas, tres documentos nuevos y cero cambios al juego actual. **Cambiá de agente a build mode** cuando quieras que empiece por la infraestructura y la estación 1 del nivel inicial.



Listo. En plan mode no puedo escribir en el proyecto, así que el documento quedó en la carpeta de planes:

**`/home/usuario/.opencode/plan/paso15-escaperoom-redes.md`**

No toqué ningún archivo del proyecto.

## Qué contiene

Sigue el formato de los `paso00`–`paso14`, que viven en `docs/argumentos-pasos/`, así que el destino natural es:

```
docs/argumentos-pasos/paso15-escaperoom-redes.md
```

Secciones:

- **Importante** y **Aislamiento**: tabla de lo que no se modifica nunca (`app/`, `tests/`, `scripts/`, `bd/schema.sql`, `bd/seeds/001–003`, `bd/escape_room_7b2026_completa.sql`, `bd/migraciones/`, la base real y los PDF de origen) y la lista cerrada de archivos nuevos.
- **Estructura de contenido**: 5 estaciones con sus descripciones y 10 temas, más los contenidos de cada tema y la capa OSI/TCP-IP que cubre.
- **Volumen**: 600 preguntas, 2400 respuestas, 600 pistas.
- **Base de datos**: `escape_room_redes_2026`, los cuatro comandos `mysql` documentados (sin script), el arranque con `MYSQL_DB` y la advertencia de la cookie de sesión al cambiar de base.
- **Contrato de los seeds**: idempotencia, `ON DUPLICATE KEY UPDATE`, `INSERT IGNORE` solo en el 001, prohibido el `;` en los textos, rangos de ids reservados (preguntas 1–200 / 201–400 / 401–600, respuestas `pregunta_id * 4 - 3` a `pregunta_id * 4`) y un ejemplo completo.
- **Reglas de redacción**, **pistas en papel** y los **tres documentos** con su contenido detallado.
- **7 tandas de implementación** con su verificación, checklist de cierre, fuera de alcance, riesgos y las 7 decisiones del paso.

## Para dejarlo en el proyecto

Cambiá de agente a build mode y lo copio a `docs/argumentos-pasos/paso15-escaperoom-redes.md`. Ese único archivo nuevo es todo lo que se tocaría: no hay cambios en el juego, ni en la base, ni en los seeds, ni en el código.



Hecho. El paso quedó en el proyecto:

- **`docs/argumentos-pasos/paso15-escaperoom-redes.md`** — 467 líneas, junto a `paso00`–`paso14`.

Ningún otro archivo fue modificado. No se tocó `app/`, `tests/`, `scripts/`, `bd/schema.sql`, `bd/seeds/001–003`, la base `escape_room_7b2026` ni los PDF de `docs/material/conexiones-de-redes-extendidas/`.

## Una cosa que queda pendiente

`docs/argumentos-pasos/README.md` tiene una tabla índice con una fila por paso (líneas 98–118). `paso15` todavía no figura ahí, porque pediste no tocar nada más. La fila que correspondería, si querés que la agregue, es:

| `paso15-escaperoom-redes.md` | contenido | Post-feria | paso14 | `docs: paso15 escenario de redes extendidas` | pendiente |

Decime si la sumo y la agrego en un solo edit.



Agregado. La tabla índice de `docs/argumentos-pasos/README.md` ahora cierra con:

| `paso15-escaperoom-redes.md` | contenido | Post-feria | paso14 | `docs: paso15 escenario de redes extendidas` | pendiente |

Es un solo renglón más; no cambié nada del resto del archivo ni del proyecto. La carpeta `docs/argumentos-pasos/` queda consistente: el documento existe y el índice lo lista.
