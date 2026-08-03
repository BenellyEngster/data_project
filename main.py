import database  
import scraper   
import treatment 

database.create_tables()

scraper.scrape_tjpr_data()

treatment.clean_data()

print("PROJECT EXECUTED SUCCESSFULLY")