import mysql.connector
from mysql.connector import Error

hostname = "462.h.filess.io"
database = "reytop3_perfectly"
port = "3306"
username = "reytop3_perfectly"
password = "73bac833e2e1437cc2e127b57d2a70b7b4f11308"

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
