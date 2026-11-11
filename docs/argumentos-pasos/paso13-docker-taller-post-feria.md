# Paso 13 — Docker para un taller post-feria

> **Origen:** pedido posterior a la feria, para trabajar con los estudiantes.
> **Tipo:** infra (educativo).
> **Requiere:** `paso12` aprobado y la feria del 16/11 terminada.
> **Commit:** `build: docker compose para taller post-feria`.
>
> **Antes de empezar:** leé `AGENTS.md` (decisiones 60 y "Qué no hacer"),
> `README.md` y `docs/instalacion-y-puesta-en-funcionamiento.md`.

## Importante

Este paso **no forma parte del camino de la feria**. La feria se resuelve con
waitress y systemd según el `paso12`. Docker es una actividad posterior para
mostrar a los estudiantes cómo se empaqueta una aplicación real.

No ejecutar este paso antes del 16/11 ni reemplazar con Docker la instalación
que ya funciona en el aula.

## Contexto

La aplicación ya corre con Flask + MySQL y tiene un `requirements.txt` con
waitress. Para el taller se busca que los estudiantes entiendan:

- Qué es una imagen y qué es un contenedor.
- Cómo se conectan dos servicios (aplicación y base) por red.
- Cómo se pasan variables de entorno sin copiar el `.env` dentro de la imagen.
- Para qué sirve un volumen y por qué los seeds solo corren la primera vez.

## Objetivo

Dejar la aplicación dockerizada para un taller guiado después de la feria, sin
cambiar el funcionamiento normal ni la instalación del aula.

## Alcance

### Archivos nuevos

- `Dockerfile`:
  - Base `python:3.12-slim`.
  - Instalar `requirements.txt`.
  - Copiar `app/` y los archivos necesarios.
  - Usuario no root.
  - Arranque con `waitress-serve --listen=0.0.0.0:8000 app:create_app`.
  - Sin `.env` ni credenciales dentro de la imagen.
- `compose.yaml`:
  - Servicio `db` con `mysql:8`, volumen persistente, `healthcheck` y los
    scripts de `bd/` montados en `/docker-entrypoint-initdb.d` en este orden:
    `01_schema.sql` y `02_contenido_inicial.sql`.
  - Servicio `web` con build local, `depends_on` con `condition:
    service_healthy`, puerto `${WEB_PORT:-8000}:8000` y variables de entorno.
  - `MYSQL_HOST=db` explícito para el servicio `web`, aunque el `.env` tenga
    `127.0.0.1`.
- `.dockerignore`: `.env`, `.venv`, `__pycache__`, `.pytest_cache`, `tests/`,
  `docs/`, `*.md` y archivos generados.
- `docs/docker.md`: guía del taller para estudiantes.

### Archivos que se actualizan

- `.env.example`: agregar `MYSQL_ROOT_PASSWORD` y `WEB_PORT`, aclarando que
  son para Docker y que no reemplazan las variables de la instalación local.
- `README.md`: sección **Docker (opcional, post-feria)** con el comando de
  arranque y la advertencia de no usarlo en la feria.
- `MEMORY.md`: estado del paso cuando se implemente.

### Fuera de alcance

- Cambiar `requirements.txt` para agregar Docker: Docker es una herramienta,
  no una dependencia Python.
- Cambiar el esquema, los seeds o el código de la aplicación.
- Publicar imágenes en un registry.
- Nginx, HTTPS, CI/CD o Kubernetes.
- Usar Docker en la feria o migrar la base real.

## Reglas del taller

- La base del contenedor es **independiente** de la base real de la feria.
- El `.env` no se copia a la imagen ni se commitea.
- Los scripts de `/docker-entrypoint-initdb.d` solo se ejecutan cuando el
  volumen de MySQL se crea por primera vez.
- Para reiniciar la base desde cero se usa `docker compose down -v`; hay que
  avisar que eso **borra** los datos del volumen.
