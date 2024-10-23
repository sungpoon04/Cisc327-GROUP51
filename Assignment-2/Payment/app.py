from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for flashing messages

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

# Mock database to validate the user payment
# It is a 2D list with method, card_number, expiration date, name, country and balance stored in each item
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
            
            # Confirm the provided information is correct before returning the balance on the account
            return float(record[6])
    return None

# Route to render the payment form
@app.route('/')
def payment_form():
    return render_template('payments.html')

# Route to process the payment form
@app.route('/process_payment', methods=['POST'])
def process_payment():
    email = request.form['email']
    method = request.form['method']
    card_number = request.form['card_number'].replace(" ", "")
    expiration = request.form['expiration']
    cvc = request.form['cvc']
    name_on_card = request.form['name_on_card'].replace(" ", "").lower()
    country = request.form['country']

    # Validate payment details against the mock database
    balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)

    if balance is not None:
        amount_due = 1244.13  # The amount due
        if balance >= amount_due:
            # Successful payment scenario
            flash(f"Payment of CAD ${amount_due} successful! Redirecting to confirmation page.", 'success')
            return redirect(url_for('payment_form'))
        else:
            # Insufficient funds
            flash(f"Insufficient funds! Available balance: CAD ${balance}.", 'error')
            return redirect(url_for('payment_form'))
    else:
        # Invalid payment details
        flash("Invalid payment details! Please try again.", 'error')
        return redirect(url_for('payment_form'))

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
