from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3

# Create (or open) a database file in your project folder
connection = sqlite3.connect("tjpr_data.db")
cursor = connection.cursor()

# Create the table where raw data will be stored
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_lawsuits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_text TEXT
    )
""")
connection.commit()

# 1. Automatically open Google Chrome
driver = webdriver.Chrome()

# 2. Access the TJPR jurisprudence portal
driver.get("https://portal.tjpr.jus.br/jurisprudencia/")
print("Title of the open page:", driver.title)

# 3. Locate the search bar by the correct ID we discovered
search = driver.find_element(By.ID, "criterioPesquisa")

# 4. Type your master's thesis keyword
search.send_keys("feminicidio")
time.sleep(1)  # Short pause to ensure input is filled

# 5. Locate the main search button and click it
search_button = driver.find_element(By.CLASS_NAME, "btn-icone-pesquisar")
search_button.click()
print("- Femicide research successfully sent to the TJPR")

time.sleep(3)

lawsuits = driver.find_elements(By.CLASS_NAME, "juris-tabela-dados")

print(f"Success, I found  {len(lawsuits)} visible cases on the first page")

for lawsuit in lawsuits:
    raw_text = lawsuit.text

    # Save this text into the table of our .db file
    cursor.execute(
        "INSERT INTO raw_lawsuits (full_text) VALUES (?)", (raw_text,)
    )

# Commit the saved data
connection.commit()
print("- All raw processes have been saved to the database")

# 6. Wait 6 seconds for the results page to load on screen
print("- Page title after the search:", driver.title)

# 7. Safely close the session
driver.quit()
connection.close()
print("- Automation completed without errors")