- El servicio `web` espera a que `db` esté saludable antes de arrancar.
- La aplicación se sirve con waitress, igual que en el camino del `paso12`.
- Los seeds deben ser los mismos que se usan localmente; no duplicar contenido
  dentro del `Dockerfile`.

## Estructura sugerida de `compose.yaml`

```yaml
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DB}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - datos_mysql:/var/lib/mysql
      - ./bd/schema.sql:/docker-entrypoint-initdb.d/01_schema.sql:ro
      - ./bd/seeds/001_contenido_inicial.sql:/docker-entrypoint-initdb.d/02_contenido_inicial.sql:ro
      - ./bd/seeds/002_contenido_intermedio.sql:/docker-entrypoint-initdb.d/03_contenido_intermedio.sql:ro
      - ./bd/seeds/003_contenido_avanzado.sql:/docker-entrypoint-initdb.d/04_contenido_avanzado.sql:ro
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 20

  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      FLASK_SECRET_KEY: ${FLASK_SECRET_KEY}
      MYSQL_HOST: db
      MYSQL_PORT: 3306
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DB: ${MYSQL_DB}
      ADMIN_USER: ${ADMIN_USER}
      ADMIN_PASSWORD_HASH: ${ADMIN_PASSWORD_HASH}
    ports:
      - "${WEB_PORT:-8000}:8000"

volumes:
  datos_mysql:
```

El `compose.yaml` definitivo puede ajustar nombres y detalles, pero debe
mantener estas ideas: dos servicios, healthcheck, volumen y variables fuera de
la imagen.

## Criterio de aceptación

- `docker compose config` no muestra errores.
- `docker compose up --build -d` levanta `db` y `web`.
- `GET /salud` responde `200` con `{"estado":"ok","base":"ok"}`.
- El login de `/admin` funciona con el hash del `.env`.
- Se puede completar una partida y el ranking muestra el intento.
- Los conteos de los seeds coinciden con la instalación local
  (`5` estaciones, `14` temas, `80` preguntas, `240` respuestas, `9` filas de
  configuración).
- `docker compose down` detiene los contenedores sin borrar el volumen.
- `docker compose down -v` elimina el volumen y, al volver a levantar, los
  seeds se ejecutan de nuevo.
- La instalación del `paso12` sigue funcionando sin Docker.
- No se agregaron CDN, credenciales ni dependencias nuevas a la aplicación.

## Verificación

```bash
docker compose config
docker compose up --build -d
curl -i http://localhost:8000/salud
docker compose logs web
docker compose exec db mysql -u root -p -e "
  USE escape_room_7b2026;
  SELECT COUNT(*) FROM estacion;
  SELECT COUNT(*) FROM tema;
  SELECT COUNT(*) FROM pregunta;
  SELECT COUNT(*) FROM respuesta;
"
docker compose down
```

Prueba de reinicio del volumen:

```bash
docker compose down -v
docker compose up -d
```

Verificar a mano:

- `/` muestra la bienvenida.
- `/admin` pide login y acepta el usuario del `.env`.
- Una partida completa de `inicial` termina y aparece en `/ranking`.
- Al bajar el volumen y volver a levantar, la base queda con los seeds.

## Ojo con

- `MYSQL_HOST=127.0.0.1` dentro de un contenedor apunta al propio contenedor,
  no a la base. Usar `db`.
- No copiar `.env` en el `Dockerfile`.
- Los seeds solo corren al crear el volumen; no se reejecutan solos.
- El `schema.sql` y los seeds crean y usan `escape_room_7b2026`; si se cambia
  `MYSQL_DB`, hay que revisar los scripts o mantener ese nombre.
- Si más adelante existe `bd/seeds/002_contenido_intermedio.sql`, agregarlo al
  volumen como `03_contenido_intermedio.sql` para que el taller tenga la misma
  cobertura que la feria.
- No usar este paso para reemplazar waitress/systemd mientras la feria esté
  en curso.
