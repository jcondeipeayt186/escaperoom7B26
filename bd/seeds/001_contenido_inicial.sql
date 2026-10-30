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
-- Solo nivel `inicial`: no hay preguntas de intermedio ni avanzado todavía.
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
INSERT INTO tema (id, nombre, estacion_id, activo) VALUES
  -- Redes
  (1, 'IP', 1, 1),
  (2, 'Router', 1, 1),
  (3, 'Redes de computadoras', 1, 1),
  (4, 'WiFi', 1, 1),
  -- Hardware
  (5, 'Procesador', 2, 1),
  (6, 'Dispositivos de entrada/salida', 2, 1),
  (7, 'Memoria RAM', 2, 1),
  -- Internet
  (8, 'Navegadores Web', 3, 1),
  (9, 'URL', 3, 1),
  (10, 'Conectividad', 3, 1),
  -- Ciberseguridad
  (11, 'Contraseña', 4, 1),
  (12, 'Phishing', 4, 1),
  -- Sistemas Operativos
  (13, 'Sistema Operativo', 5, 1),
  (14, 'Dispositivos Móviles', 5, 1)
ON DUPLICATE KEY UPDATE
  nombre = VALUES(nombre),
  estacion_id = VALUES(estacion_id);

-- ----------------------------------------------------------------------------
-- Preguntas (4 por estación, nivel inicial)
-- ----------------------------------------------------------------------------
INSERT INTO pregunta (id, titulo, descripcion, tema_id, dificultad, activo) VALUES
  -- Estación 1: Redes
  (1, '¿Qué significa IP?', NULL, 1, 'inicial', 1),
  (2, '¿Qué dispositivo conecta diferentes redes?', NULL, 2, 'inicial', 1),
  (3, '¿Qué es una red informática?', NULL, 3, 'inicial', 1),
  (4, '¿Qué se necesita para conectarse a una red WiFi?', NULL, 4, 'inicial', 1),
  -- Estación 2: Hardware
  (5, '¿Qué componente es considerado el cerebro de la computadora?', NULL, 5, 'inicial', 1),
  (6, '¿Cuál es un dispositivo de entrada?', NULL, 6, 'inicial', 1),
  (7, '¿Para qué sirve la memoria RAM?', NULL, 7, 'inicial', 1),
  (8, '¿Cuál es un dispositivo de salida?', NULL, 6, 'inicial', 1),
  -- Estación 3: Internet
  (9, '¿Qué es un navegador web?', NULL, 8, 'inicial', 1),
  (10, '¿Cuál de estos es un navegador web?', NULL, 8, 'inicial', 1),
  (11, '¿Qué significa URL?', NULL, 9, 'inicial', 1),
  (12, '¿Qué se necesita para acceder a un sitio web público en internet?', NULL, 10, 'inicial', 1),
  -- Estación 4: Ciberseguridad
  (13, '¿Cómo debe ser una contraseña segura?', NULL, 11, 'inicial', 1),
  (14, '¿Qué deberías hacer con un enlace sospechoso?', NULL, 12, 'inicial', 1),
  (15, '¿Qué es el phishing?', NULL, 12, 'inicial', 1),
  (16, '¿Qué conviene hacer con tus contraseñas?', NULL, 11, 'inicial', 1),
  -- Estación 5: Sistemas Operativos
  (17, '¿Qué es un sistema operativo?', NULL, 13, 'inicial', 1),
  (18, '¿Cuál de estos es un sistema operativo?', NULL, 13, 'inicial', 1),
  (19, '¿Para qué sirve un sistema operativo?', NULL, 13, 'inicial', 1),
  (20, '¿Cuál de estos es un sistema operativo para celulares?', NULL, 14, 'inicial', 1)
ON DUPLICATE KEY UPDATE
  titulo = VALUES(titulo),
  descripcion = VALUES(descripcion),
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
