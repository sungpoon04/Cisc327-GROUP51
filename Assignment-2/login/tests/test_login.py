import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Set up the testing environment
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test if the login page loads successfully (GET request)
    def test_login_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the page loads
        self.assertIn(b'LOGIN TO FLIGHT BOOKER', response.data)  # Check if the correct content is there

    # Test valid login (POST request)
    def test_valid_login(self):
        response = self.app.post('/', data=dict(email="user@example.com", password="password123"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ensure response status code is 200
        self.assertIn(b'Welcome to Flight Booker!', response.data)  # Check for success message

    # Test invalid login (POST request)
    def test_invalid_login(self):
        response = self.app.post('/', data=dict(email="wrong@example.com", password="wrongpassword"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check if it redirects back to login
        self.assertIn(b'Invalid email or password!', response.data)  # Check for the flashed error message

    # Test if the forgot password page loads successfully (GET request)
    def test_forgot_password_page_loads(self):
        response = self.app.get('/forgot-password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Forgot Your Password?', response.data)

    # Test valid forgot password request (POST request)
    def test_valid_forgot_password(self):
        response = self.app.post('/forgot-password', data=dict(email="user@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Should redirect back to login
        self.assertIn(b'Instructions to reset your password have been sent', response.data)  # Check for success message

    # Test invalid forgot password request (POST request)
    def test_invalid_forgot_password(self):
        response = self.app.post('/forgot-password', data=dict(email="wrong@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Should redirect back to forgot password page
        self.assertIn(b'This email is not registered in our system.', response.data)  # Check for error message

if __name__ == '__main__':
    unittest.main()
