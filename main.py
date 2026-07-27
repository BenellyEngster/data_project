from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Automatically open Google Chrome
driver = webdriver.Chrome()

# Access the website we want to test/scrape
driver.get("https://www.python.org/")
print("Opened page title:", driver.title)

# Find the search bar by the NAME attribute 
search = driver.find_element(By.NAME, "q")

# Type the word "loops" into the search box and press ENTER on the keyboard
search.send_keys("loops")
search.send_keys(Keys.RETURN)

try:
    # Explicit wait: wait up to 10 seconds until the results container is present in the DOM
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-recent-events"))
    )
    
    # Find all list items (<li> tags) inside the results container
    articles = main.find_elements(By.TAG_NAME, "li")
    
    # Loop through the results and print the text of each article found
    for article in articles:
        print("->", article.text)

finally:
    # Wait 5 seconds to visually observe the browser, then close it and end the session.
    time.sleep(5)
    driver.quit()

