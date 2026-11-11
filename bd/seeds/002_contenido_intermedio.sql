-- ============================================================================
-- Escape Room 7°B 2026 - Contenido de nivel intermedio
-- ============================================================================
-- Requiere haber ejecutado bd/schema.sql y bd/seeds/001_contenido_inicial.sql.
--
-- Uso:
--   mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
--
-- Es idempotente: ejecutarlo dos veces no duplica datos.
--   * Preguntas y respuestas usan ids fijos.
--     Al reejecutar se actualizan los textos, pero NO se cambia `activo`:
--     si el admin desactivó algo, sigue desactivado.
--   * No toca `configuracion` ni habilita el nivel.
--
-- Basado en docs/elaboradoChicos/ESCAPEROOM-intermedio.odt y completado con redacción propia.
-- ============================================================================

USE escape_room_7b2026;

SET NAMES utf8mb4;

START TRANSACTION;

-- ----------------------------------------------------------------------------
-- Preguntas (30 en total, 6 por estación)
-- ----------------------------------------------------------------------------
INSERT INTO pregunta (id, titulo, descripcion, tema_id, dificultad, activo) VALUES
  (1001, '¿Qué dirección IPv4 es una dirección de loopback?', NULL, 1, 'intermedio', 1),
  (1002, '¿Cuál es la función principal de una máscara de subred?', NULL, 1, 'intermedio', 1),
  (1003, '¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red?', NULL, 2, 'intermedio', 1),
  (1004, '¿Cuál es la función principal de un switch en una red LAN?', NULL, 3, 'intermedio', 1),
  (1005, '¿Qué función cumple un punto de acceso inalámbrico (Access Point)?', NULL, 4, 'intermedio', 1),
  (1006, '¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP?', NULL, 3, 'intermedio', 1),
  (1007, '¿Qué función cumple la tecnología SMART en las unidades de almacenamiento?', NULL, 6, 'intermedio', 1),
  (1008, '¿Qué puede indicar una pantalla azul recurrente en Windows?', NULL, 5, 'intermedio', 1),
  (1009, '¿Cuál es la finalidad de realizar una copia de seguridad?', NULL, 6, 'intermedio', 1),
  (1010, '¿Qué es la pasta térmica?', NULL, 5, 'intermedio', 1),
  (1011, '¿Qué tipo de mantenimiento busca evitar fallas futuras?', NULL, 5, 'intermedio', 1),
  (1012, '¿Qué significa que la memoria RAM sea volátil?', NULL, 7, 'intermedio', 1),
  (1013, '¿Para qué sirven las cookies de un navegador?', NULL, 8, 'intermedio', 1),
  (1014, '¿Qué hace el modo incógnito de un navegador?', NULL, 8, 'intermedio', 1),
  (1015, 'En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo?', NULL, 9, 'intermedio', 1),
  (1016, '¿Qué indica el dominio en una dirección web?', NULL, 9, 'intermedio', 1),
  (1017, '¿Qué es el ancho de banda?', NULL, 10, 'intermedio', 1),
  (1018, '¿Qué significa tener una latencia alta?', NULL, 10, 'intermedio', 1),
  (1019, '¿Qué es la autenticación de dos factores (2FA)?', NULL, 11, 'intermedio', 1),
  (1020, '¿Para qué sirve un gestor de contraseñas?', NULL, 11, 'intermedio', 1),
  (1021, '¿Por qué no conviene usar la misma contraseña en varios sitios?', NULL, 11, 'intermedio', 1),
  (1022, '¿Qué es el smishing?', NULL, 12, 'intermedio', 1),
  (1023, '¿Qué es el vishing?', NULL, 12, 'intermedio', 1),
  (1024, 'Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer?', NULL, 12, 'intermedio', 1),
  (1025, '¿Qué es un proceso?', NULL, 13, 'intermedio', 1),
  (1026, '¿Qué hace el sistema de archivos?', NULL, 13, 'intermedio', 1),
  (1027, '¿Para qué sirven los permisos de usuario?', NULL, 13, 'intermedio', 1),
  (1028, '¿Por qué conviene instalar las actualizaciones del sistema?', NULL, 13, 'intermedio', 1),
  (1029, '¿Qué son los permisos de una aplicación móvil?', NULL, 14, 'intermedio', 1),
  (1030, '¿Cuál es la diferencia principal entre Android e iOS?', NULL, 14, 'intermedio', 1)
