#!/usr/bin/python3
import seed

def stream_user_ages():
    """
    Generator that yields ages of users one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    row = cursor.fetchone()
    while row:  # only one loop
        yield row['age']
        row = cursor.fetchone()
    
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0
    
    for age in stream_user_ages():  # second loop
        total += age
        count += 1
    
    if count == 0:
        average = 0
    else:
        average = total / count
    
    print(f"Average age of users: {average:.2f}")
