import csv
import os
import random
import time
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from datetime import datetime
import pandas as pd

folder_path = "html_pages"

def scraping_process():
    links = listing_links("https://www.bizbuysell.com/businesses-for-sale/?q=ZGxhPTM%3D")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()

        page.set_default_navigation_timeout(60000)
        # Navigate to the listings URL
        final_data = []
        i = 0
        for link in links:
            i += 1
            page.goto(link)
            print("scraping: ", link)
            time.sleep(random.uniform(1, 3))
            html_source = page.content()

            # # Save the file to the specified folder
            # file_path = os.path.join(folder_path, f"{i}.html")
            # with open(file_path, "w", encoding="utf-8") as file:
            #     file.write(html_source)
            #
            # print(f"HTML content successfully saved to {file_path}")

            final_data.append(bs4scraper(html_source))
            write_csv(final_data)


def read_html_files(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    filename = '2.html'  # Only process HTML files
    file_path = os.path.join(folder_path, filename)
    # Open and read the HTML content
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
        data_dict = {}
        # Scrape individual listing pages
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract details
            title_element = soup.find('h1', class_='bfsTitle')
            data_dict['Title'] = title_element.text.strip() if title_element else 'N/A'

            location_element = soup.find('span', class_='f-l cs-800 flex-center g8 opacity-70')
            data_dict['Location'] = location_element.text.strip() if location_element else 'N/A'

            asking_price_element = soup.find('span', string='Asking Price:')
            data_dict['Asking Price'] = asking_price_element.find_next_sibling(
                'span').text.strip() if asking_price_element else 'N/A'

            cash_flow_element = soup.find('span', string='Cash Flow:')
            data_dict['Cash Flow'] = cash_flow_element.find_next_sibling(
                'span').text.strip() if cash_flow_element else 'N/A'

            business_description_element = soup.find('div', class_='businessDescription')
            data_dict['Description'] = business_description_element.text.replace("\n",
                                                                                 " ").strip() if business_description_element else 'N/A'

            broker_name_element = soup.find('a', class_='broker-name')
            data_dict['Broker Name'] = broker_name_element.text.strip() if broker_name_element else 'N/A'

            broker_phone_number_element = soup.find('span', class_="ctc_phone")
            data_dict['Phone Number'] = broker_phone_number_element.find('a').get('href').replace("tel:",
                                                                                                  "").strip() if broker_phone_number_element else 'N/A'

            gross_revenue_element = soup.find('span', string='Gross Revenue:')
            data_dict['Gross Revenue'] = gross_revenue_element.find_next_sibling(
                'span').text.strip() if gross_revenue_element else 'N/A'

            ebitda_element = soup.find('span', string='EBITDA:')
            data_dict['EBITDA'] = ebitda_element.find_next_sibling(
                'span').text.strip() if ebitda_element else 'N/A'

            ffe_element = soup.find('span', string='FF&E:')
            data_dict['FF&E'] = ffe_element.find_next_sibling(
                'span').text.strip() if ffe_element else 'N/A'

            inventory_element = soup.find('span', string='Inventory:')
            data_dict['Inventory'] = inventory_element.find_next_sibling(
                'span').text.strip() if inventory_element else 'N/A'

            established_element = soup.find('span', string='Established:')
            data_dict['Established'] = established_element.find_next_sibling(
                'span').text.strip() if established_element else 'N/A'

            rent_element = soup.find('span', string='Rent:')
            data_dict['Rent'] = rent_element.find_next_sibling(
                'span').text.strip() if rent_element else 'N/A'

            employees_element = soup.find('span', attrs={"class": "normal"},string='Employees:')
            data_dict['Employees'] = employees_element.find_parent('dt').find_next_sibling('dd').text.strip() \
                if employees_element else 'N/A'

            facilities_element = soup.find('span',attrs={"class": "normal"},string='Facilities:')
            data_dict['Facilities'] = facilities_element.find_parent('dt').find_next_sibling('dd').text.strip() \
                if facilities_element else 'N/A'

            competition_element = soup.find('span', attrs={"class": "normal"},string='Competition:')
            data_dict['Competition'] = competition_element.find_parent('dt').find_next_sibling('dd').text.strip() \
                if competition_element else 'N/A'

            growth_expansion_element = soup.find('span',attrs={"class": "normal"}, string='Growth & Expansion:')
            data_dict['Growth & Expansion'] = growth_expansion_element.find_parent('dt').find_next_sibling('dd').text.strip().replace("\n", " ") \
                if growth_expansion_element else 'N/A'

            financing_element = soup.find('span',attrs={"class": "normal"}, string='Financing:')
            data_dict['Financing'] = financing_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if financing_element else 'N/A'

            support_element = soup.find('span',attrs={"class": "normal"}, string='Support & Training:')
            data_dict['Support & Training'] = support_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if support_element else 'N/A'

            reason_element = soup.find('span',attrs={"class": "normal"},  string='Reason for Selling:')
            data_dict['Reason for Selling'] = reason_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if reason_element else 'N/A'

            home_element = soup.find('span', attrs={"class": "normal"}, string='Home-Based:')
            data_dict['Home-Based'] = home_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if home_element else 'N/A'

            building_element = soup.find('span', attrs={"class": "normal"}, string='Building SF:')
            data_dict['Building SF'] = building_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if building_element else 'N/A'

            real_estate_element = soup.find('span', attrs={"class": "normal"}, string='Real Estate:')
            data_dict['Real Estate'] = real_estate_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if real_estate_element else 'N/A'

            lease_element = soup.find('span',attrs={"class": "normal"}, string='Lease Expiration:')
            data_dict['Lease Expiration'] = lease_element.find_parent('dt').find_next_sibling(
                'dd').text.strip() \
                if lease_element else 'N/A'
            data_dict["Time Added"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except TimeoutError:
            print("timeout error")

        return data_dict


def bs4scraper(html_content):
    # Initialize data_dict before try block
    data_dict = {}

    # Scrape individual listing pages
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract details
        # Extract details
        title_element = soup.find('h1', class_='bfsTitle')
        data_dict['Title'] = title_element.text.strip() if title_element else 'N/A'

        location_element = soup.find('span', class_='f-l cs-800 flex-center g8 opacity-70')
        data_dict['Location'] = location_element.text.strip() if location_element else 'N/A'

        asking_price_element = soup.find('span', string='Asking Price:')
        data_dict['Asking Price'] = asking_price_element.find_next_sibling(
            'span').text.strip() if asking_price_element else 'N/A'

        cash_flow_element = soup.find('span', string='Cash Flow:')
        data_dict['Cash Flow'] = cash_flow_element.find_next_sibling(
            'span').text.strip() if cash_flow_element else 'N/A'

        business_description_element = soup.find('div', class_='businessDescription')
        data_dict['Description'] = business_description_element.text.replace("\n",
                                                                             " ").strip() if business_description_element else 'N/A'

        broker_name_element = soup.find('a', class_='broker-name')
        data_dict['Broker Name'] = broker_name_element.text.strip() if broker_name_element else 'N/A'

        broker_phone_number_element = soup.find('span', class_="ctc_phone")
        data_dict['Phone Number'] = broker_phone_number_element.find('a').get('href').replace("tel:",
                                                                                              "").strip() if broker_phone_number_element else 'N/A'

        gross_revenue_element = soup.find('span', string='Gross Revenue:')
        data_dict['Gross Revenue'] = gross_revenue_element.find_next_sibling(
            'span').text.strip() if gross_revenue_element else 'N/A'

        ebitda_element = soup.find('span', string='EBITDA:')
        data_dict['EBITDA'] = ebitda_element.find_next_sibling(
            'span').text.strip() if ebitda_element else 'N/A'

        ffe_element = soup.find('span', string='FF&E:')
        data_dict['FF&E'] = ffe_element.find_next_sibling(
            'span').text.strip() if ffe_element else 'N/A'

        inventory_element = soup.find('span', string='Inventory:')
        data_dict['Inventory'] = inventory_element.find_next_sibling(
            'span').text.strip() if inventory_element else 'N/A'

        established_element = soup.find('span', string='Established:')
        data_dict['Established'] = established_element.find_next_sibling(
            'span').text.strip() if established_element else 'N/A'

        rent_element = soup.find('span', string='Rent:')
        data_dict['Rent'] = rent_element.find_next_sibling(
            'span').text.strip() if rent_element else 'N/A'

        employees_element = soup.find('span', attrs={"class": "normal"}, string='Employees:')
        data_dict['Employees'] = employees_element.find_parent('dt').find_next_sibling('dd').text.strip() \
            if employees_element else 'N/A'

        facilities_element = soup.find('span', attrs={"class": "normal"}, string='Facilities:')
        data_dict['Facilities'] = facilities_element.find_parent('dt').find_next_sibling('dd').text.strip() \
            if facilities_element else 'N/A'

        competition_element = soup.find('span', attrs={"class": "normal"}, string='Competition:')
        data_dict['Competition'] = competition_element.find_parent('dt').find_next_sibling('dd').text.strip() \
            if competition_element else 'N/A'

        growth_expansion_element = soup.find('span', attrs={"class": "normal"}, string='Growth & Expansion:')
        data_dict['Growth & Expansion'] = growth_expansion_element.find_parent('dt').find_next_sibling(
            'dd').text.strip().replace("\n", " ") \
            if growth_expansion_element else 'N/A'

        financing_element = soup.find('span', attrs={"class": "normal"}, string='Financing:')
        data_dict['Financing'] = financing_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if financing_element else 'N/A'

        support_element = soup.find('span', attrs={"class": "normal"}, string='Support & Training:')
        data_dict['Support & Training'] = support_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if support_element else 'N/A'

        reason_element = soup.find('span', attrs={"class": "normal"}, string='Reason for Selling:')
        data_dict['Reason for Selling'] = reason_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if reason_element else 'N/A'

        home_element = soup.find('span', attrs={"class": "normal"}, string='Home-Based:')
        data_dict['Home-Based'] = home_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if home_element else 'N/A'

        building_element = soup.find('span', attrs={"class": "normal"}, string='Building SF:')
        data_dict['Building SF'] = building_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if building_element else 'N/A'

        real_estate_element = soup.find('span', attrs={"class": "normal"}, string='Real Estate:')
        data_dict['Real Estate'] = real_estate_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if real_estate_element else 'N/A'

        lease_element = soup.find('span', attrs={"class": "normal"}, string='Lease Expiration:')
        data_dict['Lease Expiration'] = lease_element.find_parent('dt').find_next_sibling(
            'dd').text.strip() \
            if lease_element else 'N/A'

        data_dict["Time Added"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except TimeoutError:
        print("timeout error")

    return data_dict


def write_csv(final_data):
    # Write to CSV if data is available
    if final_data:
        file_name = f"result_{final_data[-1]['Time Added'].split(' ')[0]}.csv"
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=final_data[0].keys())
            writer.writeheader()
            writer.writerows(final_data)
        print(f"Data successfully written to {file_name}")
    else:
        print("No data was scraped. CSV file was not created.")


def listing_links(base_url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        page = context.new_page()


        page.set_default_navigation_timeout(60000)
        # Navigate to the base URL

        page.goto(base_url)
        print("go to main page")

        # Scroll until page stops loading new content
        previous_height = page.evaluate("document.body.scrollHeight")

        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            new_height = page.evaluate("document.body.scrollHeight")
            sleep(3)
            print("scroll down")
            if new_height == previous_height:
                break
            previous_height = new_height
        # wait for pagination to loaded
        page.wait_for_selector("ul.ngx-pagination")

        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        #pagination links
        links =[]
        list_of_page = pagination_links(soup)
        for url in list_of_page:
            print('go to: ', url)
            page.goto(url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            diamonds = soup.find_all('app-listing-diamond')
            showcases = soup.find_all('app-listing-showcase')
            basics = soup.find_all('app-listing-basic')
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

    return links


def pagination_links(soup):
    pagination_template = soup.find( class_='ngx-pagination')
    items = pagination_template.find_all('li')
    list_of_text_in_pagination = []
    for item in items:
        item_text = item.get_text().strip()
        list_of_text_in_pagination.append(item_text)
    maximum_page = max_page(list_of_text_in_pagination)
    # generate links of each page
    pages_link =[]
    for p in range(1, maximum_page+1):
        page_link = f"https://www.bizbuysell.com/businesses-for-sale/{p}/?q=ZGxhPTM%3D"
        pages_link.append(page_link)
    return pages_link

def max_page(page_list):
    num_list = []
    for item in page_list:
        try:
            if int(item):
                num_list.append(int(item))
        except ValueError:
            pass
    return max(num_list)


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