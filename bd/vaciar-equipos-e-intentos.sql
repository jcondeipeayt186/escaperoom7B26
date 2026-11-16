-- ============================================================================
-- Escape Room - Vaciar equipos, intentos y todo su detalle
-- ============================================================================
-- Uso:
--   mysql -u <usuario> -p <base> < bd/vaciar-equipos-e-intentos.sql
-- o, con confirmación y respaldo previo:
--   ./scripts/vaciar-intentos.sh
--
-- QUÉ HACE
--   Borra equipos, intentos, envíos, respuestas elegidas, incorrectas y la
--   selección de preguntas de cada intento. Deja la base lista para empezar
--   de cero, conservando todo el contenido:
--     estacion, tema, pregunta, respuesta y configuracion NO se tocan.
--
-- ADVERTENCIA
--   Borra definitivamente el ranking y las estadísticas. No se puede deshacer.
--   Generá un respaldo antes con ./scripts/backup.sh
--
-- Este archivo NO lleva USE a propósito: la base se pasa como argumento. Si se
-- ejecuta sin base, el cliente falla con "No database selected" y no borra
-- nada, que es el fallo seguro.
--
-- El orden respeta las claves foráneas, que son todas ON DELETE RESTRICT:
-- se borran primero las tablas de detalle y al final equipo.
-- ============================================================================

START TRANSACTION;

DELETE FROM incorrecta;
DELETE FROM respuesta_elegida;
DELETE FROM intento_pregunta;
DELETE FROM intento_envio;
DELETE FROM intento_estacion;
DELETE FROM intento;
DELETE FROM equipo;

COMMIT;

-- Los contadores vuelven a 1: el id del equipo se muestra en el HUD y se usa
-- para reingresar, así que después de vaciar conviene que el próximo sea 1.
-- Van fuera de la transacción porque en MySQL el DDL provoca un commit
-- implícito: dentro de la transacción la cortaría antes de tiempo.
ALTER TABLE incorrecta        AUTO_INCREMENT = 1;
ALTER TABLE respuesta_elegida AUTO_INCREMENT = 1;
ALTER TABLE intento_pregunta  AUTO_INCREMENT = 1;
ALTER TABLE intento_envio     AUTO_INCREMENT = 1;
ALTER TABLE intento_estacion  AUTO_INCREMENT = 1;
ALTER TABLE intento           AUTO_INCREMENT = 1;
ALTER TABLE equipo            AUTO_INCREMENT = 1;

-- ----------------------------------------------------------------------------
-- Verificación rápida (opcional)
-- ----------------------------------------------------------------------------
-- SELECT 'incorrecta', COUNT(*) FROM incorrecta
-- UNION ALL SELECT 'respuesta_elegida', COUNT(*) FROM respuesta_elegida
-- UNION ALL SELECT 'intento_pregunta', COUNT(*) FROM intento_pregunta
-- UNION ALL SELECT 'intento_envio', COUNT(*) FROM intento_envio
-- UNION ALL SELECT 'intento_estacion', COUNT(*) FROM intento_estacion
-- UNION ALL SELECT 'intento', COUNT(*) FROM intento
-- UNION ALL SELECT 'equipo', COUNT(*) FROM equipo;
