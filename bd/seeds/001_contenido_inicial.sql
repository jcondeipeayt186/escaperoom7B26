-- ============================================================================
-- Escape Room 7°B 2026 - Contenido inicial (nivel inicial)
-- ============================================================================
-- Requiere haber ejecutado bd/schema.sql.
--
-- Uso:
--   mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
--
-- Es idempotente: ejecutarlo dos veces no duplica datos.
--   * Estaciones, temas, preguntas y respuestas usan ids fijos (ver abajo).
--     Al reejecutar se actualizan los textos, pero NO se cambia `activo`:
--     si el admin desactivó algo, sigue desactivado.
--   * La configuración usa INSERT IGNORE: nunca pisa los valores que el
--     admin haya cambiado (por ejemplo, las dificultades habilitadas).
--
-- Rangos de ids reservados para este seed:
--   estacion   1 - 5
--   tema       1 - 14
--   pregunta   1 - 20
--   respuesta  1 - 60
-- El contenido que se agregue desde /admin toma ids mayores por AUTO_INCREMENT.
--
-- Contenido basado en docs/ESCAPE ROOM.pdf, con tildes y tipeo corregidos.
-- Solo nivel `inicial`. Los niveles `intermedio` y `avanzado` se cargan con
-- los seeds 002 y 003.
-- ============================================================================

USE escape_room_7b2026;

SET NAMES utf8mb4;

START TRANSACTION;

-- ----------------------------------------------------------------------------
-- Estaciones (orden 1 a 5)
-- ----------------------------------------------------------------------------
INSERT INTO estacion (id, nombre, descripcion, orden, activo) VALUES
  (1, 'Redes', 'Conceptos de redes, direccionamiento IP, router y conexión WiFi.', 1, 1),
  (2, 'Hardware', 'Componentes físicos: procesador, memoria RAM y periféricos de entrada y salida.', 2, 1),
  (3, 'Internet', 'Navegadores web, direcciones URL y acceso a Internet.', 3, 1),
  (4, 'Ciberseguridad', 'Contraseñas seguras y reconocimiento de phishing.', 4, 1),
  (5, 'Sistemas Operativos', 'Funciones del sistema operativo y sistemas operativos móviles.', 5, 1)
ON DUPLICATE KEY UPDATE
  nombre = VALUES(nombre),
  descripcion = VALUES(descripcion),
  orden = VALUES(orden);

