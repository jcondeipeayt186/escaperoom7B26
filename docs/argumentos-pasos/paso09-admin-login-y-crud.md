# Paso 09 — Login, panel y CRUD del admin

> **Origen:** Pedido 9 de `docs/primeros-pasos.md` (Paso 8, primera parte).
> **Tipo:** código.
> **Requiere:** `paso08` aprobado y commiteado.
> **Commit:** `feat: panel de administración y CRUD`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Administración" y "Decisiones
> registradas"), `docs/navegacion-por-app.md` (sección 5.1 a 5.4) y
> `sql/descripcion-de-la-base-de-datos.md`.

## Contexto

El juego, el ranking público y las estadísticas funcionan. No existe el panel
de administración.

## Objetivo

Proteger `/admin`, permitir el login por variables de entorno y gestionar el
contenido con filtros, orden y borrado lógico.

## Alcance

- `GET /admin` con formulario de login.
- `POST /admin/login` y `POST /admin/logout`.
- Sesión de Flask y cierre de sesión.
- Protección de todas las rutas `/admin/*`.
- Panel `/admin/` con cards por tabla y conteos.
- Listados `/admin/<tabla>` con filtros, orden y paginación.
- Alta y edición de `estacion`, `tema`, `pregunta`, `respuesta` y
  `configuracion`.
- Baja lógica (`activo = 0`) del contenido.
- Listados de solo lectura para `equipo`, `intento`, `intento_estacion`,
  `intento_envio`, `intento_pregunta`, `respuesta_elegida` e `incorrecta`.
- Validaciones del servidor.
- Cierre de sesión por POST.

No implementar todavía la cobertura, los toggles de dificultad ni los
gráficos del panel.

## Reglas de seguridad

- Credenciales por `ADMIN_USER` y `ADMIN_PASSWORD_HASH`. Nunca hardcodear ni
  commitear.
- Comparar con `werkzeug.security.check_password_hash`.
- Error de login genérico: "Usuario o clave incorrectos", sin decir cuál
  falló.
- `/admin` no se enlaza desde ninguna página pública.
- Cookie de sesión con `httponly` y `samesite="Lax"`.
- SQL siempre parametrizado.
- Filtros y orden: validar contra una lista blanca de columnas por tabla.
  Nunca interpolar el nombre de la columna que manda el cliente.
- No mostrar el hash ni las variables de entorno.
- El cierre de sesión es POST, no GET.

## Reglas de datos

- `equipo.nombre` único y `cantidad_personas` entre 1 y 4.
- `estacion.orden` único, de 1 a 5.
- Máximo 4 temas activos por estación.
- `pregunta.dificultad` válida.
- Exactamente una respuesta correcta por pregunta.
- No borrar ni desactivar históricos: `equipo`, `intento`,
  `respuesta_elegida`, `incorrecta`, `intento_estacion`, `intento_envio` e
  `intento_pregunta`. Todos son de solo lectura.
- Cambiar la respuesta correcta de una pregunta no altera intentos ya
  finalizados: no recalcular nada.
- El borrado de contenido es lógico. Los intentos históricos siguen leyendo
  filas inactivas.

## Criterio de aceptación

- [ ] Sin sesión, cualquier `/admin/*` redirige al login.
- [ ] Con las credenciales de `.env`, el login funciona; con credenciales
      incorrectas, el mensaje es genérico.
- [ ] Cerrar sesión invalida el acceso.
- [ ] El panel lista todas las tablas con su conteo.
- [ ] Se pueden crear y editar estaciones, temas, preguntas, respuestas y
      configuración.
- [ ] Un quinto tema activo en una estación se rechaza.
- [ ] Una pregunta con 0 o 2 respuestas correctas se rechaza.
- [ ] Los históricos no se pueden borrar ni desactivar.
- [ ] Desactivar una pregunta no rompe un intento histórico.
- [ ] Ninguna página pública enlaza a `/admin`.

## Verificación

Generar el hash:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('clave-de-prueba'))"
```

Guardarlo en `.env` como `ADMIN_PASSWORD_HASH` y confirmar que `.env` no está
versionado.

Probar en una ventana de incógnito:

```bash
curl -i http://127.0.0.1:5000/admin/
curl -i http://127.0.0.1:5000/admin/estacion
```

Esperado: redirección al login.

Buscar enlaces públicos:

```bash
curl -s http://127.0.0.1:5000/ | grep -i admin
```

Esperado: sin resultados.

Después de una baja lógica:

```sql
SELECT id, titulo, activo FROM pregunta WHERE id = <id>;
SELECT COUNT(*) FROM respuesta_elegida WHERE respuesta_id IN (
  SELECT id FROM respuesta WHERE pregunta_id = <id>
);
```

Esperado: la pregunta queda `activo = 0` y las respuestas históricas siguen
ahí.

## Trampas conocidas

- `ADMIN_PASSWORD_HASH` se genera una vez y se guarda; no se compara texto
  plano.
- Si el panel usa un `<select>` de tablas, validar el nombre contra una lista
  blanca antes de armar el SQL.
- El ordenamiento por columna es el punto más fácil de inyectar SQL. Usar
  `ORDER BY` con columnas permitidas, no con texto del usuario.
- No permitir editar `intento.finalizado`, `puntaje_obtenido` ni
  `se_completo_ok` desde el CRUD.
- `se_completo_ok` es una columna generada: no se inserta ni se actualiza.
- La baja lógica no debe aplicarse a históricos aunque el formulario mande
  `activo = 0`.

## No hagas todavía

Cobertura, toggles de dificultad, intentos activos, gráficos y pruebas
automatizadas completas.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado del admin.
- Commit: `feat: panel de administración y CRUD`.
