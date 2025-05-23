import mysql.connector
import csv
import uuid
from decimal import Decimal

DB_CONFIG = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',  # Update this
}

# CSV_FILE = 'user_data.csv'


def connect_db():
    """Connect to the MySQL server."""
    return mysql.connector.connect(**DB_CONFIG)


def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    db_config = DB_CONFIG.copy()
    db_config['database'] = 'ALX_prodev'
    return mysql.connector.connect(**db_config)


def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    cursor.close()


def insert_data(connection, data):
    """Insert user data into the table if the user_id does not already exist."""
    cursor = connection.cursor()

    read_data = list(read_csv(data))

    for row in read_data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        try:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, Decimal(age)))
        except mysql.connector.Error as err:
            print(f"Error inserting {name}: {err}")
    connection.commit()
    cursor.close()


def read_csv(file_path):
    """Read CSV and yield rows (excluding headers)."""
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            yield row


def main():
    conn = connect_db()
    create_database(conn)
    conn.close()

    conn_prodev = connect_to_prodev()
    create_table(conn_prodev)
    insert_data(conn_prodev, 'user_data.csv')
    conn_prodev.close()


if __name__ == "__main__":
    main()
