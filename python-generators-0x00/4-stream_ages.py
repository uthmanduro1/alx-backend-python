import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'druth',
    'password': 'uthmanbadolee',
    'database': 'ALX_prodev'
}

def stream_user_ages():
    """Generator that yields ages one by one from the user_data table."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:  
        yield float(age)

    cursor.close()
    connection.close()

def compute_average_age():
    """Compute the average age of users using the generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    compute_average_age()
