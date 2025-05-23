import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'druth',
    'password': 'uthmanbadolee',
    'database': 'ALX_prodev'
}

def paginate_users(page_size, offset):
    """Fetch a page of users starting from a given offset."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def lazy_pagination(page_size):
    """Generator to lazily fetch pages of users."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

