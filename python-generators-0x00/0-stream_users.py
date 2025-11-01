#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function that yields rows from the user_data table one by one.
    """
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # add your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)  # dictionary=True returns each row as a dict

    # Execute the query
    cursor.execute("SELECT * FROM user_data")

    # Yield rows one by one
    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    connection.close()
