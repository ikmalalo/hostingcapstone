import mysql.connector
from mysql.connector import Error

hostname = "izh.h.filess.io"
database = "ReyTop_unlessblow"
port = "3306"
username = "ReyTop_unlessblow"
password = "234f1036bad6ab5930d6d3a10a4868b88ebe3e18"

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

