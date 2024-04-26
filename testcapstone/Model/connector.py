import mysql.connector
from mysql.connector import Error

hostname = "k76.h.filess.io"
database = "Reytop2_stopheldto"
port = "3306"
username = "Reytop2_stopheldto"
password = "b9cd2a044f066ba96021d5b0e31b0ebd92f6c713"

try:
    connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

