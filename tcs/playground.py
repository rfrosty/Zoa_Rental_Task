from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver (replace with the appropriate WebDriver for your browser)
driver = webdriver.Chrome()

# Navigate to the shopping bag page
driver.get("https://www.hirestreetuk.com/shopping-bag")

# Wait for the "Checkout" button to be clickable
checkout_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Checkout')]"))
)

# Click on the "Checkout" button
checkout_button.click()

# Close the browser
driver.quit()