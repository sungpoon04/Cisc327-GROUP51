from flask import request
import sqlite3
import init_tables

"""
    This python file is responsible for running ongoing retrieving
    and updating of user information.
"""

# checks to see if the users table exists - if not create it
def check_exist():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # using sqlite_master to check if users table exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    exist = cursor.fetchone()

    if not exist:
        init_tables.create_user()  # call func from init_tables to create tables

# function to retrieve user's email and password using their email
def get_user_by_email(email):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# function to chekc if the user is attempting to use duplicate information
def user_exists(email, phone):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? OR phone = ?", (email, phone))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

# inserting user information into the users table
def insert_user(email, phone, password, first_name, last_name, home_address):
    # see if 'users' table exist
    check_exist()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (email, phone, password, first_name, last_name, home_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email, phone, password, first_name, last_name, home_address))
    
    conn.commit()
    conn.close()
    print("User added successfully.")
    

# Function to retrieve all users (for testing or verification)
def get_all_users():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    conn.close()
    return users

def register_user():
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    home_address = request.form.get('home-address')

    insert_user(email,phone,password,first_name,last_name,home_address)


if __name__ == "__main__":
    # Example usage
    # insert_user('Alice', 'alice@example.com', '123-456-7890', 'password123')
    # print("All users:", get_all_users())
    pass