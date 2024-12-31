import csv
import random
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def initialize_driver():
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,  # Block notifications
        # Add other preferences as needed
    })
    # Run in headless mode (no GUI)
    driver = uc.Chrome(options=options)
    return driver


def bs4scraper_playwright(base_url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()


        page.set_default_navigation_timeout(60000)
        # Navigate to the base URL

        page.goto(base_url)


        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all listings
        listing_container = soup.find('div', class_="listing-container")

        diamonds = soup.find_all('app-listing-diamond')
        showcases = soup.find_all('app-listing-showcase')
        basics = soup.find_all('app-listing-basic')

        links = []

        for diamond in diamonds:
            try:
                href = diamond.find('a')['href'].replace('"', "").replace("\\", "")
                if 'www.bizbuysell.com' in href:
                    links.append(href)
                else:
                    links.append('https://www.bizbuysell.com' + href)
            except (AttributeError, KeyError):
                pass

        for showcase in showcases:
            try:
                href = showcase.find('a')['href'].replace('"', "").replace("\\", "")
                if 'www.bizbuysell.com' in href:
                    links.append(href)
                else:
                    links.append('https://www.bizbuysell.com' + href)
            except (AttributeError, KeyError):
                pass

        for basic in basics:
            try:
                href = basic.find('a')['href'].replace('"', "").replace("\\", "")
                if 'www.bizbuysell.com' in href:
                    links.append(href)
                else:
                    links.append('https://www.bizbuysell.com' + href)
            except (AttributeError, KeyError):
                pass

        print("links: ", links)
        final_data = []

        # Scrape individual listing pages
        for link in links:

            print('Scraping:', link)
            try:
                page.goto(link)
                time.sleep(random.uniform(1, 3))
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract details
                title_element = soup.find('h1', class_='bfsTitle')
                title = title_element.text.strip() if title_element else 'N/A'

                location_element = soup.find('span', class_='f-l cs-800 flex-center g8 opacity-70')
                location = location_element.text.strip() if location_element else 'N/A'

                asking_price_element = soup.find('span', string='Asking Price:')
                asking_price = asking_price_element.find_next_sibling('span').text.strip() if asking_price_element else 'N/A'

                cash_flow_element = soup.find('span', string='Cash Flow:')
                cash_flow = cash_flow_element.find_next_sibling('span').text.strip() if cash_flow_element else 'N/A'

                business_description_element = soup.find('div', class_='businessDescription')
                business_description = business_description_element.text.replace("\n",
                                                                                 " ").strip() if business_description_element else 'N/A'

                broker_name_element = soup.find('a', class_='broker-name')
                broker_name = broker_name_element.text.strip() if broker_name_element else 'N/A'

                broker_phone_number_element = soup.find('span', class_="ctc_phone")
                phone_number = broker_phone_number_element.find('a').get('href').replace("tel:",
                                                                                         "").strip() if broker_phone_number_element else 'N/A'

                data = {
                    'Title': title,
                    'Location': location,
                    'Asking Price': asking_price,
                    'Cash Flow': cash_flow,
                    'Description': business_description,
                    'Broker Name': broker_name,
                    'Phone Number': phone_number,
                }
                final_data.append(data)
            except TimeoutError:
                print("TimeoutError")

        # Write to CSV if data is available
        if final_data:
            file_name = "result.csv"
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=final_data[0].keys())
                writer.writeheader()
                writer.writerows(final_data)
            print(f"Data successfully written to {file_name}")
        else:
            print("No data was scraped. CSV file was not created.")


def bs4scraper_selenium(html_content, driver):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all listings
    listing_container = soup.find('div', class_="listing-container")

    diamonds = soup.find_all('app-listing-diamond')
    showcases = soup.find_all('app-listing-showcase')
    basics = soup.find_all('app-listing-basic')

    links = []

    for diamond in diamonds:
        try:
            href = diamond.find('a')['href'].replace('"', "").replace("\\", "")
            if 'www.bizbuysell.com' in href:
                links.append(href)
            else:
                links.append('https://www.bizbuysell.com' + href)
        except (AttributeError, KeyError):
            pass

    for showcase in showcases:
        try:
            href = showcase.find('a')['href'].replace('"', "").replace("\\", "")
            if 'www.bizbuysell.com' in href:
                links.append(href)
            else:
                links.append('https://www.bizbuysell.com' + href)
        except (AttributeError, KeyError):
            pass

    for basic in basics:
        try:
            href = basic.find('a')['href'].replace('"', "").replace("\\", "")
            if 'www.bizbuysell.com' in href:
                links.append(href)
            else:
                links.append('https://www.bizbuysell.com' + href)
        except (AttributeError, KeyError):
            pass

    print("links: ", links)
    final_data = []

    # Scrape individual listing pages
    for link in links:
        print('Scraping:', link)
        driver.get(link)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract details
        title_element = soup.find('h1', class_='bfsTitle')
        title = title_element.text.strip() if title_element else 'N/A'

        location_element = soup.find('span', class_='f-l cs-800 flex-center g8 opacity-70')
        location = location_element.text.strip() if location_element else 'N/A'

        asking_price_element = soup.find('span', string='Asking Price:')
        asking_price = asking_price_element.find_next_sibling('span').text.strip() if asking_price_element else 'N/A'

        cash_flow_element = soup.find('span', string='Cash Flow:')
        cash_flow = cash_flow_element.find_next_sibling('span').text.strip() if cash_flow_element else 'N/A'

        business_description_element = soup.find('div', class_='businessDescription')
        business_description = business_description_element.text.replace("\n",
                                                                         " ").strip() if business_description_element else 'N/A'

        broker_name_element = soup.find('a', class_='broker-name')
        broker_name = broker_name_element.text.strip() if broker_name_element else 'N/A'

        broker_phone_number_element = soup.find('span', class_="ctc_phone")
        phone_number = broker_phone_number_element.find('a').get('href').replace("tel:",
                                                                                 "").strip() if broker_phone_number_element else 'N/A'

        data = {
            'Title': title,
            'Location': location,
            'Asking Price': asking_price,
            'Cash Flow': cash_flow,
            'Description': business_description,
            'Broker Name': broker_name,
            'Phone Number': phone_number,
        }
        final_data.append(data)
    # Write to CSV if data is available
    if final_data:
        file_name = "result.csv"
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=final_data[0].keys())
            writer.writeheader()
            writer.writerows(final_data)
        print(f"Data successfully written to {file_name}")
    else:
        print("No data was scraped. CSV file was not created.")

def spider_selenium(driver):

    driver.get("https://www.bizbuysell.com/businesses-for-sale/?q=ZGxhPTM%3D")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait until document.readyState is 'complete'
    # Example: Wait for a product element to be visible
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    wait.until(EC.presence_of_element_located((By.XPATH, '//pagination-template')))

    html_content = driver.page_source
    bs4scraper_selenium(html_content, driver)


