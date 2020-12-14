from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.autoyoula import AutoyoulaSpider

'''
в терминале - scrapy startproject gb_parse.
scrapy в корневой папке создает каталог gb_parse, в нем spiders и в каталогах необходимые файлы инициализации в корневой папке создает файл scrapy.cfg
делаем паука набрав в терминале scrapy genspider autoyoula auto.youla.ru
один паук один сайт
создается файл паука с привязкой к доменному имени
'''

# from gb_parse import settings

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    # crawl_settings.setmodule(settings) если днелали from gb_parse import settings
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(AutoyoulaSpider) # добавляем пауков такими строками
    crawl_proc.start()
