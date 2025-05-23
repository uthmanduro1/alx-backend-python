# 0-stream_users.py
import mysql.connector
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'user',  
    'password': 'password',
    'database': 'ALX_prodev'
}

def stream_users():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()


sys.modules[__name__] = stream_users