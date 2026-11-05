
Estado actual (verificado recién)
MySQL está activo en 127.0.0.1:3306.
La base tiene el seed completo: 5 estaciones, 14 temas, 20 preguntas, 60 respuestas, 9 filas de configuración.
Configuración: duracion_estacion_segundos = 240, max_respuestas_incorrectas = 2, max_envios_estacion = 2, max_ayudas_estacion = 2, intermedio y avanzado deshabilitados.
0 intentos cargados: base limpia para empezar la prueba.
.venv y .env existen y están listos.

1. Levantar la app (prueba local, en esta notebook)
   Desde la raíz del repositorio:

source .venv/bin/activate
flask --app app run --debug
Queda en http://127.0.0.1:5000.

Antes de jugar, comprobá que responde y que ve la base:

curl -i http://127.0.0.1:5000/salud
Tiene que devolver 200 con {"estado": "ok", "base": "ok"}. Si devuelve 503, el problema es MySQL o las credenciales de .env, no el juego.

Para detener: Ctrl+C.

2. Si vas a probar desde otra notebook o el televisor
   El comando anterior solo escucha en localhost. Para la red local:

source .venv/bin/activate
flask --app app run --debug --host=0.0.0.0
Averiguá la IP del servidor:

hostname -I
Y desde la otra máquina entrá a http://IP-DEL-SERVIDOR:5000.

Ojo: /ranking todavía no existe. El ranking que se ve hoy es el de /juego/final. La vista de TV con polling es el paso08.

3. Antes de empezar el guion
   2 o 3 personas que no hayan visto el código; una sola observa y anota, sin ayudar.
   Cronómetro real y las pistas impresas de docs/ESCAPE ROOM.pdf.
   Una sesión de navegador por equipo. La sesión de Flask guarda equipo_id e intento_id: si abrís dos equipos en la misma ventana, se pisan. Usá ventanas de incógnito separadas o perfiles/navegadores distintos.
   Anotá el ID del equipo que aparece en el HUD: lo van a necesitar para el punto de identidad.
4. Guion de prueba (resumen operativo)
   El detalle está en docs/argumentos-pasos/paso07-prueba-manual-del-mvp.md. Lo importante a mirar:

Bienvenida: nombre nuevo, integrantes y dificultad. Solo debe ofrecer inicial. Probá cantidad 0 y 5: deben rechazarse con error inline (estado 400, sin crear nada).
Identidad: salí y volvé a entrar con el mismo nombre → debe pedir el ID. Probá un ID incorrecto (debe rechazarse) y el correcto (debe reanudar el intento activo, no crear otro).
Estación 1:
HUD completo: equipo, ID, estación, contador general subiendo, contador de estación bajando, ayudas, incorrectas, envíos.
Recargá (F5): mismas 4 preguntas, mismo orden, mismos tiempos.
Pedí Ayuda 1 y Ayuda 2: al llegar a 2 se deshabilitan. La app no debe mostrar texto de pista.
Enviá incompleto: debe rechazar sin registrar envío.
Enviá con 1 incorrecta: sigue, suma incorrecta y envío.
Enviá con 2 incorrectas: eliminación inmediata.
Aviso de 30 segundos: texto titilante y audio (el audio necesita un clic previo; si está bloqueado, el aviso visual igual debe verse). Este punto tarda ~3:30; si querés probarlo rápido, se puede bajar duracion_estacion_segundos en la base solo con 0 intentos activos y después restaurarla a 240.
Recorrido: completar las 5 estaciones. Verificar orden, que no se pueda saltar por URL (/juego/estacion/3 estando en la 1 debe redirigir), que la transición muestre Continuar y que el cronómetro de la siguiente arranque recién al presionarlo.
Abandono: probar botón, confirmación y pantalla de eliminación. Distinguir los tres motivos: por_tiempo, por_respuestas_incorrectas, abandono.
Final y ranking: completar un intento; ver tiempo total, ayudas, posición, top 10 y ranking completo con filtros. Confirmar que el intento eliminado no aparece.
Pantalla chica y grande: HUD legible en notebook y de pie frente a un televisor.
5. Consultas útiles para verificar sin tocar datos
Con el usuario de MySQL de tu .env:

mysql -u <usuario></usuario> -p escape_room_7b2026 -e "
SELECT id, nombre, cantidad_personas FROM equipo;
SELECT id, equipo_id, dificultad, finalizado, puntaje_obtenido,
       TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin) AS segundos
FROM intento ORDER BY id;
SELECT * FROM incorrecta ORDER BY id;
SELECT id, intento_id, estacion_id, fecha_inicio, fecha_fin, ayudas, completada
FROM intento_estacion ORDER BY id;
SELECT * FROM intento_envio ORDER BY id;"
Sirven para confirmar: que no se duplicó el equipo, que se guardaron las 4 respuestas elegidas, que las incorrectas están en incorrecta, y que puntaje_obtenido coincide con los segundos reales.

6. Al terminar
   Cargá las observaciones en la planilla del paso07 (#, paso, qué esperaba, qué pasó, ¿bloquea?).
   No hace falta limpiar la base ahora: los intentos de prueba quedan como históricos y los eliminados no ensucian el ranking. Si querés dejar la base limpia para la feria, lo definimos después (es borrado de datos, así que lo confirmás vos).
   Si aparece algo bloqueante, cambiá a un agente de implementación (yo estoy en modo plan y no puedo modificar archivos). La corrección va con commit fix: correcciones del MVP, y después actualizamos MEMORY.md con el resultado.
