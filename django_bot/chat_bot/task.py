import random
import time

from celery import shared_task

from chat_bot.constant import RENT_ALIAS, SALE_ALIAS
from chat_bot.utils import strat_scrape_and_update

RENT_URL = "https://www.sothebysrealty.com/eng/rentals/london-en-gbr"
SALE_URL = "https://www.sothebysrealty.com/eng/sales/london-en-gbr"


@shared_task
def scrape_homes(all_pages: bool = False):
    print(f"Start scraping homes... All pages: {all_pages}")

    for type_of_purchase, url in ((RENT_ALIAS, RENT_URL), (SALE_ALIAS, SALE_URL)):
        strat_scrape_and_update(type_of_purchase, url, all_pages)
        time.sleep(random.randint(4, 10))

    print("Scraping homes finished!")
