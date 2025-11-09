import pymysql

# Function to create a connection to the MySQL database
def create_connection():
    return pymysql.connect(
        host="host.docker.internal", # Your MySQL server host
        user="root",              # Your MySQL username
        password="rootroot",    # Your MySQL password
        database="userinfo"     # Your MySQL database name
    )

# Function to create a table to store names if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS names (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
    )
    """)
    connection.commit()
    cursor.close()

# Function to insert a name into the database
def insert_name(connection, name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO names (name) VALUES (%s)", (name,))
    connection.commit()
    cursor.close()

# Function to fetch all names from the database
def fetch_all_names(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM names")
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return names

import pymysql

# ... your functions here ...

if __name__ == "__main__":
    connection = create_connection()
    create_table(connection)
    
    # Insert example names
    insert_name(connection, "Khushi")
    insert_name(connection, "Alice")
    
    # Fetch and display all names
    all_names = fetch_all_names(connection)
    print("Names in database:", all_names)
    
    connection.close()
