import mysql.connector
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'druth',  
    'password': 'uthmanbadolee',
    'database': 'ALX_prodev'
}

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor: 
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:  
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size): 
        # process and filter users over 25
        for user in batch:
            if float(user['age']) > 25:
                print(user)
                return user
