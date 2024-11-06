import sqlite3

def check_exist():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # using sqlite_master to check if users table exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    exist = cursor.fetchone()

    if not exist:
        create_payments()

def create_payments():
    # connect to local mydatabase.db
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    
    # Create the payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        method TEXT CHECK(method IN ('debit', 'credit', 'visa', 'master')),
        card_number TEXT UNIQUE NOT NULL CHECK(LENGTH(card_number) = 16),
        expiration TEXT NOT NULL CHECK(LENGTH(expiration) = 4),
        cvc TEXT NOT NULL CHECK(LENGTH(cvc) = 3),
        name TEXT NOT NULL,
        country TEXT CHECK(country IN ('CA', 'US')),
        balance REAL CHECK(balance >= 0)
    )
    ''')
    
    sample_payments = [
    ('debit', '1111111111111111', '0125', '001', 'johnsmith', 'CA', '1300'),
    ('credit', '2222222222222222', '0226', '002', 'johnsmith', 'CA', '1500'),
    ('visa', '3333333333333333', '0327', '003', 'johnsmith', 'US', '2000'),
    ('master', '4444444444444444', '0428', '004', 'johnsmith', 'US', '3000'),
    ('debit', '5555555555555555', '0529', '005', 'johnsmith', 'CA', '900')
    ]
    
    for row in sample_payments:
        cursor.execute('''
            INSERT INTO payments (method, card_number, expiration, cvc, name, country, balance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Database and table created successfully.")


check_exist()