-- ----------------------------------------------------------------------------
-- Temas (máximo 4 por estación)
-- ----------------------------------------------------------------------------
INSERT INTO tema (id, nombre, introduccion, estacion_id, activo) VALUES
  -- Redes
  (1, 'IP', 'Una dirección IP identifica a cada dispositivo dentro de una red y permite que los datos lleguen a destino. Puede ser privada, pública o especial, como la de loopback. Conocerla ayuda a entender cómo se comunican los equipos.', 1, 1),
  (2, 'Router', 'El router es el equipo que conecta redes distintas y decide por dónde sale cada paquete. En una casa suele unir la red interna con Internet. Su trabajo es distinto del de un switch o un punto de acceso.', 1, 1),
  (3, 'Redes de computadoras', 'Una red de computadoras es un conjunto de dispositivos conectados para compartir datos y recursos. Puede ser cableada o inalámbrica y su tamaño va desde una casa hasta una empresa. Los protocolos son las reglas que ordenan esa comunicación.', 1, 1),
  (4, 'WiFi', 'El WiFi permite conectar dispositivos sin cables mediante ondas de radio. Un punto de acceso recibe la señal y la integra a la red. La seguridad de esa conexión depende del cifrado y de la clave que se use.', 1, 1),
  -- Hardware
  (5, 'Procesador', 'El procesador ejecuta las instrucciones y coordina el trabajo del equipo. Dentro tiene memorias muy rápidas y se comunica con el resto de los componentes. Su rendimiento depende de varios factores, no solo de la velocidad que muestra la caja.', 2, 1),
  (6, 'Dispositivos de entrada/salida', 'Los dispositivos de entrada permiten ingresar datos y los de salida muestran el resultado. Algunos cumplen las dos funciones, como una pantalla táctil. El almacenamiento también forma parte del hardware y guarda la información.', 2, 1),
  (7, 'Memoria RAM', 'La memoria RAM es el espacio de trabajo del equipo: guarda lo que se está usando en ese momento. Es rápida y volátil, por eso los datos se pierden al apagar. Cuando falta, el sistema puede apoyarse en el disco con la memoria virtual.', 2, 1),
  -- Internet
  (8, 'Navegadores Web', 'El navegador es el programa que pide las páginas y las muestra en pantalla. Guarda cookies, caché e historial para que la navegación sea más rápida y cómoda. También ofrece modos y opciones de privacidad que conviene conocer.', 3, 1),
  (9, 'URL', 'Una URL es la dirección de un recurso en Internet y tiene varias partes. El protocolo indica cómo se pide, el dominio identifica al servidor y la ruta señala el recurso. Los parámetros agregan datos a la consulta.', 3, 1),
  (10, 'Conectividad', 'La conectividad depende de varios factores: la velocidad, la latencia y la calidad de la red. El ancho de banda mide cuánto puede pasar y la latencia cuánto tarda. Los códigos HTTP, por su parte, informan cómo respondió el servidor.', 3, 1),
  -- Ciberseguridad
  (11, 'Contraseña', 'Las contraseñas protegen las cuentas y deben ser largas, únicas y difíciles de adivinar. Un gestor y la autenticación de dos factores ayudan a cuidarlas. Compartirlas o repetirlas aumenta el riesgo.', 4, 1),
  (12, 'Phishing', 'El phishing reúne engaños que buscan robar información haciéndose pasar por alguien confiable. Llega por correo, mensajes o llamadas y suele usar la urgencia. La ingeniería social ataca la confianza de las personas.', 4, 1),
  -- Sistemas Operativos
  (13, 'Sistema Operativo', 'El sistema operativo administra el hardware y permite ejecutar los programas. Su núcleo, el kernel, coordina la memoria, el procesador y los dispositivos. Los procesos y los hilos son parte de esa administración.', 5, 1),
  (14, 'Dispositivos Móviles', 'Los teléfonos y las tabletas usan sistemas operativos móviles como Android e iOS. Cada aplicación pide permisos para acceder a funciones y datos. Instalar solo desde la tienda oficial reduce riesgos.', 5, 1)
ON DUPLICATE KEY UPDATE
  nombre = VALUES(nombre),
  introduccion = VALUES(introduccion),
  estacion_id = VALUES(estacion_id);

