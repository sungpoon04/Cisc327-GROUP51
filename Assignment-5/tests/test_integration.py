import unittest
from app import app
import uuid
from database_op import insert_user, delete_user

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.test_email = f"unique_{uuid.uuid4()}@example.com"
        cls.test_phone = f"123456{uuid.uuid4().int % 10000}"  # Ensure unique phone number
        cls.test_password = "password123"
        cls.test_payment_method = {
            'email': cls.test_email,
            'method': 'debit',
            'card_number': '1111111111111111',
            'expiration': '0125',
            'cvc': '001',
            'name_on_card': 'johnsmith',
            'country': 'CA'
        }
        # Add a valid user to the database for testing
        insert_user(cls.test_email, cls.test_phone, cls.test_password, "Test", "User", "123 Test St")

    @classmethod
    def tearDownClass(cls):
        # Remove the test user after all tests are done
        delete_user(cls.test_email)

    def test_wrong_login_correct_login_and_payment(self):
        # Step 1: Attempt login with wrong credentials
        wrong_login = {'email': 'wrong_user@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/login', data=wrong_login, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password!', response.data)

        # Step 2: Log in with correct credentials
        correct_login = {'email': self.test_email, 'password': self.test_password}
        response = self.client.post('/login', data=correct_login, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flight Booker!', response.data)

        # Step 3: Make a payment
        response = self.client.post('/process_payment', data=self.test_payment_method, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Payment of CAD $1244.13 successful!', response.data)

if __name__ == '__main__':
    unittest.main()
