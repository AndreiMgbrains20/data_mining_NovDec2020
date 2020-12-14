from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.gb_parse.gb_parse.spiders.hhru import  HhruSpider

'''
В терминале - scrapy startproject hw_05
scrapy в корневой папке создает каталог hw_05 и в нем spiders
и в каталогах необходимые файлы инициализации
в корневой папке создает файл scrapy.cfg
делаем паука набрав в терминале scrapy genspider autoyoula auto.youla.ru
один паук один сайт
создается файл паука с привязкой к доменному имени
'''
# from hw_05 import settings

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule('hw_05.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    # crawl_proc.crawl(AutoyoulaSpider) # добавляем пауков такими строками
    crawl_proc.crawl(HhruSpider) # добавляем пауков такими строками
    crawl_proc.start()