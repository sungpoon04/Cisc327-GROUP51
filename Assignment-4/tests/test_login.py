import unittest
from app import app
from database_op import insert_user, delete_user
import uuid

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client with unique user data for isolation."""
        self.app = app.test_client()
        self.app.testing = True
        # Ensure user data is unique to avoid database locking issues
        self.test_email = f"unique_{uuid.uuid4()}@example.com"
        self.test_phone = f"123456{uuid.uuid4().int % 10000}"  # Ensure unique phone number
        insert_user(self.test_email, self.test_phone, "password123", "Test", "User", "456 Unique St")

    def tearDown(self):
        """Delete the test user after each test to maintain database integrity."""
        delete_user(self.test_email)

    # Test if the login page loads successfully (GET request)
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LOGIN TO FLIGHT BOOKER', response.data)

    # Test valid login (POST request)
    def test_valid_login(self):
        response = self.app.post('/login', data=dict(email=self.test_email, password="password123"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flight Booker!', response.data)

    # Test invalid login (POST request)
    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(email="wrong@example.com", password="wrongpassword"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password!', response.data)

    # Test if the forgot password page loads successfully (GET request)
    def test_forgot_password_page_loads(self):
        response = self.app.get('/forgot-password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Forgot Your Password?', response.data)

    # Test valid forgot password request (POST request)
    def test_valid_forgot_password(self):
        response = self.app.post('/forgot-password', data=dict(email=self.test_email), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Instructions to reset your password have been sent', response.data)

    # Test invalid forgot password request (POST request)
    def test_invalid_forgot_password(self):
        response = self.app.post('/forgot-password', data=dict(email="wrong@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This email is not registered in our system.', response.data)

    # Test the root route to ensure it loads the registration page successfully
    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Creating your account', response.data)

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
