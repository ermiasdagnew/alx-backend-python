#!/usr/bin/python3
import seed  # your seed.py for DB connection

def stream_users_in_batches(batch_size=50):
    """
    Generator function that fetches users from the database in batches.
    Uses yield, no return.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # yield the batch

    cursor.close()
    connection.close()


def batch_processing(batch_size=50):
    """
    Processes each batch and yields users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # yield individual users, no return