-- ----------------------------------------------------------------------------
-- Preguntas (4 por estación, nivel inicial)
-- ----------------------------------------------------------------------------
INSERT INTO pregunta (id, titulo, descripcion, explicacion, tema_id, dificultad, activo) VALUES
  -- Estación 1: Redes
  (1, '¿Qué significa IP?', NULL, 'IP son las siglas de Internet Protocol, el protocolo que identifica cada dispositivo dentro de una red y permite que los datos sepan hacia dónde viajar. Cada equipo conectado recibe una dirección IP, como si fuera su número de casa.', 1, 'inicial', 1),
  (2, '¿Qué dispositivo conecta diferentes redes?', NULL, 'El router une redes distintas y decide por dónde enviar cada paquete de datos. En una casa, es el equipo que conecta la red interna con Internet. Un teclado o un monitor no cumplen esa función.', 2, 'inicial', 1),
  (3, '¿Qué es una red informática?', NULL, 'Una red informática es un conjunto de dispositivos conectados entre sí para compartir información y recursos. Pueden estar unidos por cables o por WiFi y sirven para intercambiar archivos, usar una impresora o navegar.', 3, 'inicial', 1),
  (4, '¿Qué se necesita para conectarse a una red WiFi?', NULL, 'Para entrar a una red WiFi protegida hay que conocer su contraseña o clave de seguridad. Esa clave evita que cualquier persona se conecte sin permiso. Los cables HDMI o las impresoras no tienen relación con esa conexión.', 4, 'inicial', 1),
  -- Estación 2: Hardware
  (5, '¿Qué componente es considerado el cerebro de la computadora?', NULL, 'El procesador, también llamado CPU, ejecuta las instrucciones y coordina las tareas del equipo. Por eso se lo compara con el cerebro de la computadora: sin él, el resto de los componentes no puede trabajar. El teclado y el monitor solo permiten entrar o ver información.', 5, 'inicial', 1),
  (6, '¿Cuál es un dispositivo de entrada?', NULL, 'Un dispositivo de entrada permite ingresar datos al equipo. El teclado lo hace cuando escribís y el ratón cuando movés el puntero. El monitor y el parlante son de salida, porque muestran o emiten el resultado.', 6, 'inicial', 1),
  (7, '¿Para qué sirve la memoria RAM?', NULL, 'La memoria RAM guarda los datos y los programas que se están usando en ese momento. Es muy rápida, pero al apagar el equipo su contenido se pierde. No sirve para imprimir ni para proteger la pantalla.', 7, 'inicial', 1),
  (8, '¿Cuál es un dispositivo de salida?', NULL, 'Un dispositivo de salida presenta al usuario el resultado del trabajo del equipo. El monitor muestra texto e imágenes y el parlante emite sonido. El ratón y el micrófono son de entrada.', 6, 'inicial', 1),
  -- Estación 3: Internet
  (9, '¿Qué es un navegador web?', NULL, 'Un navegador web es el programa que pide las páginas a los servidores y las muestra en pantalla. Chrome, Firefox y Edge son ejemplos. No es una parte del procesador ni un cable de red.', 8, 'inicial', 1),
  (10, '¿Cuál de estos es un navegador web?', NULL, 'Google Chrome es un navegador web: sirve para abrir sitios y navegar por Internet. Windows es un sistema operativo y la calculadora es una aplicación de cálculo. Cada programa cumple una función distinta.', 8, 'inicial', 1),
  (11, '¿Qué significa URL?', NULL, 'URL son las siglas de Uniform Resource Locator y funcionan como la dirección de una página, una imagen o un archivo en Internet. Al escribirla en el navegador, el equipo sabe qué servidor buscar y qué recurso pedir.', 9, 'inicial', 1),
  (12, '¿Qué se necesita para acceder a un sitio web público en internet?', NULL, 'Para ver un sitio público hace falta una conexión que llegue hasta el servidor donde está alojado. Sin conexión a Internet, el navegador no puede pedir esa página. Un escáner o un pendrive no reemplazan esa conexión.', 10, 'inicial', 1),
  -- Estación 4: Ciberseguridad
  (13, '¿Cómo debe ser una contraseña segura?', NULL, 'Una contraseña segura combina mayúsculas, minúsculas, números y símbolos, y tiene suficiente longitud para que no se adivine fácilmente. Evitá datos obvios como 123456 o tu nombre. Cuanto más difícil de adivinar, mejor protege la cuenta.', 11, 'inicial', 1),
  (14, '¿Qué deberías hacer con un enlace sospechoso?', NULL, 'Antes de abrir un enlace dudoso conviene comprobar quién lo envió y por qué. Se puede consultar por otro canal, como una llamada o el sitio oficial. Abrirlo o compartirlo solo aumenta el riesgo.', 12, 'inicial', 1),
  (15, '¿Qué es el phishing?', NULL, 'El phishing es un engaño que imita a una empresa o a una persona conocida para que entregues contraseñas o datos. Suele llegar por correo, mensaje o llamada. No es un programa de fotos ni una clase de monitor.', 12, 'inicial', 1),
  (16, '¿Qué conviene hacer con tus contraseñas?', NULL, 'Las contraseñas son personales y no se comparten con nadie, ni con amigos ni con desconocidos. Usar la misma en todos lados multiplica el daño si una se filtra. Guardarlas de forma segura ayuda a no tener que recordarlas de memoria.', 11, 'inicial', 1),
  -- Estación 5: Sistemas Operativos
  (17, '¿Qué es un sistema operativo?', NULL, 'Un sistema operativo es el software principal que administra el hardware y permite ejecutar los programas. Windows, Linux y Android son ejemplos. Sin él, el equipo no sabría cómo usar sus componentes.', 13, 'inicial', 1),
  (18, '¿Cuál de estos es un sistema operativo?', NULL, 'Windows es un sistema operativo: administra el equipo y sirve de base para los demás programas. Microsoft Word es un procesador de textos y Google Chrome es un navegador. Cada uno se apoya en el sistema operativo.', 13, 'inicial', 1),
  (19, '¿Para qué sirve un sistema operativo?', NULL, 'El sistema operativo reparte el procesador, la memoria y el almacenamiento entre los programas. También controla los permisos y la comunicación con los dispositivos. No se limita al color del monitor ni a escribir documentos.', 13, 'inicial', 1),
  (20, '¿Cuál de estos es un sistema operativo para celulares?', NULL, 'Android es un sistema operativo móvil, pensado para teléfonos y tabletas. PowerPoint y Excel son aplicaciones de oficina que funcionan sobre un sistema operativo. iOS es otro sistema móvil, de otra empresa.', 14, 'inicial', 1)
