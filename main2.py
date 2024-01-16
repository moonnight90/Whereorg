from requests import Session
from bs4 import BeautifulSoup



class Scraper():

    def __init__(self) -> None:
        self.client = Session()
        self.client.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})


    def make_request(self,url):
        resp = self.client.get(url)
        return resp
    
    def make_soup(self,resp):

        return BeautifulSoup(resp.content,'lxml')
    
    def extract_text(self,soup,selector):
        try:
            return soup.select_one(selector).getText(strip=True)
        except:
            return ''

    def scrape_link(self,url):
        soup = self.make_soup(self.make_request(url))
        listings = soup.select('#business-listings>div.company-block')
        results =  [{
            "Title":self.extract_text(i,'a.company-list-title'),
            "Address#1": self.extract_text(i,'div.addr-only'),
            "Address#2": self.extract_text(i,'div.addr-bot'),
            "Phone": self.extract_text(i,'div.phone')
        } for i in listings]
        
    
    def filter_categories(self,url,sub=False):
        soup = self.make_soup(self.make_request(url))

        categories = soup.select('div.category>ul>li')
        for category in categories:
            numbers = self.extract_text(category,'span')
            url = "https://www.whereorg.com"+category.select_one('a')['href']

            if int(numbers)<=100 or sub:
                self.scrape_link(url)
            else:
                self.filter_categories(url,sub=True)
                
    
    

    def filter_location(self,url):
        resp = self.make_request(url)
        soup = self.make_soup(resp)
        states_lis = soup.select('div.location>ul>li')
        content = soup.select_one('div.filter-location>div.fitler-field-content').getText(strip=True)

        for li in states_lis:
            url = "https://www.whereorg.com"+li.select_one('a')['href']
            if content.find('City or suburb')==-1:
                self.filter_location(url)
            else:
                full_text = li.getText(strip=True)
                numbers = li.select_one('span').getText(strip=True)
                if int(numbers)<=100:
                    self.scrape_link(url)
                else:
                    self.filter_categories(url)


                


    def run(self,url):
        self.filter_location(url)
        



if __name__ == "__main__":
    Scraper().run('https://www.whereorg.com/businesses/food-all')
