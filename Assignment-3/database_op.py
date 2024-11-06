from flask import request
import sqlite3
import init_tables

"""
    This python file is responsible for running ongoing retrieving
    and updating of user information.
"""

DATABASE = 'mydatabase.db'  # database path

# Checks to see if the users table exists - if not, creates it
def check_exist():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Using sqlite_master to check if the users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    exist = cursor.fetchone()

    if not exist:
        init_tables.create_user()  # Call function from init_tables to create tables
    conn.close()

# Function to retrieve a user's email and password using their email
def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT email, password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to check if the user is attempting to use duplicate information
def user_exists(email, phone):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? OR phone = ?", (email, phone))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Function to insert user information into the users table
def insert_user(email, phone, password, first_name, last_name, home_address):
    # Check if 'users' table exists
    check_exist()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (email, phone, password, first_name, last_name, home_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email, phone, password, first_name, last_name, home_address))
    conn.commit()
    conn.close()
    print("User added successfully.")

# Function to delete a user by email (for cleanup in tests)
def delete_user(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    print(f"User with email {email} deleted successfully.")

# Function to retrieve all users (for testing or verification)
def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Function to register a user from a Flask form request
def register_user():
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    home_address = request.form.get('home-address')
    insert_user(email, phone, password, first_name, last_name, home_address)

if __name__ == "__main__":
    # Example usage
    # insert_user('alice@example.com', '1234567890', 'password123', 'Alice', 'Smith', '123 Main St')
    # print("All users:", get_all_users())
    pass
