# Estado actual del repositorio

Fecha: 4/11/2026

- **`paso02` implementado: bienvenida e identidad del equipo.** `GET/POST /`, `GET/POST /equipo/identificar` y `GET /juego` (tablero provisorio) ya funcionan. La bienvenida pide nombre, cantidad de integrantes (1–4) y dificultad; solo ofrece las dificultades habilitadas en `configuracion`. Un nombre nuevo crea `equipo` e `intento` en una transacción; un nombre existente deriva a identificación por ID sin duplicar el equipo. Si el equipo tiene un intento activo se reanuda; si no, se crea uno nuevo con `ultima_estacion_visitada` en la estación activa con `orden = 1`. La sesión guarda solo `equipo_id` e `intento_id` y el servidor vuelve a validarlos en cada request. El HUD mínimo muestra `Equipo N.º X · nombre` y la estación actual. La lógica de dominio vive en `app/servicios/` (`configuracion.py`, `equipos.py`, `estaciones.py`); las plantillas nuevas son `bienvenida.html`, `identificar.html`, `juego.html` y `_hud.html`.
- Se verificó el criterio del `paso02` con el cliente de pruebas y MySQL: alta con nombre normalizado, variante con mayúsculas/acentos y espacios repetidos que pide ID, ID inexistente rechazado sin revelar datos, cantidad 0/5 y dificultad deshabilitada rechazadas con `400`, recarga que conserva el intento, reanudación del intento activo y creación de uno nuevo al cerrarlo. Los datos de prueba se borraron al terminar.
- **La aplicación Flask tiene el esqueleto del `paso01`.** Existe `app/` con la app factory `create_app()`, `app/db.py` (PyMySQL, cursor de diccionarios, conexión por request y helper `transaction()`), los blueprints `juego`, `ranking`, `estadisticas` y `admin`, las plantillas `base.html`, `404.html` y `500.html`, Bootstrap 5.3.3 local en `app/static/vendor/bootstrap/` y la ruta `GET /salud`.
- `requirements.txt` fija Flask 3.1.3, `PyMySQL[rsa]` 1.2.3, python-dotenv 1.2.4, pytest 9.2.0 y waitress 3.0.2. `.env.example` documenta las 8 variables y `.env` existe local con permisos `600` (no versionado). `.gitignore` cubre `.venv/`, `.env`, cachés de Python y volcados de base.
- `GET /salud` responde `200 {"estado":"ok","base":"ok"}` con MySQL arriba y `503` genérico si la base falla. También se verificaron las páginas 404 y 500, la ausencia de CDN y los conteos 5/14/20/60.
- Todavía no hay tests automatizados: `pytest` termina con código 5 y es lo esperado hasta el `paso11`.
- `docs/proyectoEscapeRoom-7B.md` es la presentación breve del proyecto (título y reseña de cinco párrafos), útil para el stand o para compartir con la comunidad escolar.
- Documentos de apoyo: `sql/descripcion-de-la-base-de-datos.md` (modelo y tablas), `docs/navegacion-por-app.md` (pantallas y rutas), `docs/primeros-pasos.md` (hoja de ruta y guion de pedidos), `docs/tecnologias.md` (stack explicado con ejemplos y glosario) y `docs/instalacion-y-puesta-en-funcionamiento.md` (servidor Ubuntu y acceso desde las notebooks). Si contradicen a `docs/escape-room.md`, manda `docs/escape-room.md`.
- `docs/argumentos-pasos/` contiene el guion operativo: un archivo por paso (`paso00` a `paso12`) derivado de la sección 11 de `docs/primeros-pasos.md`, pensado para usarse con `/feature`. El `README.md` de esa carpeta explica los tipos de paso (código, test, infra, manual) y cómo se avanza. `paso00` verifica la base, `paso01` a `paso06` construyen el MVP, `paso07` es una prueba manual con personas y `paso08` a `paso12` agregan ranking público, admin, tests y puesta en marcha.
- **`paso00` completado el 3/11/2026.** La base `escape_room_7b2026` se creó con `bd/schema.sql` y el seed se ejecutó dos veces sin duplicar filas. Pasaron todas las verificaciones de `docs/argumentos-pasos/paso00-verificar-base-y-contenido.md`: 5 estaciones, 14 temas, 20 preguntas y 60 respuestas activas; 4 preguntas `inicial` por estación; al menos 1 pregunta por tema; 3 opciones y exactamente 1 correcta por pregunta; máximo de 4 temas por estación; 9 claves en `configuracion` con las dos dificultades en `0`. No hubo cambios de código ni commit.
- `docs/src/` contiene **prototipos de referencia**, no código de producción. No copiarlos tal cual.
- `docs/src/index.html` es una maqueta de una sola página: no cumple el requisito de una página por estación, no tiene temporizadores, audio, dificultad, administración ni persistencia.
- `docs/src/ranking-puntajes/` mezcla un prototipo HTML con restos de SQLite (`basededatos.py`, `.db`) y PHP (`contador.php`). **No forman parte del stack** y no deben reutilizarse. El HTML sirve solo como referencia visual.
- `docs/instalacion-y-puesta-en-funcionamiento.md` está completo: servidor Ubuntu, MySQL, venv, waitress, systemd, firewall, acceso desde las notebooks y una sección específica para usar una notebook personal (por ejemplo, la del docente) como servidor. Los comandos de desarrollo ya se probaron contra el scaffold real; la puesta en marcha con waitress se cierra en el `paso12`.
- No modificar los archivos de `docs/` salvo que el pedido sea explícitamente sobre la documentación.

## Próximo paso

Implementar el `paso03-seleccion-de-preguntas.md` del guion `docs/argumentos-pasos/`:

```text
/feature @docs/argumentos-pasos/paso03-seleccion-de-preguntas.md
```

Objetivo: congelar en `intento_pregunta` las 4 preguntas del nivel del intento, con al menos una por tema activo y selección aleatoria estable ante recargas.

Cada paso se lanza con `/feature @docs/argumentos-pasos/<archivo>.md`, se revisa el plan, se implementa, se verifica el criterio de aceptación y se hace el commit indicado. El `paso07` es manual: lo hacen personas jugando, no el agente.
