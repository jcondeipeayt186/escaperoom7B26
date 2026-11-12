-- ============================================================================
-- Escape Room 7°B 2026 - Esquema de base de datos (MySQL 8)
-- ============================================================================
-- Uso:
--   mysql -u <usuario> -p < bd/schema.sql
--
-- Este archivo crea la base y las tablas. No carga contenido: para eso usar
--   mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
-- o, para cargar estructura y contenido de una sola vez:
--   mysql -u <usuario> -p < bd/escape_room_7b2026_completa.sql
--
-- Convenciones:
--   * snake_case para tablas y columnas.
--   * Claves foráneas <entidad>_id.
--   * equipo, intento, respuesta_elegida e incorrecta son históricos:
--     no se borran (ni física ni lógicamente).
--   * estacion, tema, pregunta y respuesta usan borrado lógico con activo.
--   * Las fechas de juego las escribe la aplicación (no se confía en el
--     reloj del navegador). Por eso no hay DEFAULT CURRENT_TIMESTAMP en las
--     columnas que definen tiempos.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS escape_room_7b2026
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE escape_room_7b2026;

SET NAMES utf8mb4;

-- ----------------------------------------------------------------------------
-- Equipos
-- ----------------------------------------------------------------------------
-- El nombre es único (comparación sin distinguir mayúsculas ni acentos por
-- la colación utf8mb4_unicode_ci). Si un equipo repite el nombre, la
-- aplicación pide el id para continuar con el mismo equipo.
CREATE TABLE IF NOT EXISTS equipo (
  id                INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre            VARCHAR(120) NOT NULL,
  cantidad_personas TINYINT UNSIGNED NOT NULL,
  fecha_creacion    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_equipo_nombre (nombre),
  CONSTRAINT chk_equipo_cantidad CHECK (cantidad_personas BETWEEN 1 AND 4)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Contenido: estaciones, temas, preguntas y respuestas
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS estacion (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre      VARCHAR(80) NOT NULL,
  descripcion VARCHAR(255) NOT NULL DEFAULT '',
  orden       TINYINT UNSIGNED NOT NULL,
  activo      TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_estacion_orden (orden),
  UNIQUE KEY uq_estacion_nombre (nombre)
) ENGINE=InnoDB;

-- Máximo 4 temas activos por estación: se valida en /admin (no en la base).
CREATE TABLE IF NOT EXISTS tema (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre      VARCHAR(80) NOT NULL,
  estacion_id INT UNSIGNED NOT NULL,
  activo      TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_tema_estacion_nombre (estacion_id, nombre),
  CONSTRAINT fk_tema_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pregunta (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  titulo      VARCHAR(255) NOT NULL,
  descripcion TEXT NULL,
  tema_id     INT UNSIGNED NOT NULL,
  dificultad  ENUM('inicial', 'intermedio', 'avanzado') NOT NULL,
  activo      TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY idx_pregunta_tema_dificultad (tema_id, dificultad, activo),
  CONSTRAINT fk_pregunta_tema
    FOREIGN KEY (tema_id) REFERENCES tema (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS respuesta (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  contenido   VARCHAR(255) NOT NULL,
  correcta    TINYINT(1) NOT NULL DEFAULT 0,
  pregunta_id INT UNSIGNED NOT NULL,
  activo      TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY idx_respuesta_pregunta (pregunta_id, activo),
  CONSTRAINT fk_respuesta_pregunta
    FOREIGN KEY (pregunta_id) REFERENCES pregunta (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Intentos
-- ----------------------------------------------------------------------------
-- finalizado = NULL mientras el intento está en curso.
-- se_completo_ok es derivado de finalizado (no se edita a mano).
-- puntaje_obtenido guarda los segundos totales solo si finalizado = 'completo'.
CREATE TABLE IF NOT EXISTS intento (
  id                       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  equipo_id                INT UNSIGNED NOT NULL,
  dificultad               ENUM('inicial', 'intermedio', 'avanzado') NOT NULL DEFAULT 'inicial',
  fecha_inicio             DATETIME(3) NOT NULL,
  fecha_fin                DATETIME(3) NULL DEFAULT NULL,
  se_completo_ok           TINYINT(1) GENERATED ALWAYS AS (IF(finalizado = 'completo', 1, 0)) STORED,
  cantidad_ayudas          SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  puntaje_obtenido         INT UNSIGNED NULL DEFAULT NULL,
  finalizado               ENUM('completo', 'abandono', 'por_respuestas_incorrectas', 'por_tiempo') NULL DEFAULT NULL,
  ultima_estacion_visitada INT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY idx_intento_equipo (equipo_id),
  KEY idx_intento_activo (fecha_fin),
  KEY idx_intento_ranking (finalizado, fecha_inicio, fecha_fin, cantidad_ayudas),
  CONSTRAINT fk_intento_equipo
    FOREIGN KEY (equipo_id) REFERENCES equipo (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_intento_ultima_estacion
    FOREIGN KEY (ultima_estacion_visitada) REFERENCES estacion (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Detalle del intento
-- ----------------------------------------------------------------------------
-- Una fila por estación jugada. ayudas va de 0 a 2 (máximo configurable en
-- configuracion.max_ayudas_estacion).
CREATE TABLE IF NOT EXISTS intento_estacion (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  intento_id   INT UNSIGNED NOT NULL,
  estacion_id  INT UNSIGNED NOT NULL,
  fecha_inicio DATETIME(3) NOT NULL,
  fecha_fin    DATETIME(3) NULL DEFAULT NULL,
  ayudas       TINYINT UNSIGNED NOT NULL DEFAULT 0,
  completada   TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_intento_estacion (intento_id, estacion_id),
  CONSTRAINT fk_ie_intento
    FOREIGN KEY (intento_id) REFERENCES intento (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_ie_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Un envío del formulario. Permite mostrar "envíos: 1 de 2" y congelar el
-- estado al segundo envío.
CREATE TABLE IF NOT EXISTS intento_envio (
  id                     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  intento_id             INT UNSIGNED NOT NULL,
  estacion_id            INT UNSIGNED NOT NULL,
  fecha                  DATETIME(3) NOT NULL,
  respuestas_correctas   TINYINT UNSIGNED NOT NULL DEFAULT 0,
  respuestas_incorrectas TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_envio_intento_estacion (intento_id, estacion_id, fecha),
  CONSTRAINT fk_envio_intento
    FOREIGN KEY (intento_id) REFERENCES intento (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_envio_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Selección aleatoria estable de las 4 preguntas de cada estación del intento.
-- Recargar la página no cambia las preguntas.
CREATE TABLE IF NOT EXISTS intento_pregunta (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  intento_id  INT UNSIGNED NOT NULL,
  estacion_id INT UNSIGNED NOT NULL,
  pregunta_id INT UNSIGNED NOT NULL,
  orden       TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ip_intento_estacion_orden (intento_id, estacion_id, orden),
  UNIQUE KEY uq_ip_intento_estacion_pregunta (intento_id, estacion_id, pregunta_id),
  CONSTRAINT fk_ip_intento
    FOREIGN KEY (intento_id) REFERENCES intento (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_ip_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_ip_pregunta
    FOREIGN KEY (pregunta_id) REFERENCES pregunta (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT chk_ip_orden CHECK (orden BETWEEN 1 AND 4)
) ENGINE=InnoDB;

-- Registro completo de respuestas elegidas (correctas e incorrectas).
CREATE TABLE IF NOT EXISTS respuesta_elegida (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  fecha_respondida DATETIME(3) NOT NULL,
  intento_id       INT UNSIGNED NOT NULL,
  intento_envio_id INT UNSIGNED NOT NULL,
  respuesta_id     INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY idx_re_intento (intento_id),
  KEY idx_re_envio (intento_envio_id),
  KEY idx_re_respuesta (respuesta_id),
  CONSTRAINT fk_re_intento
    FOREIGN KEY (intento_id) REFERENCES intento (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_re_envio
    FOREIGN KEY (intento_envio_id) REFERENCES intento_envio (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_re_respuesta
    FOREIGN KEY (respuesta_id) REFERENCES respuesta (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Subconjunto de respuestas incorrectas. La duplicación con respuesta_elegida
-- es intencional: alimenta el HUD y las estadísticas.
CREATE TABLE IF NOT EXISTS incorrecta (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pregunta_id      INT UNSIGNED NOT NULL,
  respuesta_id     INT UNSIGNED NOT NULL,
  fecha            DATETIME(3) NOT NULL,
  intento_id       INT UNSIGNED NOT NULL,
  intento_envio_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY idx_incorrecta_intento (intento_id),
  KEY idx_incorrecta_envio (intento_envio_id),
  CONSTRAINT fk_inc_pregunta
    FOREIGN KEY (pregunta_id) REFERENCES pregunta (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inc_respuesta
    FOREIGN KEY (respuesta_id) REFERENCES respuesta (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inc_intento
    FOREIGN KEY (intento_id) REFERENCES intento (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inc_envio
    FOREIGN KEY (intento_envio_id) REFERENCES intento_envio (id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Configuración
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS configuracion (
  clave VARCHAR(80) NOT NULL,
  valor VARCHAR(255) NOT NULL,
  PRIMARY KEY (clave)
) ENGINE=InnoDB;
