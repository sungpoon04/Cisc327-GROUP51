from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup Selenium WebDriver
driver = webdriver.Chrome()  # Or webdriver.Firefox(), based on your setup
driver.get("http://127.0.0.1:5000/payment")  # Navigate to the payment page

try:
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    
    # Fill in the payment form
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "method").send_keys("debit")
    driver.find_element(By.NAME, "card_number").send_keys("1111111111111111")
    driver.find_element(By.NAME, "expiration").send_keys("0125")
    driver.find_element(By.NAME, "cvc").send_keys("001")
    driver.find_element(By.NAME, "name_on_card").send_keys("johnsmith")
    driver.find_element(By.NAME, "country").send_keys("CA")
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Wait for the flash message
    flash_message = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flash-message"))  # Adjust class name if necessary
    )
    
    # Verify flash message content
    print("Flash message:", flash_message.text)
    
except TimeoutException:
    print("Test failed: Element not found or took too long to load.")
finally:
    # Close the browser
    driver.quit()
