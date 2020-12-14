# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient  # добавляем включаем в сеттингсе пайплайн

class GbParsePipeline:
    def __init__(self):  # Перегружаем инит из паука убираем базу
        self.db = MongoClient()['parse_gb_11_3']

    def process_item(self, item, spider):
        if spider.db_type == 'MONGO':
            collection = self.db[spider.name][spider.name_collection]
            if spider.name_collection == 'company':
                for field in ['web',
                              'activity',
                              'description', ]:
                    item.setdefault(field, 'NULL')
                if 'name' not in item.keys():
                    item.setdefault('name', 'NULL')
                    collection = self.db[spider.name]['NO_NAME_COMP']
            collection.insert_one(item)
        return item