
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
