import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Function to set a random User-Agent
def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'
        # Add more user agents as needed
    ]
    return random.choice(user_agents)

# Function to add random delays
def random_delay():
    time.sleep(random.uniform(1, 3))

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Open Google
driver.get("https://usa.visa.com/support/consumer/travel-support/exchange-rate-calculator.html")

# Handle cookies (if prompted)
try:
    accept_cookies = driver.find_element(By.XPATH, '//button[text()="I agree"]')
    accept_cookies.click()
except:
    pass

random_delay()

# Find the search box using its name attribute value
search_box = driver.find_element(By.NAME, "q")

# Send the text "Selenium" to the search box
search_box.send_keys("Selenium")

# Add a random delay before pressing Enter
random_delay()

# Press Enter/Return
search_box.send_keys(Keys.RETURN)

# Wait for the results to load
random_delay()

# Find all the result titles
titles = driver.find_elements(By.TAG_NAME, "h3")

# Print the titles
for title in titles:
    print(title.text)

# Close the browser
driver.quit()
