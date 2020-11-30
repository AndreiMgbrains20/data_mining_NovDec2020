# Lesson 01. Home work. Vers.1

#pip install requests
import os
from pathlib import Path
import json
import time
import requests

url_5ka_offers = 'https://5ka.ru/special_offers/'
url_5ka_categories = 'https://5ka.ru/api/v2/categories/'
#url_magnit = 'https://magnit.ru/promo'

print('Испольуется ОС: ', os.name)
req_5ka = requests.get(url_5ka_offers)
print('Заголовки: \n', req_5ka.headers)
print('Ответ: \n', req_5ka.text)

class Parse5ka:
    _headers = {
        'User-Agent': "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    }
    _params = {
        'records_per_page': 50,
    }

    def __init__(self, start_url):
        self.start_url = start_url

    @staticmethod
    def _get(*args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    # todo Создать класс исключение
                    raise Exception
                return response
            except Exception:
                time.sleep(0.025)

    def parse(self, url):
        params = self._params
        while url:
            response: requests.Response = self._get(url, params=params, headers=self._headers)
            if params:
                params = {}
            data: dict = response.json()
            url = data.get('next')
            yield data.get('results')

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                self._save_to_file(product, product['id'])
            time.sleep(0.01)

    @staticmethod
    def _save_to_file(product, file_name):
        path = Path(os.path.dirname(__file__)).joinpath('products').joinpath(f'{file_name}.json')
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(product, file, ensure_ascii=False)


class Parse5ka_category(Parse5ka):

    def __init__(self, start_url, category_url):
        self.category_url = category_url
        super().__init__(start_url)

    def get_category(self, url_cat):
        response = self._get(url_cat, headers=self._headers)
        return response.json()

    def run(self):
        for category in self.get_category(self.category_url):
            data = {
                'name': category['parent_group_name'],
                'code': category['parent_group_code'],
                'products': []
            }
            self._params['categories'] = category['parent_group_code']
            print(data['name'])
            for products in self.parse(self.start_url):
                data['products'].extend(products)
                self._save_to_file(data, data['code'])
            time.sleep(0.01)

if __name__ == '__main__':
    parser = Parse5ka_category(url_5ka_offers, url_5ka_categories)
    parser.run()