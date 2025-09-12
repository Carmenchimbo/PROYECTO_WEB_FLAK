import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # Cambia si tu usuario es otro
        password="",       # Pon tu contraseña si tienes
        database="libreria_sofi"
    )

#git config user.name "Carmenchimbo"
#git config user.email "ca.chimbos@uea.edu.ec"