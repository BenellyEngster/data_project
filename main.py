import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 1. Read and initially display the CSV dataset
try:
    df = pd.read_csv(
        "data/homicidios-e-feminicidios.csv",
        encoding="latin-1",
        sep=";"
    )
    print("--- First rows of the CSV file ---")
    print(df.head())
    print("-" * 40)
except Exception as e:
    print(f"Warning: Could not read the CSV file. Error: {e}")
    print("-" * 40)

# 2. Browser configuration and initialization using Options
options = Options()
# If you want to run the browser in the background (headless mode) in the future, just uncomment the line below:
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# 3. Access the website and automate the search (Web Scraping)
driver.get("https://www.python.org/")
print("Opened page title:", driver.title)

# Find the search bar by its NAME attribute
search = driver.find_element(By.NAME, "q")

# Type the word "loops" into the search box and press ENTER on the keyboard
search.send_keys("loops")
search.send_keys(Keys.RETURN)

try:
    # Explicit wait: wait up to 15 seconds (increased to prevent Timeout errors) until the results container is present in the DOM
    main = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-recent-events"))
    )
    
    # Find all list items (<li> tags) inside the results container
    articles = main.find_elements(By.TAG_NAME, "li")
    
    print("\n--- Results found on the Web ---")
    for article in articles:
        print("->", article.text)

finally:
    # Wait 5 seconds to visually observe the browser behavior
    time.sleep(5)
    
    # Safety shield: Try to close the browser without freezing the terminal if the connection dropped or timed out
    try:
        driver.quit()
    except Exception as e:
        print("The browser was already closed or did not respond to the shutdown command.")