import scrapy
import pymongo
import requests, random, base64
import re

class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    ccs_query = {
        'brands': 'div.ColumnItemList_container__5gTrc div.ColumnItemList_column__5gjdt a.blackLink',
        'pagination': '.Paginator_block__2XAPy a.Paginator_button__u1e7D',
        'ads': 'article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = pymongo.MongoClient()['parse_spyder_0912'][self.name]

    def parse(self, response):
        for brand in response.css(self.ccs_query['brands']):
            yield response.follow(brand.attrib.get('href'), callback=self.brand_page_parse)

    def brand_page_parse(self, response):
        for pag_page in response.css(self.ccs_query['pagination']):
            yield response.follow(pag_page.attrib.get('href'), callback=self.brand_page_parse)

        for ads_page in response.css(self.ccs_query['ads']):
            yield response.follow(ads_page.attrib.get('href'), callback=self.ads_parse)

    def ads_parse(self, response):
        data = {
            'title': response.css('.AdvertCard_advertTitle__1S1Ak::text').get(),
            'images': [img.attrib.get('src') for img in response.css('figure.PhotoGallery_photo__36e_r img')],
            'description': response.css('div.AdvertCard_descriptionInner__KnuRi::text').get(),
            'url': response.url,
            'autor': self.extr_author(response),
            'phone': self.extr_tel(response),
            'specification': self.get_specification(response),
        }
        self.db.insert_one(data)

    def get_specification(self, response):
        return {itm.css('.AdvertSpecs_label__2JHnS::text').get(): itm.css(
            '.AdvertSpecs_data__xK2Qx::text').get() or itm.css('a::text').get() for itm in
                response.css('.AdvertSpecs_row__ljPcX')}

    def extr_tel1(self, response):
        _headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36",
        }
        response_mob = requests.get(response.url, headers=_headers)
        tel_patt = '\+7\s\([0-9]+\)\s[0-9]+-[0-9]+-[0-9]+'
        # tel_patt = '(?<=href=\"tel:).+[0-9]{2}-[0-9]{2}'
        tel = re.search(tel_patt, response_mob.text)[0]
        return tel

    def extr_tel2(self, response):
        text = response.xpath('//script[contains(text(), "window.transitState =")]/text()').get()
        tel_str2 = re.findall(r'phone%22%2C%22(.{32})Xw%3D%3D%22%2C%22tim', text)[0]
        tel = base64.b64decode(base64.b64decode(tel_str2.encode())).decode()
        return tel

    def extr_tel(self, response):
        if random.choice('12') == '1':
            # print('tel_1')
            return self.extr_tel1(response)
        else:
            # print('tel_2')
            return self.extr_tel2(response)


    def extr_author(self, response):
        try:
            text = response.xpath('//script[contains(text(), "window.transitState =")]/text()').get()
            patt = r'(?<=youlaId%22%2C%22)[0-9|a-zA-Z]+(?=%22%2C%22avatar)'
            youlaId = re.search(patt, text)[0]
            youlaId_url = f'https://youla.ru/user/{youlaId}'
        except TypeError:
            text = response.text
            patt = r'(?<=Fcardealers%2F)[0-9|a-zA-Z|-]+'
            youlaId = re.search(patt, text)[0]
            youlaId_url = f'https://auto.youla.ru/cardealers/{youlaId}'
        return youlaId_url
'''
В рамках ДЗ - два метода извлечения телефона:
1. get-запросом с мобильным юзерагентом, 
2. с расшифровкой телефона из текста скрипта. 
При извлечении автора помимо физических лиц добавлены автосалоны
'''
