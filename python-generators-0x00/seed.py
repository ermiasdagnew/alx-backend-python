#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # replace with your MySQL username
            password='password' # replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create database ALX_prodev if not exists"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # replace with your MySQL username
            password='password',# replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create table user_data if not exists"""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
    """)
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, file_path):
    """Insert CSV data into user_data table"""
    cursor = connection.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()

# --- Generator function ---
def stream_rows(connection, batch_size=1):
    """Generator to yield rows one by one from user_data table"""
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names
    cursor.execute("SELECT * FROM user_data;")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()
