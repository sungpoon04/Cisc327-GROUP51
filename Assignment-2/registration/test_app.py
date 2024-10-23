import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Set up the testing environment
    def setUp(self):
        self.app = app.test_client()  # Create a test client
        self.app.testing = True       # Set Flask to testing mode

    # Test if the home page loads successfully
    def test_home_page(self):
        result = self.app.get('/')  # Simulate a GET request
        self.assertEqual(result.status_code, 200)  # Check if the status code is 200 for success

    # Test for successful step 1
    def test_successful_step1(self):
        result = self.app.post('/step1', data={
            'email': 'test@example.com',
            'password': 'password123',
            'confirmPassword': 'password123'
        })
        self.assertEqual(result.status_code, 200)  # Check if step 1 was successful
        self.assertIn(b'Step 1 successful', result.data)

    # Test for failed step 1 due to passwords that don't match
    def test_failed_step1_password(self):
        result = self.app.post('/step1', data={
            'email': 'test@example.com',
            'password': 'password_a',
            'confirmPassword': 'password_b'
        })
        self.assertEqual(result.status_code, 400)  # Expecting 400 for failed validation
        self.assertIn(b'Step 1 failed', result.data)

    # Test for failed step 1 due to missing email
    def test_failed_step1_email(self):
        result = self.app.post('/step1', data={
            'password': 'password123',
            'confirmPassword': 'password123'
        })
        self.assertEqual(result.status_code, 400)  # Expecting 400 for failed validation
        self.assertIn(b'Step 1 failed', result.data)

    # Test for successful step 2
    def test_successful_step2(self):
        result = self.app.post('/step2', data={
            'first-name': 'Steven',
            'last-name': 'Guan',
            'home-address': 'Queen\'s University'
        })
        self.assertEqual(result.status_code, 200)  # Check if step 2 was successful
        self.assertIn(b'Step 2 successful', result.data)

    # Test for failed step 2 due to unfilled sections
    def test_failed_step2_missing_1(self):
        result = self.app.post('/step2', data={
            'last-name': 'Guan',
            'home-address': 'Queen\'s University'
        })
        self.assertEqual(result.status_code, 400)  # Expecting 400 for failed validation
        self.assertIn(b'Step 2 failed', result.data)

    # Test for successful step 3
    def test_successful_step3(self):
        result = self.app.post('/step3', data={
            'user-code': '123456',
            'code': '123456',
        })
        self.assertEqual(result.status_code, 200)  # Check if step 3 was successful
        self.assertIn(b'Step 3 successful', result.data)

    # Test for failed step 3 due to verification codes not matching
    def test_failed_step3_matching(self):
        result = self.app.post('/step3', data={
            'user-code': '7654321',
            'code': '123456',
        })
        self.assertEqual(result.status_code, 400)  # Expecting 400 for failed validation
        self.assertIn(b'Step 3 failed', result.data)



if __name__ == '__main__':
    unittest.main()