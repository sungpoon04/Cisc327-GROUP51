import sqlite3

"""
    This python file is used to initialize tables
    for our local database.
"""

def create_user():
    # connect to local mydatabase.db
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # create table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            home_address TEXT NOT NULL
        )
    ''')

    # save changes to mydatabase.db
    conn.commit()
    # close connection
    conn.close()

    print("Table has been successfully created.")

if __name__ == "__main__":
    create_user()