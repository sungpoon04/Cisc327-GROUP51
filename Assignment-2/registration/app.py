from flask import Flask, render_template, request
import random

app = Flask(__name__)
app.secret_key = 'secret_key_for_sessions'

# open terminal
# cd .\CISC327_assignment\
# python .\register_back.py

@app.route('/')
def index():
    return render_template('register_front.html')

@app.route('/step1', methods=['POST'])
def step1():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')

    if not email or (password != confirm_password):
        return 'Step 1 failed', 400
    return 'Step 1 successful', 200


@app.route('/step2', methods=['POST'])
def step2():
    first = request.form.get('first-name')
    last = request.form.get('last-name')
    address = request.form.get('home-address')

    if (not first) or (not last) or (not address):
        return 'Step 2 failed', 400
    return 'Step 2 successful', 200


@app.route('/step3', methods=['POST'])
def step3():
    user_code = request.form.get('user-code')
    user_code = int(user_code)
    if not user_code or not (100000 <= user_code <= 999999):
        return 'Step 3 failed', 400
    return 'Step 3 successful', 200   


if __name__ == '__main__':
    app.run(debug=True)