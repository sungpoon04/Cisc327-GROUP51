from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock user database
users = {
    "user@example.com": "password123",
    "hassan@gmail.com": "password123",
    "steven@gmail.com": "password123",
    "anwar@gmail.com": "password123"
}

# Route for the login page, served at the root URL "/"
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email] == password:
            return "Welcome to Flight Booker!"
        else:
            flash("Invalid email or password!")
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Route for the forgot-password page
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            flash(f"Instructions to reset your password have been sent to {email}.")
            return redirect(url_for('login'))
        else:
            flash("This email is not registered in our system.")
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