ON DUPLICATE KEY UPDATE
  titulo = VALUES(titulo),
  descripcion = VALUES(descripcion),
  explicacion = VALUES(explicacion),
  tema_id = VALUES(tema_id),
  dificultad = VALUES(dificultad);

-- ----------------------------------------------------------------------------
-- Respuestas (3 opciones por pregunta, una sola correcta)
-- ----------------------------------------------------------------------------
INSERT INTO respuesta (id, contenido, correcta, pregunta_id, activo) VALUES
  -- Pregunta 1
  (1, 'Internet personal', 0, 1, 1),
  (2, 'Internet Protocol', 1, 1, 1),
  (3, 'Información privada', 0, 1, 1),
  -- Pregunta 2
  (4, 'Teclado', 0, 2, 1),
  (5, 'Router', 1, 2, 1),
  (6, 'Monitor', 0, 2, 1),
  -- Pregunta 3
  (7, 'Un conjunto de dispositivos conectados', 1, 3, 1),
  (8, 'Un programa para dibujar', 0, 3, 1),
  (9, 'Una pieza de la computadora', 0, 3, 1),
  -- Pregunta 4
  (10, 'Una contraseña, si está protegida', 1, 4, 1),
  (11, 'Un cable HDMI obligatoriamente', 0, 4, 1),
  (12, 'Una impresora', 0, 4, 1),
  -- Pregunta 5
  (13, 'Teclado', 0, 5, 1),
  (14, 'Procesador', 1, 5, 1),
  (15, 'Monitor', 0, 5, 1),
  -- Pregunta 6
  (16, 'Monitor', 0, 6, 1),
  (17, 'Parlante', 0, 6, 1),
  (18, 'Teclado', 1, 6, 1),
  -- Pregunta 7
  (19, 'Guardar datos temporalmente mientras se trabaja', 1, 7, 1),
  (20, 'Imprimir documentos', 0, 7, 1),
  (21, 'Proteger físicamente la pantalla', 0, 7, 1),
  -- Pregunta 8
  (22, 'Ratón', 0, 8, 1),
  (23, 'Micrófono', 0, 8, 1),
  (24, 'Monitor', 1, 8, 1),
  -- Pregunta 9
  (25, 'Un programa para visitar páginas web', 1, 9, 1),
  (26, 'Una parte del procesador', 0, 9, 1),
  (27, 'Un cable de red', 0, 9, 1),
  -- Pregunta 10
  (28, 'Google Chrome', 1, 10, 1),
  (29, 'Windows', 0, 10, 1),
  (30, 'Calculadora', 0, 10, 1),
  -- Pregunta 11
  (31, 'Una dirección de un recurso en internet', 1, 11, 1),
  (32, 'Una memoria de computadora', 0, 11, 1),
  (33, 'Un tipo de teclado', 0, 11, 1),
  -- Pregunta 12
  (34, 'Una conexión a internet', 1, 12, 1),
  (35, 'Un escáner obligatoriamente', 0, 12, 1),
  (36, 'Un pendrive siempre', 0, 12, 1),
  -- Pregunta 13
  (37, '123456', 0, 13, 1),
  (38, 'Tu nombre solamente', 0, 13, 1),
  (39, 'Larga y difícil de adivinar', 1, 13, 1),
  -- Pregunta 14
  (40, 'Abrirlo inmediatamente', 0, 14, 1),
  (41, 'Evitar abrirlo y verificar su origen', 1, 14, 1),
  (42, 'Compartirlo con todos', 0, 14, 1),
  -- Pregunta 15
  (43, 'Un intento de engaño para robar información', 1, 15, 1),
  (44, 'Un programa para editar fotos', 0, 15, 1),
  (45, 'Una clase de monitor', 0, 15, 1),
  -- Pregunta 16
  (46, 'Compartirlas con desconocidos', 0, 16, 1),
  (47, 'Usar la misma en todos lados', 0, 16, 1),
  (48, 'Mantenerlas privadas', 1, 16, 1),
  -- Pregunta 17
  (49, 'El software que administra la computadora', 1, 17, 1),
  (50, 'Un cable de alimentación', 0, 17, 1),
  (51, 'Una aplicación para dibujar', 0, 17, 1),
  -- Pregunta 18
  (52, 'Microsoft Word', 0, 18, 1),
  (53, 'Windows', 1, 18, 1),
  (54, 'Google Chrome', 0, 18, 1),
  -- Pregunta 19
  (55, 'Administrar recursos y permitir ejecutar programas', 1, 19, 1),
  (56, 'Solo para cambiar el color del monitor', 0, 19, 1),
  (57, 'Solo para escribir documentos', 0, 19, 1),
  -- Pregunta 20
  (58, 'Android', 1, 20, 1),
  (59, 'PowerPoint', 0, 20, 1),
  (60, 'Excel', 0, 20, 1)
