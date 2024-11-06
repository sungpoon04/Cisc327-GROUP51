import unittest
from app import app
import random

class FlaskTestCase(unittest.TestCase):

    # Set up the testing environment
    def setUp(self):
        self.app = app.test_client()  # Create a test client
        self.app.testing = True       # Set Flask to testing mode

    def generate_random_phone(self):
        # Generate a random 10-digit phone number
        # Adds uniqueness so that database doesn't fail
        return str(random.randint(1000000000, 9999999999))

    def generate_random_email(self):
        # Generate a random email address
        # Adds uniqueness so that database doesn't fail
        return f"test{random.randint(1000, 9999)}@example.com"

    def test_home_page(self):
        result = self.app.get('/')  # Simulate a GET request
        self.assertEqual(result.status_code, 200)  # Check if the status code is 200 for success

    def test_successful_registration(self):
        # Set a mock verification code in cookies
        with self.app as client:
            client.set_cookie('localhost', 'verification_code', '123456')
            result = client.post('/register', data={
                'email': self.generate_random_email(),
                'phone': self.generate_random_phone(),
                'password': 'password123',
                'confirmPassword': 'password123',
                'first-name': 'John',
                'last-name': 'Doe',
                'home-address': '123 Queen Street',
                'user-code': '123456',
                'termsBox': 'on'
            })
            # Check if registration was successful (redirect which is code 302)
            self.assertEqual(result.status_code, 302) 

    def test_failed_registration_password(self):
        result = self.app.post('/register', data={
            'email': self.generate_random_email(),
            'phone': self.generate_random_phone(),
            'password': 'password123',
            'confirmPassword': 'password321',
            'first-name': 'John',
            'last-name': 'Doe',
            'home-address': '123 Queen Street',
            'user-code': '123456',
            'termsBox': 'on'
        })
        self.assertIn(b'Passwords do not match or are invalid.', result.data)

    def test_failed_registration_missing_email(self):
        result = self.app.post('/register', data={
            'phone': self.generate_random_phone(),
            'password': 'password123',
            'confirmPassword': 'password123',
            'first-name': 'John',
            'last-name': 'Doe',
            'home-address': '123 Queen Street',
            'user-code': '123456',
            'termsBox': 'on'
        })
        self.assertIn(b'Missing essential information', result.data)

    def test_failed_registration_missing_user_code(self):
        with self.app as client:
            client.set_cookie('localhost', 'verification_code', '123456')
            result = client.post('/register', data={
                'email': self.generate_random_email(),
                'phone': self.generate_random_phone(),
                'password': 'password123',
                'confirmPassword': 'password123',
                'first-name': 'John',
                'last-name': 'Doe',
                'home-address': '123 Queen Street',
                'termsBox': 'on'
            })
            self.assertIn(b'Incorrect verification code.', result.data)

    def test_failed_registration_terms_unchecked(self):
        with self.app as client:
            client.set_cookie('localhost', 'verification_code', '123456')
            result = client.post('/register', data={
                'email': self.generate_random_email(),
                'phone': self.generate_random_phone(),
                'password': 'password123',
                'confirmPassword': 'password123',
                'first-name': 'John',
                'last-name': 'Doe',
                'home-address': '123 Queen Street',
                'user-code': '123456'
            })
            self.assertIn(b'Terms and Conditions not accepted', result.data)

if __name__ == '__main__':
    unittest.main()
