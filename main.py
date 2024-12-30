import csv
import requests
from bs4 import BeautifulSoup
from scraper.web_scraper import initialize_driver, spider

if __name__ == "__main__":
    driver = initialize_driver()
    spider(driver)
    driver.quit()