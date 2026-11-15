-- ============================================================================
-- Escape Room 7°B 2026 - Migración: explicaciones e introducciones
-- ============================================================================
-- Agrega las dos columnas de contenido que usa la pantalla de transición:
--   * tema.introduccion
--   * pregunta.explicacion
--
-- Uso:
--   mysql -u <usuario> -p < bd/migraciones/20261113_explicaciones-e-introducciones.sql
--
-- Es idempotente: se puede ejecutar dos veces sin error y no toca datos.
-- Consulta information_schema antes de agregar cada columna para que funcione
-- en MySQL 8 sin depender de ADD COLUMN IF NOT EXISTS.
-- Después de aplicarla hay que reejecutar los seeds para cargar el contenido.
-- ============================================================================

USE escape_room_7b2026;

SET NAMES utf8mb4;

SET @existe_introduccion = (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'tema'
    AND COLUMN_NAME = 'introduccion'
);

SET @sql_introduccion = IF(
  @existe_introduccion = 0,
  'ALTER TABLE tema ADD COLUMN introduccion TEXT NULL AFTER nombre',
  'SELECT 1'
);

PREPARE stmt_introduccion FROM @sql_introduccion;
EXECUTE stmt_introduccion;
DEALLOCATE PREPARE stmt_introduccion;

SET @existe_explicacion = (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'pregunta'
    AND COLUMN_NAME = 'explicacion'
);

SET @sql_explicacion = IF(
  @existe_explicacion = 0,
  'ALTER TABLE pregunta ADD COLUMN explicacion TEXT NULL AFTER descripcion',
  'SELECT 1'
);

PREPARE stmt_explicacion FROM @sql_explicacion;
EXECUTE stmt_explicacion;
DEALLOCATE PREPARE stmt_explicacion;
