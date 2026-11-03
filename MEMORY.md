# Estado actual del repositorio

Fecha: 3/11/2026

- Todavía **no existe la aplicación Flask**: no hay código de app, `requirements.txt` ni tests. Ya existen el esquema (`bd/schema.sql`) y el seed de contenido inicial (`bd/seeds/001_contenido_inicial.sql`).
- `docs/proyectoEscapeRoom-7B.md` es la presentación breve del proyecto (título y reseña de cinco párrafos), útil para el stand o para compartir con la comunidad escolar.
- Documentos de apoyo: `sql/descripcion-de-la-base-de-datos.md` (modelo y tablas), `docs/navegacion-por-app.md` (pantallas y rutas), `docs/primeros-pasos.md` (hoja de ruta y guion de pedidos), `docs/tecnologias.md` (stack explicado con ejemplos y glosario) y `docs/instalacion-y-puesta-en-funcionamiento.md` (servidor Ubuntu y acceso desde las notebooks). Si contradicen a `docs/escape-room.md`, manda `docs/escape-room.md`.
- `docs/argumentos-pasos/` contiene el guion operativo: un archivo por paso (`paso00` a `paso12`) derivado de la sección 11 de `docs/primeros-pasos.md`, pensado para usarse con `/feature`. El `README.md` de esa carpeta explica los tipos de paso (código, test, infra, manual) y cómo se avanza. `paso00` verifica la base, `paso01` a `paso06` construyen el MVP, `paso07` es una prueba manual con personas y `paso08` a `paso12` agregan ranking público, admin, tests y puesta en marcha.
- `docs/src/` contiene **prototipos de referencia**, no código de producción. No copiarlos tal cual.
- `docs/src/index.html` es una maqueta de una sola página: no cumple el requisito de una página por estación, no tiene temporizadores, audio, dificultad, administración ni persistencia.
- `docs/src/ranking-puntajes/` mezcla un prototipo HTML con restos de SQLite (`basededatos.py`, `.db`) y PHP (`contador.php`). **No forman parte del stack** y no deben reutilizarse. El HTML sirve solo como referencia visual.
- `docs/instalacion-y-puesta-en-funcionamiento.md` está completo: servidor Ubuntu, MySQL, venv, waitress, systemd, firewall, acceso desde las notebooks y una sección específica para usar una notebook personal (por ejemplo, la del docente) como servidor. Los comandos de la app quedan pendientes de probar contra el scaffold real.
- No modificar los archivos de `docs/` salvo que el pedido sea explícitamente sobre la documentación.

## Próximo paso

Implementar los pasos del guion `docs/argumentos-pasos/` en orden:

1. `paso00-verificar-base-y-contenido.md` — ejecutar `bd/schema.sql` y el seed dos veces, y verificar los conteos. No crea archivos del repo ni lleva commit.
2. `paso01-esqueleto-flask.md` — scaffold Flask, `requirements.txt`, `.env.example`, `.gitignore`, app factory, conexión a MySQL con PyMySQL, blueprints vacíos, `templates/base.html` con Bootstrap local y ruta `/salud`.

Cada paso se lanza con `/feature @docs/argumentos-pasos/<archivo>.md`, se revisa el plan, se implementa, se verifica el criterio de aceptación y se hace el commit indicado. El `paso07` es manual: lo hacen personas jugando, no el agente.