ON DUPLICATE KEY UPDATE
  contenido = VALUES(contenido),
  correcta = VALUES(correcta),
  pregunta_id = VALUES(pregunta_id);

-- ----------------------------------------------------------------------------
-- Configuración inicial
-- ----------------------------------------------------------------------------
-- INSERT IGNORE: si el admin ya cambió un valor, el seed no lo pisa.
INSERT IGNORE INTO configuracion (clave, valor) VALUES
  ('dificultad_intermedia_habilitada', '0'),
  ('dificultad_avanzada_habilitada', '0'),
  ('duracion_estacion_segundos', '240'),
  ('max_ayudas_estacion', '2'),
  ('max_envios_estacion', '2'),
  ('max_respuestas_incorrectas', '2'),
  ('max_integrantes_equipo', '4'),
  ('max_temas_por_estacion', '4'),
  ('preguntas_por_estacion', '4');

COMMIT;

-- ----------------------------------------------------------------------------
-- Verificación rápida (opcional)
-- ----------------------------------------------------------------------------
-- SELECT e.orden, e.nombre, COUNT(DISTINCT t.id) AS temas, COUNT(DISTINCT p.id) AS preguntas
-- FROM estacion e
-- LEFT JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
-- LEFT JOIN pregunta p ON p.tema_id = t.id AND p.dificultad = 'inicial' AND p.activo = 1
-- GROUP BY e.id, e.orden, e.nombre
-- ORDER BY e.orden;