ON DUPLICATE KEY UPDATE
  titulo = VALUES(titulo),
  descripcion = VALUES(descripcion),
  tema_id = VALUES(tema_id),
  dificultad = VALUES(dificultad);

-- ----------------------------------------------------------------------------
-- Respuestas (3 opciones por pregunta, una sola correcta)
-- ----------------------------------------------------------------------------
INSERT INTO respuesta (id, contenido, correcta, pregunta_id, activo) VALUES
  (2001, '127.0.0.1', 1, 1001, 1),
  (2002, '169.254.1.1', 0, 1001, 1),
  (2003, '192.168.1.1', 0, 1001, 1),
  (2004, 'Identificar el fabricante del equipo', 0, 1002, 1),
  (2005, 'Diferenciar la parte de red y la parte de host de una dirección IP', 1, 1002, 1),
  (2006, 'Aumentar la velocidad de la conexión', 0, 1002, 1),
  (2007, 'DNS', 0, 1003, 1),
  (2008, 'DHCP', 1, 1003, 1),
  (2009, 'FTP', 0, 1003, 1),
  (2010, 'Conectar la red local a Internet obligatoriamente', 0, 1004, 1),
  (2011, 'Conectar dispositivos dentro de una red local y enviar los datos al dispositivo correspondiente', 1, 1004, 1),
  (2012, 'Convertir señales digitales en sonido', 0, 1004, 1),
  (2013, 'Almacenar los archivos de los usuarios', 0, 1005, 1),
  (2014, 'Conectar dispositivos inalámbricos a una red cableada', 1, 1005, 1),
  (2015, 'Reemplazar la memoria RAM del equipo', 0, 1005, 1),
  (2016, 'DNS', 1, 1006, 1),
  (2017, 'DHCP', 0, 1006, 1),
  (2018, 'ARP', 0, 1006, 1),
  (2019, 'Controlar las conexiones WiFi', 0, 1007, 1),
  (2020, 'Supervisar indicadores de estado y anticipar posibles fallas', 1, 1007, 1),
  (2021, 'Cifrar automáticamente todos los archivos', 0, 1007, 1),
  (2022, 'Que el monitor está conectado correctamente', 0, 1008, 1),
  (2023, 'Que el router está apagado', 0, 1008, 1),
  (2024, 'Un error crítico del sistema o del hardware', 1, 1008, 1),
  (2025, 'Recuperar información ante pérdida o daño', 1, 1009, 1),
  (2026, 'Eliminar la necesidad de antivirus', 0, 1009, 1),
  (2027, 'Aumentar la velocidad de Internet', 0, 1009, 1),
  (2028, 'Un aislante que impide el paso del calor', 0, 1010, 1),
  (2029, 'Un adhesivo para fijar la memoria RAM', 0, 1010, 1),
  (2030, 'Un material que mejora la transferencia de calor entre superficies', 1, 1010, 1),
  (2031, 'Correctivo', 0, 1011, 1),
  (2032, 'Preventivo', 1, 1011, 1),
  (2033, 'Destructivo', 0, 1011, 1),
  (2034, 'Que guarda los datos para siempre', 0, 1012, 1),
  (2035, 'Que pierde su contenido al apagarse el equipo', 1, 1012, 1),
  (2036, 'Que solo funciona con Internet', 0, 1012, 1),
  (2037, 'Para acelerar el procesador', 0, 1013, 1),
  (2038, 'Para que el sitio recuerde datos de la visita, como la sesión o las preferencias', 1, 1013, 1),
  (2039, 'Para impedir que el sitio use HTTPS', 0, 1013, 1),
  (2040, 'Cifra todos los archivos del equipo', 0, 1014, 1),
  (2041, 'Impide que el proveedor de Internet vea la navegación', 0, 1014, 1),
  (2042, 'No guarda el historial ni las cookies de esa sesión en el dispositivo', 1, 1014, 1),
  (2043, 'https', 1, 1015, 1),
  (2044, 'www.escuela.edu.ar', 0, 1015, 1),
  (2045, '/aula/notas', 0, 1015, 1),
  (2046, 'La contraseña de la red WiFi', 0, 1016, 1),
  (2047, 'El nombre que identifica al sitio o servidor', 1, 1016, 1),
  (2048, 'El tipo de procesador del servidor', 0, 1016, 1),
  (2049, 'El tiempo que tarda un dato en llegar', 0, 1017, 1),
  (2050, 'La cantidad de dispositivos conectados a la red', 0, 1017, 1),
  (2051, 'La cantidad de datos que se pueden transmitir por segundo', 1, 1017, 1),
  (2052, 'Que los datos llegan más rápido', 0, 1018, 1),
  (2053, 'Que los datos tardan más en llegar a destino', 1, 1018, 1),
  (2054, 'Que se reduce el tamaño de los archivos', 0, 1018, 1),
  (2055, 'Usar dos contraseñas iguales en dos sitios', 0, 1019, 1),
  (2056, 'Un segundo paso de verificación además de la contraseña', 1, 1019, 1),
  (2057, 'Cambiar la contraseña dos veces por año', 0, 1019, 1),
  (2058, 'Para compartir las contraseñas con todos', 0, 1020, 1),
  (2059, 'Para eliminar la necesidad de usar contraseñas', 0, 1020, 1),
  (2060, 'Para guardar y generar contraseñas seguras sin memorizarlas todas', 1, 1020, 1),
  (2061, 'Porque si filtran una, pueden acceder a las demás cuentas', 1, 1021, 1),
  (2062, 'Porque ocupa más espacio en el disco', 0, 1021, 1),
  (2063, 'Porque el navegador la borra automáticamente', 0, 1021, 1),
  (2064, 'Un ataque que solo afecta impresoras', 0, 1022, 1),
  (2065, 'Un engaño por SMS o aplicación de mensajería', 1, 1022, 1),
  (2066, 'Un tipo de contraseña segura', 0, 1022, 1),
  (2067, 'Un virus que borra archivos', 0, 1023, 1),
  (2068, 'Una actualización del sistema operativo', 0, 1023, 1),
  (2069, 'Un engaño realizado por llamada telefónica', 1, 1023, 1),
  (2070, 'Hacer clic y completar los datos rápido', 0, 1024, 1),
  (2071, 'No hacer clic y verificar el pedido por un canal oficial', 1, 1024, 1),
  (2072, 'Reenviarlo a todos tus contactos', 0, 1024, 1),
  (2073, 'Un archivo guardado en el disco', 0, 1025, 1),
  (2074, 'Un programa que se está ejecutando', 1, 1025, 1),
  (2075, 'Un componente físico del procesador', 0, 1025, 1),
  (2076, 'Aumenta la memoria RAM', 0, 1026, 1),
  (2077, 'Conecta el equipo a Internet', 0, 1026, 1),
  (2078, 'Organiza y controla el acceso a archivos y carpetas', 1, 1026, 1),
  (2079, 'Para cambiar el color de la pantalla', 0, 1027, 1),
  (2080, 'Para medir la velocidad de la red', 0, 1027, 1),
  (2081, 'Para controlar quién puede leer, modificar o ejecutar archivos', 1, 1027, 1),
  (2082, 'Porque corrigen errores y mejoran la seguridad', 1, 1028, 1),
  (2083, 'Porque borran todos los archivos', 0, 1028, 1),
  (2084, 'Porque aumentan el tamaño del disco', 0, 1028, 1),
  (2085, 'Los datos del plan de Internet', 0, 1029, 1),
  (2086, 'Autorizaciones para acceder a cámara, ubicación, contactos y otros datos', 1, 1029, 1),
  (2087, 'Las contraseñas del equipo', 0, 1029, 1),
  (2088, 'Uno es un navegador y el otro un procesador', 0, 1030, 1),
  (2089, 'Android es un hardware y iOS un cable', 0, 1030, 1),
  (2090, 'Son dos sistemas operativos móviles de empresas distintas', 1, 1030, 1)
ON DUPLICATE KEY UPDATE
  contenido = VALUES(contenido),
  correcta = VALUES(correcta),
  pregunta_id = VALUES(pregunta_id);

COMMIT;

-- ----------------------------------------------------------------------------
-- Verificación rápida (opcional)
-- ----------------------------------------------------------------------------
-- SELECT e.orden, e.nombre, COUNT(p.id) AS preguntas
-- FROM estacion e
-- JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
-- JOIN pregunta p ON p.tema_id = t.id AND p.activo = 1
-- WHERE p.dificultad = 'intermedio'
-- GROUP BY e.id, e.orden, e.nombre
-- ORDER BY e.orden;
