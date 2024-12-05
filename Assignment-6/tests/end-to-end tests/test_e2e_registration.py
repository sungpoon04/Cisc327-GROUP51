# Filename: test_registration.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def generate_unique_email():
    """Generates a unique email address using the current timestamp."""
    timestamp = int(time.time())
    return f"testuser_{timestamp}@example.com"

def extract_verification_code(alert_text):
    """Extracts the 6-digit verification code from the alert text."""
    match = re.search(r"\d{6}", alert_text)
    if match:
        return match.group(0)
    return None


def test_successful_registration(driver, wait):
    print("\nRunning Test Case: Successful Registration")
    driver.get("http://localhost:5000/")
    
    # Fill out the registration form with valid data
    unique_email = generate_unique_email()
    driver.find_element(By.ID, "email").send_keys(unique_email)
    driver.find_element(By.ID, "phone").send_keys("1234567890")
    driver.find_element(By.ID, "password").send_keys("SecurePass123")
    driver.find_element(By.ID, "confirmPassword").send_keys("SecurePass123")
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "home-address").send_keys("123 Main St")
    
    # Click on "Generate Code" to receive the verification code
    generate_code = driver.find_element(By.XPATH, "//span[text()='Generate Code']")
    generate_code.click()
    print("Clicked on 'Generate Code'.")
    
    # Handle the alert to capture the verification code
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert received with text: {alert_text}")
    verification_code = extract_verification_code(alert_text)
    alert.accept()
    print(f"Captured Verification Code: {verification_code}")
    
    # Enter the verification code
    driver.find_element(By.ID, "user-code").send_keys(verification_code)
    
    # Accept the Terms and Conditions
    terms_checkbox = driver.find_element(By.NAME, "termsBox")
    terms_checkbox.click()
    print("Checked the Terms and Conditions box.")
    
    # Submit the registration form
    register_button = driver.find_element(By.ID, "registerButton")
    register_button.click()
    print("Clicked on the Register button.")
    
    # Wait for the response and verify success message
    time.sleep(2)  # Adjust sleep time as needed
    # Wait for the redirect to the login page
    expected_login_url = "http://localhost:5000/login/"
    try:
        wait.until(EC.url_to_be(expected_login_url))
        current_url = driver.current_url
        print(f"Current URL after registration: {current_url}")
        
        if current_url == expected_login_url:
            print("Test Passed: Registration was successful and redirected to the login page.")
        else:
            print("Test Failed: Did not redirect to the login page as expected.")
    except:
        print("Test Failed: Redirect to the login page did not occur within the expected time.")

def test_duplicate_email_registration(driver, wait):
    print("\nRunning Test Case: Duplicate Email Registration")
    driver.get("http://localhost:5000/")
    
    # Use a fixed email to test duplicate registration
    duplicate_email = "duplicate@example.com"
    
    # Pre-register the email manually or ensure it's already in the database
    # For simplicity, we'll attempt to register twice in the script
    
    # First Registration
    driver.find_element(By.ID, "email").send_keys(duplicate_email)
    driver.find_element(By.ID, "phone").send_keys("0987654321")
    driver.find_element(By.ID, "password").send_keys("AnotherPass123")
    driver.find_element(By.ID, "confirmPassword").send_keys("AnotherPass123")
    driver.find_element(By.ID, "first-name").send_keys("Jane")
    driver.find_element(By.ID, "last-name").send_keys("Smith")
    driver.find_element(By.ID, "home-address").send_keys("456 Elm St")
    
    # Generate and enter verification code
    generate_code = driver.find_element(By.XPATH, "//span[text()='Generate Code']")
    generate_code.click()
    print("Clicked on 'Generate Code'.")
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert received with text: {alert_text}")
    verification_code = extract_verification_code(alert_text)
    alert.accept()
    print(f"Captured Verification Code: {verification_code}")
    driver.find_element(By.ID, "user-code").send_keys(verification_code)
    
    # Accept the Terms and Conditions
    terms_checkbox = driver.find_element(By.NAME, "termsBox")
    terms_checkbox.click()
    print("Checked the Terms and Conditions box.")
    
    # Submit the registration form
    register_button = driver.find_element(By.ID, "registerButton")
    register_button.click()
    print("Clicked on the Register button.")
    
    time.sleep(2)
    
    # Attempt Duplicate Registration
    driver.get("http://localhost:5000/")
    print("Attempting to register with duplicate email.")
    
    driver.find_element(By.ID, "email").send_keys(duplicate_email)
    driver.find_element(By.ID, "phone").send_keys("1122334455")
    driver.find_element(By.ID, "password").send_keys("DuplicatePass123")
    driver.find_element(By.ID, "confirmPassword").send_keys("DuplicatePass123")
    driver.find_element(By.ID, "first-name").send_keys("Alice")
    driver.find_element(By.ID, "last-name").send_keys("Johnson")
    driver.find_element(By.ID, "home-address").send_keys("789 Oak St")
    
    # Generate and enter verification code
    generate_code = driver.find_element(By.XPATH, "//span[text()='Generate Code']")
    generate_code.click()
    print("Clicked on 'Generate Code' for duplicate registration.")
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert received with text: {alert_text}")
    verification_code = extract_verification_code(alert_text)
    alert.accept()
    print(f"Captured Verification Code: {verification_code}")
    driver.find_element(By.ID, "user-code").send_keys(verification_code)
    
    # Accept the Terms and Conditions
    terms_checkbox = driver.find_element(By.NAME, "termsBox")
    terms_checkbox.click()
    print("Checked the Terms and Conditions box for duplicate registration.")
    
    # Submit the registration form
    register_button = driver.find_element(By.ID, "registerButton")
    register_button.click()
    print("Clicked on the Register button for duplicate registration.")
    
    time.sleep(2)
    
    # Verify duplicate email error message
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Missing essential information" not in body_text and "Registration successful!" not in body_text:
        print("Test Passed: Duplicate email registration was correctly handled.")
    else:
        print("Test Failed: Duplicate email registration was not handled as expected.")

