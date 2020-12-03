# Lesson 02. Home work. Vers.1
# Урок 2. Парсинг HTML. BeautifulSoup, MongoDB

#Задание
#пример структуры и типы обязательно хранить поля даты как объекты datetime
#{
#    "url": str,
#    "promo_name": str,
#    "product_name": str,
#    "old_price": float,
#    "new_price": float,
#    "image_url": str,
#    "date_from": "DATETIME",
#    "date_to": "DATETIME",
#}

#pip install bs4 lxml pymongo python-dotenv

import os
import time
import re
import datetime as dt
import requests
import bs4
import pymongo
import dotenv
from urllib.parse import urljoin
import requests

dotenv.load_dotenv('.env')

url_magn_msk = 'https://magnit.ru/promo/?geo=moskva'

print('Испольуется ОС: ', os.name)
#req_magn_msk = requests.get(url_magn_msk)
#print('Заголовки: \n', url_magn_msk.headers)
#print('Ответ: \n', url_magn_msk.text)

class MagnitParse:
    mon_to_num = {'ноября': 11, 'декабря': 12, 'января': 1, 'февраля': 2}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }
    akcii = set()
    def __init__(self, start_url):
        self.start_url = start_url
        client = pymongo.MongoClient(os.getenv('DATA_BASE'))
        self.db = client['magnit_parse_29_11']
        self.product_template = {
            'url': lambda soup: urljoin(self.start_url, soup.get('href')),
            'promo_name': lambda soup: soup.find('div', attrs={'class': 'card-sale__header'}).text,
            'product_name': lambda soup: soup.find('div', attrs={'class': 'card-sale__title'}).text,
            'old_price': lambda soup: self.extr_price(soup, 'old'),
            'new_price': lambda soup: self.extr_price(soup, 'new'),
            'image_url': lambda soup: urljoin(self.start_url, soup.find('img').get('data-src')),
            'date_from': lambda soup: self.extr_date(soup, 1),
            'date_to': lambda soup: self.extr_date(soup, 3),
        }

    def extr_price(self, soup, type_price):
        if type_price == 'old':
            class_price = 'label__price_old'
        elif type_price == 'new':
            class_price = 'label__price_new'
        return float(soup.find('div', attrs={'class': f'{class_price}'}).contents[1].text + '.' + soup.find('div', attrs={'class': f'{class_price}'}).contents[3].text)

    def extr_date(self, soup, num):
        s = re.search(r'(?<=\w\s).*', soup.find('div', attrs={'class': 'card-sale__date'}).contents[num].text)[0]
        s = s.split(' ')
        data = dt.datetime(2010 if self.mon_to_num[s[1]] < 8 else 2020, self.mon_to_num[s[1]], int(s[0]))
        return data

    @staticmethod
    def _get(*args, **kwargs):
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise Exception
                return response
            except Exception:
                time.sleep(0.5)

    def soup(self, url) -> bs4.BeautifulSoup:
        response = self._get(url, headers=self.headers)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def run(self):
        soup = self.soup(self.start_url)
        for product in self.parse(soup):
            try:
                self.save(product)
            except KeyError:
                collection = self.db['errors']
                collection.insert_one(product)
                continue

    def parse(self, soup):
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})

        for product in catalog.find_all('a', recursive=False):
            pr_data = self.get_product(product)
            yield pr_data

    def get_product(self, product_soup) -> dict:

        result = {}
        for key, value in self.product_template.items():
            try:
                result[key] = value(product_soup)
            except Exception as e:
                continue
        return result

    def save(self, product):
        self.akcii.add(product['promo_name'])
        collection = self.db['m_2911']
        collection.insert_one(product)

if __name__ == '__main__':
    parser = MagnitParse(url_magn_msk)
    parser.run()
