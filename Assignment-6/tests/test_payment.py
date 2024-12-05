import unittest
from app import app, validate_payment, load_payment_data  # Import functions from app.py

class TestPaymentValidation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Load payment data from the database
        cls.payment_data = load_payment_data()
        app.config['TESTING'] = True  # Enable testing mode
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    def test_process_payment_success(self):
        with app.test_client() as client:
            response = client.post('/process_payment', data={
                'email': 'test@example.com',
                'method': 'debit',
                'card_number': '1111111111111111',
                'expiration': '0125',
                'cvc': '001',
                'name_on_card': 'johnsmith',
                'country': 'CA'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Payment of CAD $1244.13 successful!', response.data)

    def test_process_payment_insufficient_funds(self):
        with app.test_client() as client:
            response = client.post('/process_payment', data={
                'email': 'test@example.com',
                'method': 'debit',
                'card_number': '5555555555555555',
                'expiration': '0529',
                'cvc': '005',
                'name_on_card': 'johnsmith',
                'country': 'CA'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Insufficient funds!', response.data)

    def test_process_payment_invalid_details(self):
        with app.test_client() as client:
            response = client.post('/process_payment', data={
                'email': 'test@example.com',
                'method': 'debit',
                'card_number': '9999999999999999',  # Invalid card number
                'expiration': '0125',
                'cvc': '001',
                'name_on_card': 'johnsmith',
                'country': 'CA'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid payment details!', response.data)
    
    def test_cancel_payment_redirect(self):
        with app.test_client() as client:
            response = client.get('/cancel_payment')
            self.assertEqual(response.status_code, 302)  # HTTP status for redirect
            self.assertIn('/login', response.location)  # Check redirection to /login

    # Tests for valid cards in the database with sufficient funds
    def test_debit(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)

    def test_credit(self):
        method = "credit"
        card_number = "2222222222222222"
        expiration = "0226"
        cvc = "002"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)
        
    def test_visa(self):
        method = "visa"
        card_number = "3333333333333333"
        expiration = "0327"
        cvc = "003"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)
        
    def test_master(self):
        method = "master"
        card_number = "4444444444444444"
        expiration = "0428"
        cvc = "004"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)

    # Test for valid card with insufficient funds
    def test_insufficient_fund(self):
        method = "debit"
        card_number = "5555555555555555"
        expiration = "0529"
        cvc = "005"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertLess(balance, 1244.13)

    # Test with an incorrect payment method
    def test_incorrect_method(self):
        method = "credit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Test with an incorrect card number
    def test_incorrect_number(self):
        method = "debit"
        card_number = "1111111122222222"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Test with an incorrect expiration date
    def test_incorrect_expiration(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "1299"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Test with an incorrect CVC
    def test_incorrect_cvc(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "999"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Test with an incorrect name
    def test_incorrect_name(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "smithjohn"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Test with an incorrect country
    def test_incorrect_country(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)


if __name__ == '__main__':
    unittest.main() # pragma: no cover
