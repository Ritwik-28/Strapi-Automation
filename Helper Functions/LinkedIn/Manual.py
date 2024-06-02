from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")

# Start the WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Open the website
    driver.get('https://www.linkedin.com/in/{user_name}/') # Update LinkedIn Profile

    # Wait for the page to load and check for authentication or pop-ups
    wait = WebDriverWait(driver, 10)

    # Handle authentication if it appears
    try:
        username = wait.until(EC.presence_of_element_located((By.NAME, 'session_key')))
        password = driver.find_element(By.NAME, 'session_password')
        login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')

        # Enter your credentials
        username.send_keys('login_id') # Update with dummy account email id
        password.send_keys('password') # Update with dummy account password
        login_button.click()
    except:
        print("No login required or login elements not found")

    # Close pop-up if it appears
    try:
        pop_up_close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/section/button')))
        pop_up_close_button.click()
    except:
        print("No pop-up appeared or pop-up elements not found")

    # Find the image using the provided XPath and download it
    try:
        img = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section[1]/div/section/section[1]/div/div[1]/img')))
        img_url = img.get_attribute('src')

        # Download the image
        img_data = requests.get(img_url).content
        with open('downloaded_image.png', 'wb') as handler:
            handler.write(img_data)

        print("Image downloaded successfully")
    except:
        print("Image not found or failed to download")

finally:
    # Close the browser
    driver.quit()
