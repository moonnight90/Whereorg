
import logging
from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
import os

OUTPUT_FILE = "Data.csv"

# Configure minimalistic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

save_results = lambda results: pd.DataFrame(results).to_csv(OUTPUT_FILE,index=False,mode='a',header=not os.path.exists(OUTPUT_FILE))

class Scraper():

    def __init__(self) -> None:
        self.client = Session()
        self.client.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        # Set up a logger
        self.logger = logging.getLogger('Scraper')

    def make_request(self, url):
        self.logger.debug(f'Making request to {url}')
        resp = self.client.get(url)
        return resp
    
    def make_soup(self, resp):
        self.logger.debug('Creating BeautifulSoup object')
        return BeautifulSoup(resp.content, 'lxml')
    
    def extract_text(self, soup, selector):
        try:
            return soup.select_one(selector).getText(strip=True)
        except:
            return ''

    def scrape_link(self, url):
        self.logger.info(f'Scraping link: {url}')
        soup = self.make_soup(self.make_request(url))
        listings = soup.select('#business-listings>div.company-block')
        results =  [{
            "Title": self.extract_text(i, 'a.company-list-title'),
            "Address#1": self.extract_text(i, 'div.addr-only'),
            "Address#2": self.extract_text(i, 'div.addr-bot'),
            "Phone": self.extract_text(i, 'div.phone')
        } for i in listings]

        save_results(results)
        self.logger.info(f'Scraped and Saved {len(results)} entries from {url}')
    def filter_categories(self, url, sub=False):
        self.logger.debug(f'Filtering categories for: {url}')
        soup = self.make_soup(self.make_request(url))
        categories = soup.select('div.category>ul>li')
        for category in categories:
            numbers = self.extract_text(category, 'span')
            url = "https://www.whereorg.com" + category.select_one('a')['href']

            if int(numbers) <= 100 or sub:
                self.scrape_link(url)
            else:
                self.filter_categories(url, sub=True)

    def filter_location(self, url):
        self.logger.debug(f'Filtering location for: {url}')
        resp = self.make_request(url)
        soup = self.make_soup(resp)
        locations_lis = soup.select('div.location>ul>li')
        # content = soup.select_one('div.filter-location>div.fitler-field-content').getText(strip=True)
        content = self.extract_text(soup,'div.filter-location>div.fitler-field-content')
        content = 'City or suburb' if content == '' else content

        for li in locations_lis:
            url = "https://www.whereorg.com" + li.select_one('a')['href']
            if content.find('City or suburb') == -1:
                self.filter_location(url)
            else:
                # full_text = li.getText(strip=True)
                numbers = li.select_one('span').getText(strip=True)
                if int(numbers) <= 100:
                    self.scrape_link(url)
                else:
                    self.filter_categories(url)

    def run(self, url):
        self.logger.info(f'Starting scraping process for: {url}')
        self.filter_location(url)

if __name__ == "__main__":
    Scraper().run(input('main_category_link? '))
