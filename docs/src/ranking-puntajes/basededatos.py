import sqlite3
print ("Iniciando....")
try:
    conexion = sqlite3.connect("basededatos_contador.db")
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM "Puntuación"')
    resultado =  cursor.fetchall()
    for fila in resultado:
        print ("Datos: ")
        print (fila)
except sqlite3.Error as error:
    print ("Hubo un error: " + error)
finally:            
    conexion.close()
