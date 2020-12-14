

'''
Версия 1.

Урок 4. Парсинг HTML. XPath

Источник https://auto.youla.ru/
Обойти все марки авто и зайти на странички объявлений
Собрать след стуркутру и сохранить в БД Монго
Название объявления
Список фото объявления (ссылки)
Список характеристик
Описание объявления
ссылка на автора объявления
дополнительно попробуйте вытащить телефона


'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.autoyoula import AutoyoulaSpider


if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(AutoyoulaSpider)
    crawl_proc.start()
