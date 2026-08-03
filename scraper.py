from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

def scrape_tjpr_data():
    print("Starting the scraper bot...")
    
    # Connect to the existing database (which database.py should have created)
    connection = sqlite3.connect("tjpr_data.db")
    cursor = connection.cursor()

    # 1. Automatically open Google Chrome
    driver = webdriver.Chrome()

    # 2. Access the TJPR jurisprudence portal
    driver.get("https://portal.tjpr.jus.br/jurisprudencia/")
    print("Title of the open page:", driver.title)

    # 3. Locate the search bar
    search = driver.find_element(By.ID, "criterioPesquisa")

    # 4. Type the keyword
    search.send_keys("feminicidio")
    time.sleep(1)  # Short pause to ensure input is filled

    # 5. Locate and click the search button
    search_button = driver.find_element(By.CLASS_NAME, "btn-icone-pesquisar")
    search_button.click()
    print("Femicide research successfully sent to the TJPR")

    time.sleep(3) # Wait for the results to load on the screen

    # Collect the lawsuit blocks
    lawsuits = driver.find_elements(By.CLASS_NAME, "juris-tabela-dados")
    print(f"Success. I found {len(lawsuits)} visible cases on the first page.")

    # For loop: Save each raw text to the database
    for lawsuit in lawsuits:
        raw_text = lawsuit.text
        cursor.execute(
            "INSERT INTO raw_lawsuits (full_text) VALUES (?)", (raw_text,)
        )

    # Commit the saved data
    connection.commit()
    print("All raw processes have been saved to the database")

    driver.quit()
    connection.close()
    print("Automation completed without errors")