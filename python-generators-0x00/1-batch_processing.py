#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    """
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # add your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM user_data")
    
    while True:
        batch = cursor.fetchmany(batch_size)  # fetch batch_size rows at a time
        if not batch:
            break
        yield batch  # yield the whole batch
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users and prints only users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user['age'] > 25:  # filter users over age 25
                print(user)  # this prints the user
