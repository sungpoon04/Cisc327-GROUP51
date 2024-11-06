import unittest
from app import app
import random

class FlaskTestCase(unittest.TestCase):

    # Set up the testing environment
    def setUp(self):
        self.app = app.test_client()  # Create a test client
        self.app.testing = True       # Set Flask to testing mode

    def generate_random_phone(self):
        return str(random.randint(1000000000, 9999999999))

    def generate_random_email(self):
        return f"test{random.randint(1000, 9999)}@example.com"

    def test_successful_registration(self):
        with self.app as client:
            client.set_cookie('verification_code', '123456')
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
            client.set_cookie('verification_code', '123456')
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
            client.set_cookie('verification_code', '123456')
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
