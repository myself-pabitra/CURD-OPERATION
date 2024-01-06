import mysql.connector
from dotenv import dotenv_values

# Load environment variables
config_credentials = dict(dotenv_values(".env"))


MYSQL_HOST = config_credentials['MYSQL_HOST']
MYSQL_USER = config_credentials['MYSQL_USER']
MYSQL_PASSWORD = config_credentials['MYSQL_PASSWORD']
MYSQL_DB = config_credentials['MYSQL_DB']


# Connect to MySQL
def connect():
    return mysql.connector.connect(
        user=MYSQL_USER,
        host=MYSQL_HOST,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )



def initialize_db():
    conn = connect()
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255) NOT NULL,
        item_description TEXT NOT NULL
    )
    """
    cursor.execute(query)
    conn.close()


def create_items(item_name, item_description):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO items (item_name, item_description) VALUES (%s, %s)"
    values = (item_name, item_description)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return cursor.lastrowid


def get_item_by_id(item_id):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM items WHERE item_id = %s"
    cursor.execute(query, (item_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_all_items():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM items"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def update_item(item_id,item_name,item_description):
    conn = connect()
    cursor = conn.cursor()
    query = "UPDATE items SET item_name = %s, item_description = %s WHERE item_id = %s"
    values = (item_name, item_description, item_id)
    cursor.execute(query,values)
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated



def delete_item(item_id):
    conn = connect()
    cursor = conn.cursor()
    query = "DELETE FROM items WHERE id = %s"
    cursor.execute(query, (item_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


