import unittest
from app import app
from database_op import insert_user, delete_user

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and insert a unique user for each test."""
        self.app = app.test_client()
        self.app.testing = True

        # Insert a unique user with a unique email and phone number
        try:
            insert_user("unique_user@example.com", "0987654321", "password123", "Test", "User", "456 Unique St")
        except Exception as e:
            print("Error setting up test user:", e)

    def tearDown(self):
        """Clean up by deleting the user after each test to avoid conflicts."""
        try:
            delete_user("unique_user@example.com")
        except Exception as e:
            print("Error tearing down test user:", e)

    # Test if the login page loads successfully (GET request)
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LOGIN TO FLIGHT BOOKER', response.data)

    # Test valid login (POST request)
    def test_valid_login(self):
        response = self.app.post('/login', data=dict(email="unique_user@example.com", password="password123"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check for an element unique to the payment page to confirm redirection
        self.assertIn(b'Pay CAD $1244.13', response.data)  # Ensures the payment page is displayed

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
        response = self.app.post('/forgot-password', data=dict(email="unique_user@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Instructions to reset your password have been sent', response.data)

    # Test invalid forgot password request (POST request)
    def test_invalid_forgot_password(self):
        response = self.app.post('/forgot-password', data=dict(email="wrong@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This email is not registered in our system.', response.data)

if __name__ == '__main__':
    unittest.main()
