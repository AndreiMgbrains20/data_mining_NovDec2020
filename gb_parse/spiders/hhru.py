import scrapy
from hw_05.gb_parse.gb_parse.loaders import HHVacancyLoader, HHCompanyLoader

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    name_collection = ''
    db_type = 'MONGO'  # этикетка паука можно использовать для разделения пауков по пайпланам
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    xpath_query = {
        'pagination': '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
        'vacancy_urls': '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
        'company': '//div[contains(@class, "vacancy-company__details")]//a/@href',
        'company_vacancy': '//a[@data-qa="employer-page__employer-vacancies-link"]/@href',
    }
    # шаблон
    itm_vac_template = {
        "title": '//h1[@data-qa="vacancy-title"]/text()',
        "salary": '//p[@class="vacancy-salary"]//text()',
        "description": '//div[@data-qa="vacancy-description"]//text()',
        "skills": '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/text()',
        "company_url": '//a[@data-qa="vacancy-company-name"]/@href',
    }

    itm_comp_template = {
        'name': '//h1/span[contains(@class, "company-header-title-name")]/text()',
        'web': '//a[contains(@data-qa, "company-site")]/@href',
        'activity': '//div[contains(@class, "employer-sidebar-content")]//p/text()',
        'description': '//div[contains(@data-qa, "company-description")]//text()',
    }

    def parse(self, response):
        for pag_page in response.xpath(self.xpath_query['pagination']):
            yield response.follow(pag_page, callback=self.parse)

        for vacancy_page in response.xpath(self.xpath_query['vacancy_urls']):
            yield response.follow(vacancy_page, callback=self.vacancy_parse)

    def vacancy_parse(self, response, **kwargs):
        self.name_collection = 'vacancy'
        loader = HHVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self.itm_vac_template.items():
            loader.add_xpath(key, value)

        yield loader.load_item()
        yield response.follow(response.xpath(self.itm_vac_template['company_url']).get(), callback=self.company_parse)

    def company_parse(self, response, **kwargs):
        self.name_collection = 'company'
        loader = HHCompanyLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self.itm_comp_template.items():
            loader.add_xpath(key, value)

        yield loader.load_item()

        if response.xpath(self.xpath_query['company_vacancy']).get():
            yield response.follow(response.xpath(self.xpath_query['company_vacancy']).get(), callback=self.parse)