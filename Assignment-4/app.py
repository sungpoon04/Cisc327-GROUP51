from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import random
import sqlite3
from database_op import insert_user, get_user_by_email, user_exists  # Assuming these functions are in database_op.py

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Function to load payment data
def load_payment_data():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT method, card_number, expiration, cvc, name, country, balance FROM payments")
    payment_data = cursor.fetchall()
    conn.close()
    return payment_data

# Load the payment data when the app starts
payment_data = load_payment_data()

# Function to validate card details
def validate_payment(method, card_number, expiration, cvc, name, country):
    for record in payment_data:
        if (record[0] == method and
            record[1] == card_number and
            record[2] == expiration and
            record[3] == cvc and
            record[4] == name and
            record[5] == country):
            return float(record[6])  # Returns balance
    return None

@app.route('/register', methods=['GET','POST'])
def register():
    # Retrieve form data
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    home_address = request.form.get('home-address')
    user_code = request.form.get('user-code')
    terms = request.form.get('termsBox')

    # Check if passwords match criteria
    if password != confirm_password:
        return 'Passwords do not match or are invalid.', 400

    # Check for missing essential components
    if (not first_name) or (not last_name) or (not home_address) or (not email):
        return 'Missing essential information', 400
    
    # Check if terms and conditions were accepted
    if not terms:
        return 'Terms and Conditions not accepted', 400

    # Check if verification code is correct (assuming the frontend generated code is passed correctly)
    # Retrieve code from cookies
    generated_code = request.cookies.get('verification_code') 
    if user_code != generated_code:
        return 'Incorrect verification code.', 400

    # Insert user into the database
    insert_user(email, phone, password, first_name, last_name, home_address)

    # Redirect to the login page after successful registration
    return redirect(url_for('login'))  # Redirect to the login route


# Root route to redirect to the registration page
@app.route('/')
def home():
    return render_template('register_front.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve the user from the database
        user = get_user_by_email(email)

        # Check if user exists and passwords match
        if user and user[1] == password:  # user[1] contains the password
            flash("Welcome to Flight Booker!", "login_success")
            session['logged_in'] = True
            return redirect(url_for('payment_form'))
        else:
            flash("Invalid email or password!", "login_error")
            return redirect(url_for('login'))

    return render_template('login.html')

# Forgot Password Route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = get_user_by_email(email)
        if user:
            flash(f"Instructions to reset your password have been sent to {email}.", "login_info")
            return redirect(url_for('login'))
        else:
            flash("This email is not registered in our system.", "login_error")
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')
'''
# Flight Selection Route
@app.route('/selection', methods=['GET', 'POST'])
def selection():
    flights = [
        {"departure": "07:23", "arrival": "06:35", "stops": "1 Stop, 18h 12m", "economy_price": "CAD 1,251", "business_price": "CAD 10,268"},
        {"departure": "15:09", "arrival": "16:45", "stops": "1 Stop, 18h 36m", "economy_price": "CAD 1,193", "business_price": "CAD 13,267"},
        {"departure": "13:25", "arrival": "16:45", "stops": "1 Stop, 20h 21m", "economy_price": "CAD 1,236", "business_price": "CAD 13,267"},
        {"departure": "13:29", "arrival": "06:41", "stops": "1 Stop, 17h 12m", "economy_price": "CAD 1,198", "business_price": "CAD 10,258"}
    ]

    if request.method == 'POST':
        selected_flight = request.form.get('flight')
        session['selected_flight'] = flights[int(selected_flight)]
        return redirect(url_for('confirmed'))

    return render_template('selection.html', flights=flights)
'''
# Payment Form Route
@app.route('/payment', methods=['GET'])
def payment_form():
    return render_template('payments.html')

# Payment Processing Route
@app.route('/process_payment', methods=['POST'])
def process_payment():
    email = request.form.get('email')
    method = request.form.get('method')
    card_number = request.form.get('card_number').replace(" ", "")
    expiration = request.form.get('expiration')
    cvc = request.form.get('cvc')
    name_on_card = request.form.get('name_on_card').replace(" ", "").lower()
    country = request.form.get('country')
    amount_due = 1244.13

    balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
    if balance is not None and balance >= amount_due:
        flash(f"Payment of CAD ${amount_due} successful! Remaining balance: CAD ${balance - amount_due}.", 'success')
        return redirect(url_for('payment_form'))
    elif balance is not None:
        flash(f"Insufficient funds! Available balance: CAD ${balance}.", 'error')
    else:
        flash("Invalid payment details! Please try again.", 'error')
    return redirect(url_for('payment_form'))
    
@app.route('/cancel_payment', methods=['GET'])
def cancel_payment():
    # Redirect to the login page
    return redirect(url_for('login'))
    
'''
# Confirmation Route
@app.route('/confirmed', methods=['GET'])
def confirmed():
    selected_flight = session.get('selected_flight')
    return render_template('confirmed.html', flight=selected_flight)
'''
if __name__ == '__main__':
    app.run(debug=True)
