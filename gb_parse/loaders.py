import re, base64
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from hw_05.gb_parse.gb_parse.spiders.items import AutoYoulaItem
from hw_05.gb_parse.gb_parse.spiders.items import HHVacancyItem, HHCompanyItem

# AutoYoula Function
def get_autor(js_string):
    re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
    result = re.findall(re_str, js_string)
    return f'https://youla.ru/user/{result[0]}' if result else None


def get_tel(js_string):
    text = js_string
    tel_str2 = re.findall(r'phone%22%2C%22(.{32})Xw%3D%3D%22%2C%22tim', text)[0]
    tel = base64.b64decode(base64.b64decode(tel_str2.encode())).decode()
    return tel


def get_specifications(itm):
    tag = Selector(text=itm)
    result = {tag.css('.AdvertSpecs_label__2JHnS::text').get(): tag.css(
        '.AdvertSpecs_data__xK2Qx::text').get() or tag.css('a::text').get()}
    return result

def specifications_out(data: list):
    result = {}
    for itm in data:
        result.update(itm)
    return result
# AutoYoula Function END

class AutoYoulaLoader(ItemLoader):
    default_item_class = AutoYoulaItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_out = TakeFirst()
    autor_in = MapCompose(get_autor)
    autor_out = TakeFirst()
    phone_in = MapCompose(get_tel)
    phone_out = TakeFirst()
    specifications_in = MapCompose(get_specifications)
    specifications_out = specifications_out

# HH Function
def companyUrl(url):
    return f'https://hh.ru{url}'

def extr_name(data):
    if data != []:
        data = ''.join(data[:2])
    else:
        data = 'Данные отсутствуют'
    return data

# HH Function END

class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    company_url_in = MapCompose(companyUrl)
    company_url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()

class HHCompanyLoader(ItemLoader):
    default_item_class = HHCompanyItem
    name_out = extr_name
    url_out = TakeFirst()
    web_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    activity_out = TakeFirst()