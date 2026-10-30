<?php
$servidor = "localhost";
$usuario = "root";
$password = "";
$base_datos = "contador_escaperoom"; // <-- ¡Tiene que llamarse igual que en phpMyAdmin!

$conexion = new mysqli($servidor, $usuario, $password, $base_datos);

if ($conexion->connect_error) {
    die("Error de conexión: " . $conexion->connect_error);
}

// Incrementamos el contador
$conexion->query("UPDATE contador_escaperoom SET total = total + 1 WHERE id = 1");

// Consultamos el valor actualizado
$resultado = $conexion->query("SELECT total FROM contador_escaperoom WHERE id = 1");

if ($resultado && $resultado->num_rows > 0) {
    $fila = $resultado->fetch_assoc();
    echo $fila['total'];
} else {
    echo "0";
}

$conexion->close();
?>