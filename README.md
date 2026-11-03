# Escape Room 7.º B 2026

Aplicación web para la Feria de Producciones del IPEATyM 186 Castagnari (13/11/2026).

## Documentación

- `docs/proyectoEscapeRoom-7B.md` — título y reseña breve del proyecto.
- `docs/escape-room.md` — requisitos funcionales y contenido inicial.
- `docs/primeros-pasos.md` — hoja de ruta y guion de pedidos, paso a paso.
- `docs/argumentos-pasos/` — un archivo por paso (`paso00` a `paso12`), listo para usar con `/feature`. Incluye el índice y los criterios de aceptación.
- `docs/navegacion-por-app.md` — pantallas, rutas, elementos y objetivos.
- `docs/tecnologias.md` — stack explicado: frontend, backend, base de datos y herramientas.
- `docs/instalacion-y-puesta-en-funcionamiento.md` — instalación en Ubuntu y uso desde las notebooks.
- `sql/descripcion-de-la-base-de-datos.md` — modelo de datos, tablas y consultas.
- `AGENTS.md` — decisiones registradas, modelo de datos y convenciones.

## Base de datos

El esquema y el contenido inicial ya están disponibles:

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
```

La aplicación Flask todavía no está implementada. Los comandos de arranque se agregarán cuando exista el scaffold.