def test_password_mismatch(driver, wait):
    print("\nRunning Test Case: Password Mismatch")
    driver.get("http://localhost:5000/")
    
    # Fill out the registration form with mismatched passwords
    unique_email = generate_unique_email()
    driver.find_element(By.ID, "email").send_keys(unique_email)
    driver.find_element(By.ID, "phone").send_keys("2233445566")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "confirmPassword").send_keys("Password321")  # Mismatch
    driver.find_element(By.ID, "first-name").send_keys("Bob")
    driver.find_element(By.ID, "last-name").send_keys("Brown")
    driver.find_element(By.ID, "home-address").send_keys("321 Pine St")
    
    # Generate and enter verification code
    generate_code = driver.find_element(By.XPATH, "//span[text()='Generate Code']")
    generate_code.click()
    print("Clicked on 'Generate Code' for password mismatch.")
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert received with text: {alert_text}")
    verification_code = extract_verification_code(alert_text)
    alert.accept()
    print(f"Captured Verification Code: {verification_code}")
    driver.find_element(By.ID, "user-code").send_keys(verification_code)
    
    # Accept the Terms and Conditions
    terms_checkbox = driver.find_element(By.NAME, "termsBox")
    terms_checkbox.click()
    print("Checked the Terms and Conditions box for password mismatch.")
    
    # Submit the registration form
    register_button = driver.find_element(By.ID, "registerButton")
    register_button.click()
    print("Clicked on the Register button for password mismatch.")
    
    time.sleep(2)
    
    # Verify password mismatch error message
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Passwords do not match" in body_text:
        print("Test Passed: Password mismatch was correctly handled.")
    else:
        print("Test Failed: Password mismatch was not handled as expected.")

def test_missing_required_fields(driver, wait):
    print("\nRunning Test Case: Missing Required Fields")
    driver.get("http://localhost:5000/")
    
    # Fill out the registration form with missing email
    driver.find_element(By.ID, "email").send_keys("")  # Missing email
    driver.find_element(By.ID, "phone").send_keys("3344556677")
    driver.find_element(By.ID, "password").send_keys("NoEmailPass")
    driver.find_element(By.ID, "confirmPassword").send_keys("NoEmailPass")
    driver.find_element(By.ID, "first-name").send_keys("Charlie")
    driver.find_element(By.ID, "last-name").send_keys("Davis")
    driver.find_element(By.ID, "home-address").send_keys("654 Cedar St")
    
    # Generate and enter verification code
    generate_code = driver.find_element(By.XPATH, "//span[text()='Generate Code']")
    generate_code.click()
    print("Clicked on 'Generate Code' for missing fields.")
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert received with text: {alert_text}")
    verification_code = extract_verification_code(alert_text)
    alert.accept()
    print(f"Captured Verification Code: {verification_code}")
    driver.find_element(By.ID, "user-code").send_keys(verification_code)
    
    # Do NOT accept the Terms and Conditions
    print("Did not check the Terms and Conditions box.")
    
    # Attempt to submit the registration form (Register button is disabled)
    register_button = driver.find_element(By.ID, "registerButton")
    if register_button.is_enabled():
        register_button.click()
        print("Clicked on the Register button.")
    else:
        print("Register button is disabled due to missing required fields.")
    
    time.sleep(2)
    
    # Verify missing fields error message
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Missing essential information" in body_text:
        print("Test Passed: Missing required fields were correctly handled.")
    else:
        print("Test Failed: Missing required fields were not handled as expected.")


def main():
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Run all test cases
        test_successful_registration(driver, wait)
        test_duplicate_email_registration(driver, wait)
        test_password_mismatch(driver, wait)
        test_missing_required_fields(driver, wait)
    finally:
        # Close the browser after all tests
        driver.quit()

if __name__ == "__main__":
    main()
