from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock user database
users = {
    "user@example.com": "password123",
    "hassan@gmail.com": "password123",
    "steven@gmail.com": "password123",
    "sungmoon@gmail.com": "password123",
    "anwar@gmail.com": "password123"
}

# Mock payment database from file
def read_database(file_name):
    data_list = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                line_items = line.strip().split()
                data_list.append(line_items)
    except FileNotFoundError:
        print("The file was not found.")
    
    return data_list

payment_data = read_database("database.txt")

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
    
# Registration Steps
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        step = request.form.get('step')

        if step == '1':
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')
            
            if not email or (password != confirm_password):
                flash("Passwords do not match or email is missing.", "error")
                return redirect(url_for('register'))
            
            # Store in session for multi-step process
            session['email'] = email
            session['password'] = password
            return render_template('register_front.html', step=2)
        
        elif step == '2':
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            address = request.form.get('home-address')
            
            if not first_name or not last_name or not address:
                flash("Please complete all fields in Step 2.", "error")
                return redirect(url_for('register'))
            
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['address'] = address
            session['verification_code'] = str(random.randint(100000, 999999))
            flash("Verification code sent.", "info")
            return render_template('register_front.html', step=3)
        
        elif step == '3':
            user_code = request.form.get('user-code')
            if user_code == session.get('verification_code'):
                flash("Registration successful!", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid verification code.", "error")
                return render_template('register_front.html', step=3)

    return render_template('register_front.html', step=1)
    
# Root route to redirect to the registration page
@app.route('/')
def home():
    return redirect(url_for('register'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and users[email] == password:
            flash("Welcome to Flight Booker!", "success")
            session['logged_in'] = True
            return redirect(url_for('payment_form'))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Forgot Password Route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in users:
            flash(f"Instructions to reset your password have been sent to {email}.", "info")
            return redirect(url_for('login'))
        else:
            flash("This email is not registered in our system.", "error")
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')
    
# Selection Route
@app.route('/selection', methods=['GET', 'POST'])
def selection():
    #if not session.get('logged_in'):
     #   flash("Please log in first to select a flight," "error")
     #   return redirect(url_for('login'))
    
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

    # Validate payment details
    balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)

    if balance is not None:
        if balance >= amount_due:
            flash(f"Payment of CAD ${amount_due} successful! Remaining balance: CAD ${balance - amount_due}.", 'success')
            return redirect(url_for('payment_form'))
        else:
            flash(f"Insufficient funds! Available balance: CAD ${balance}.", 'error')
            return redirect(url_for('payment_form'))
    else:
        flash("Invalid payment details! Please try again.", 'error')
        return redirect(url_for('payment_form'))

# Confirmation Route
@app.route('/confirmed', methods=['GET'])
def confirmed():
    selected_flight = session.get('selected_flight')
    #if not selected_flight:
    #    flash("No flight selected. Please select a flight.", "error")
    #    return redirect(url_for('selection'))

    return render_template('confirmed.html', flight=selected_flight)

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
