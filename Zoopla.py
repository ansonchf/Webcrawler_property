import requests
from bs4 import BeautifulSoup
import csv
import time


class ZooplaScraper:
    results = []

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        hd = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
        res = requests.get(url, headers = hd)
#        res.encoding = res.apparent_encoding
        print(' | Status code: %s' % res.status_code)
        
        return res
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')        
        
        datas = content.findAll('div', {'class': 'listing-results-wrapper'})
        
        for data in datas:      
            self.results.append({
                'title': data.find('a', {'style': 'text-decoration:underline;'}).text,
                'address': data.find('a', {'class': 'listing-results-address'}).text,
                'date': data.find('p', {'class': 'listing-results-marketed'}).text.split('Listed on')[1].split('by')[0].strip(),
                'description': data.find('p').text.strip(),
                'price': data.find('a', {'class': 'listing-results-price'}).text.strip().split(' ')[0].strip(),
                'phone': data.find('span', {'class': 'agent_phone'})  .text.strip(),
                'link': "https://www.zoopla.co.uk/"+ data.find('a', {'class': 'photo-hover'})['href']
            })
    
    def to_csv(self):
        with open('zoopla_sale.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
        
            for row in self.results:
                writer.writerow(row)
            
            print('Stored results to "zoopla_sale.csv"')
    
    def run(self):
        for page in range(1, 15):
            url = 'https://www.zoopla.co.uk/for-sale/property/glasgow/?identifier=glasgow&page_size=100&q=Glasgow&radius=0&pn='
            url += str(page)
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(1)

        self.to_csv()
        

if __name__ == '__main__':
    scraper = ZooplaScraper()
    scraper.run()
