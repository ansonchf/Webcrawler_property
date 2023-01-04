import requests
from bs4 import BeautifulSoup
import csv
import time


class RightmoveScraper:
    results = []

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        hd = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        res = requests.get(url, headers = hd)
#        res.encoding = res.apparent_encoding
        print(' | Status code: %s' % res.status_code)
        
        return res
    
#    def parse(self, html):
#        content = BeautifulSoup(html, 'lxml')        
        
#        datas = content.findAll('div', {'class': 'l-propertySearch-results propertySearch-results'})
        
#        for data in datas:      
#            self.results.append({
#                'title': data.find('h2', {'class': 'propertyCard-title'}).text.strip(),
#                'address': data.find('meta', {'itemprop': 'streetAddress'}).text.strip(),
#                'date': data.find('span', {'propertyCard-branchSummary-addedOrReduced'}).text.split()[-1],
#                'description': data.find('span', { 'data-test': 'property-description'}).text.strip(),
#                'price': data.find('div', {'class': 'propertyCard-priceValue'}).text.strip(),
#                'phone': data.find('a', {'class': 'propertyCard-contactsPhoneNumber'})  .text.strip(),
#                'link': "https://www.rightmove.co.uk/"+ data.find('a', {'class': 'propertyCard-link'})['href']
#            })
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        
        titles = [title.text.strip() for title in content.findAll('h2', {'class': 'propertyCard-title'})]
        addresses = [address['content'] for address in content.findAll('meta', {'itemprop': 'streetAddress'})]
        dates = [date.text.split(' ')[-1] for date in content.findAll('span', {'class': 'propertyCard-branchSummary-addedOrReduced'})]
        descriptions = [description.text for description in content.findAll('span', {'data-test': 'property-description'})]
        prices = [price.text.strip() for price in content.findAll('div', {'class': 'propertyCard-priceValue'})]
        phones = [phone.text.strip() for phone in content.findAll('a', {'class': 'propertyCard-contactsPhoneNumber'})]
        links = [link['href'] for link in content.findAll('a', {'data-test': 'property-details'})]
        
        for index in range(0, len(titles)):
            self.results.append({
                'title': titles[index],
                'address': addresses[index],
                'date': dates[index],
                'description': descriptions[index],
                'price': prices[index],
                'phone': phones[index],
                'link': "https://www.rightmove.co.uk/" + links[index],
            })
    
    def to_csv(self):
        with open('rightmove_sale.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
        
            for row in self.results:
                writer.writerow(row)
            
            print('Stored results to "Rightmove_sale.csv"')
    
    def run(self):
        for page in range(0, 43):
            index = page * 24
            url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E550&sortType=6&index=' + str(index) + '&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='
           
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(1)

        self.to_csv()
        

if __name__ == '__main__':
    scraper = RightmoveScraper()
    scraper.run()
