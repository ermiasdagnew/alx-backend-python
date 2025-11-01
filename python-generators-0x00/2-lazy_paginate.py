#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches users in pages of page_size.
    """
    offset = 0
    while True:  # only one loop required
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop if no more rows
        yield page
        offset += page_size  # move to next page
