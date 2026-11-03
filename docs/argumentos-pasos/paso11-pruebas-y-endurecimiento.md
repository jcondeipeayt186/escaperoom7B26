# Paso 11 — Pruebas automatizadas y endurecimiento

> **Origen:** Pedido 11 de `docs/primeros-pasos.md` (Paso 9).
> **Tipo:** test.
> **Requiere:** `paso10` aprobado y commiteado.
> **Commit:** `test: reglas del juego y endurecimiento`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Pruebas y verificación"),
> `docs/escape-room.md`, `docs/navegacion-por-app.md` y
> `sql/descripcion-de-la-base-de-datos.md`.

## Contexto

La app está completa y probada a mano. Falta cubrir las reglas críticas con
pruebas que se puedan repetir.

## Objetivo

Que `pytest` demuestre las reglas del juego y que no queden agujeros de
seguridad ni fugas de información.

## Alcance

- Configurar pytest con una base de prueba independiente.
- Fixtures de app, cliente y base.
- Tests de las reglas listadas abajo.
- Revisión de SQL parametrizado y de la sesión de admin.
- Implementación de CSRF en los formularios.
- Prueba de idempotencia del seed.
- Comandos reales en `README.md`.

## Base de prueba

- Base separada, por ejemplo `escape_room_7b2026_test`.
- Nunca apuntar los tests a la base de la feria ni a la de desarrollo.
- Variables de entorno de test explícitas.
- Crear el esquema una vez por sesión y limpiar entre tests.
- Como MySQL no hace rollback de DDL, limpiar las tablas históricas en orden
  inverso a las claves foráneas, o desactivar `FOREIGN_KEY_CHECKS` durante la
  limpieza.
- El seed se puede cargar con ids fijos para tener contenido estable.

## Casos a cubrir

Reglas del juego:

- Avance solo con las 4 respuestas correctas.
- Eliminación por 2 respuestas incorrectas.
- Eliminación por tiempo agotado.
- Eliminación por abandono.
- Máximo 2 envíos y bloqueo al segundo.
- Máximo 2 ayudas por estación e intento.
- Registro de todas las respuestas en `respuesta_elegida` y de las
  incorrectas en `incorrecta`.
- Selección de 4 preguntas, al menos 1 por tema activo y 4 en total.
- Con más de 4 temas, 4 temas al azar y 1 pregunta de cada uno.
- Selección estable después de recargar.
- Recarga sin reiniciar tiempos.
- Reanudación desde `ultima_estacion_visitada`.
- Ranking: tiempo ascendente, luego ayudas, luego `id`.
- Exclusión de `abandono`, `por_respuestas_incorrectas` y `por_tiempo`.
- `puntaje_obtenido` solo en completos.

Contenido y admin:

- Filtrado de preguntas por dificultad y por tema.
- Nivel no habilitable sin cobertura en alguna estación o tema.
- Toggle de dificultad bloqueado con intentos activos.
- Borrado lógico sin romper intentos históricos.
- Se rechaza un quinto tema activo.
- Se rechaza una pregunta con 0 o 2 respuestas correctas.
- `/admin` inaccesible sin login y no enlazado desde páginas públicas.
- Históricos no borrables.

Bienvenida y datos:

- Cantidad de integrantes entre 1 y 4.
- Reingreso con nombre existente: pide ID y no duplica equipo.
- Estadísticas públicas sin nombres de equipos ni respuestas correctas.
- Ausencia de la respuesta correcta en el HTML y en el JSON público.
- Seed idempotente: ejecutarlo dos veces no duplica.

## CSRF

`AGENTS.md` pide revisar CSRF pero no autoriza agregar dependencias.

- Opción recomendada: token propio en sesión, generado por request, incluido
  en un campo oculto de todos los formularios POST y validado en el servidor.
- No agregar Flask-WTF ni otra dependencia sin consultar.
- Cubrir con un test que un POST sin token se rechaza.
- El login y el logout también llevan token.

## Criterio de aceptación

- [ ] `pytest` pasa completo dos veces seguidas.
- [ ] Los tests usan una base independiente y no dejan datos de prueba.
- [ ] Están cubiertos todos los casos de la lista.
- [ ] Un POST sin token CSRF se rechaza.
- [ ] El seed es idempotente en la base de prueba.
- [ ] `README.md` tiene los comandos reales de instalación, arranque y test.
- [ ] No quedan credenciales ni `SECRET_KEY` de desarrollo en archivos
      versionados.

## Verificación

```bash
pytest -q
pytest -q
```

Después de la segunda corrida, revisar que las tablas de la base de prueba no
tengan filas de más y que la base de desarrollo no se haya tocado.

Buscar fugas:

```bash
grep -riE "correcta|password_hash|SECRET_KEY" templates static
```

Esperado: solo referencias legítimas de nombres de campo, nunca valores ni la
opción correcta marcada.

Revisar SQL:

```bash
grep -rn "execute(" app | grep -v "%s"
```

Esperado: ninguna consulta armada con f-strings o concatenación de datos del
usuario.

## Trampas conocidas

- No testear contra la base real.
- No relajar una regla para que el test pase.
- Los tests de tiempo no deben esperar 4 minutos: manipular `fecha_inicio` en
  la base o bajar `duracion_estacion_segundos` en la configuración de test.
- Las selecciones aleatorias se prueban por propiedades (4 preguntas, 1 por
  tema, sin repetir), no por un resultado fijo.
- Cuidado con el orden de limpieza por las claves foráneas.
- No dejar `SECRET_KEY` ni credenciales en `conftest.py`.

## No hagas todavía

Cambios de esquema, contenido nuevo, ni funcionalidad que no esté pedida.

## Al terminar

- Resumir archivos, comandos y resultado de `pytest`.
- Actualizar `MEMORY.md` con el estado de las pruebas.
- Commit: `test: reglas del juego y endurecimiento`.
