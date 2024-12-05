import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the WebDriver once for all tests.
        """
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        """
        Quit the WebDriver after all tests.
        """
        cls.driver.quit()

    def setUp(self):
        """
        Runs before each test method.
        """
        self.driver.get(f"{self.base_url}/login")
        # Wait for the login form to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )


    def test_valid_login(self):
        """
        Test logging in with valid credentials.
        """
        email = "testlogin@gmail.com"
        password = "password123"

        # Fill out the login form
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the flash message
        flash_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash-message"))
        )

        # Assert the welcome message is displayed
        self.assertIn("Welcome to Flight Booker!", flash_message.text)
        print("Valid login test passed!")

    def test_invalid_email(self):
        """
        Test logging in with an invalid email.
        """
        invalid_email = "invalidemail@notregistered.com"
        password = "hassan786"

        # Fill out the login form
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(invalid_email)

        password_field = self.driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the flash message
        flash_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash-message"))
        )

        # Assert the error message is displayed
        self.assertIn("Invalid email or password!", flash_message.text)
        print("Invalid email test passed!")

    def test_invalid_password(self):
        """
        Test logging in with an invalid password.
        """
        email = "123456789@gmail.com"
        invalid_password = "wrongpassword"

        # Fill out the login form
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(invalid_password)

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the flash message
        flash_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash-message"))
        )

        # Assert the error message is displayed
        self.assertIn("Invalid email or password!", flash_message.text)
        print("Invalid password test passed!")

    def test_forgot_password_load(self):
        """
        Test if the 'Forgot your password?' link navigates to the Forgot Password page.
        """
        # Find and click the 'Forgot your password?' link
        forgot_password_link = self.driver.find_element(By.LINK_TEXT, "Forgot your password?")
        forgot_password_link.click()

        # Wait for the Forgot Password form to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Assert that the current URL is the forgot-password page
        current_url = self.driver.current_url
        expected_url = f"{self.base_url}/forgot-password"
        self.assertEqual(current_url, expected_url)
        print("Forgot password page load test passed!")

if __name__ == "__main__":
    unittest.main()
