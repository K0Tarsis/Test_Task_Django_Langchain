import random
import re
import time
from typing import List, Union
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from chat_bot.models import Homes

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def strat_scrape_and_update(type_of_purchase: str, url: str, all_pages: bool = False):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:

        scrape_and_update(
            driver=driver,
            type_of_purchase=type_of_purchase,
            url=url,
            all_pages=all_pages
        )

    finally:
        driver.quit()

def scrape_and_update(driver: webdriver.Chrome, type_of_purchase: str, url: str, all_pages: bool = False):
    data_on_page, next_page_href = scrape_page(url, driver)

    for data in data_on_page:
        try:

            data.update({"type_of_purchase": type_of_purchase})

            Homes.objects.update_or_create(
                title=data['title'],
                type_of_purchase=type_of_purchase,
                defaults=data
            )

        except Exception as e:
            pass

    print(f"Number of items found: {len(data_on_page)}")
    print(f"Next page URL: {next_page_href}")

    if next_page_href and all_pages:
        time.sleep(random.randint(4, 10))
        scrape_and_update(
            driver=driver,
            type_of_purchase=type_of_purchase,
            url=next_page_href,
            all_pages=all_pages
        )


def scrape_page(url: str, driver: webdriver.Chrome) -> tuple[List[dict], Union[str, None]]:
    driver.get(url)

    try:

        data_on_page = scrape_data(driver)

    except:
        data_on_page = None
        time.sleep(random.randint(2, 7))

    try:
        next_page_element = driver.find_element(
            By.CSS_SELECTOR,'a.Pagination__item.Pagination__item--arrow[rel="next"]'
        )
        next_page_href = next_page_element.get_attribute('href') if next_page_element else None

    except:
        next_page_href = None

    return data_on_page, next_page_href


def scrape_data(driver: webdriver.Chrome) -> List[dict]:
    """
    Extracts property data from the current page using Selenium.
    """
    data_on_page = []

    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.grid__item.Search-results__item'))
        )

    all_items = driver.find_elements(By.CSS_SELECTOR, '.grid__item.Search-results__item')

    for item in all_items:
        try:
            results_body = item.find_element(By.CSS_SELECTOR, '.Results-card__body')

            title, address = get_title_and_address(results_body)
            price = int(re.sub(r"[^\d]", "", results_body.find_element(By.CSS_SELECTOR, '.Results-card__body-price').text.strip()))
            bedrooms, bathrooms, area = get_number_of_bedrooms_bathrooms_and_area(results_body)

            data_on_page.append({
                'title': title,
                'price': price,
                'address': address,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area': area,
                'summary': results_body.text.strip()  # Optionally store the full summary
            })

        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    return data_on_page


def get_title_and_address(results_body: WebElement) -> tuple[str, Union[str, None]]:
    try:
        title_and_address = results_body.find_element(By.CSS_SELECTOR, '.Results-card__body-address-wrapper')
        h3_tags = title_and_address.find_elements(By.TAG_NAME, 'h3')

        if len(h3_tags) >= 2:
            title = h3_tags[0].text.strip()
            address = h3_tags[1].text.strip()
        else:
            title = title_and_address.text.strip()
            address = None

        return title, address
    except Exception as e:
        print(f"Error extracting title and address: {e}")
        return "", None


def get_number_of_bedrooms_bathrooms_and_area(results_body: WebElement) -> tuple[
    Union[int, None], Union[int, None], Union[int, None]]:
    bedrooms, bathrooms, area = None, None, None

    try:
        feat_list = results_body.find_element(By.CSS_SELECTOR, '.Results-card__feat-list')
        li_tags = feat_list.find_elements(By.TAG_NAME, 'li')

        if len(li_tags) == 2:
            bedrooms = int(li_tags[0].text.strip().split(' ')[0])
            area = int(li_tags[1].text.strip().split(' ')[0].replace(',', ''))

        elif len(li_tags) == 3:
            bedrooms = int(li_tags[0].text.strip().split(' ')[0])
            bathrooms = int(li_tags[1].text.strip().split(' ')[0])
            area = int(li_tags[2].text.strip().split(' ')[0].replace(',', ''))

    except Exception as e:
        print(f"Error extracting features: {e}")

    return bedrooms, bathrooms, area
