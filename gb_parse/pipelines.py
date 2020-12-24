# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request # запросы из Scrapy
from scrapy.pipelines.images import ImagesPipeline # Работа с картинками
from pymongo import MongoClient  # добавляем включаем в сеттингсе пайплайн
from .loaders import stopcheck, treemaker, pathfinder
db_name = 'parse_gb_hands_new'


class GbParsePipeline:
    def __init__(self):  # Перегружаем инит из паука убираем базу
        client = MongoClient()
        client.drop_database(db_name)
        self.db = MongoClient()[db_name]

    def process_item(self, item, spider):

        if spider.db_type == 'MONGO_YOULA':
            collection = self.db[spider.name]
            collection.insert_one(item)

        if spider.db_type == 'MONGO_HH':
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

        if spider.name == 'instagram':

            if 'img' in item.keys():
                collection = self.db[spider.name]['tag_img']
            if 'follow_id' in item.keys():
                collection = self.db[spider.name]['follow']
            if 'index' in item.keys():
                if item['index'] == 'user_data':
                    collection = self.db[spider.name]['user_data']
                if item['index'] == 'tag':
                    collection = self.db[spider.name]['tag']

            collection.insert_one(item)

        if spider.name == 'handshake':
            if item['index'] == 'follow':
                collection = self.db[spider.name]['follow']
            if item['index'] == 'subs':
                collection = self.db[spider.name]['subs']
            collection.insert_one(item)

        return item


class GbImagePipeline(ImagesPipeline):  # Картинки с ЮЛЫ

    def get_media_requests(self, item, info):
        if info.spider.name == 'autoyoula':
            for img_url in item.get('images', []):
                yield Request(img_url)

        if info.spider.name == 'instagram':
            if 'img' in item.keys():
                yield Request(item['img'])

    def item_completed(self, results, item, info):
        if results:
            if info.spider.name == 'autoyoula':
                item['images'] = [itm[1] for itm in results]

            if info.spider.name == 'instagram':
                item['img'] = results[0][1]
        return item


class GbParseHandsh:
    def __init__(self):
        self.db = MongoClient()[db_name]

    def process_item(self, item, spider):
        if spider.name == 'handshake':
            collection = self.db[spider.name]
            if item['follow_id'] == spider.target['user_id']:
                stopcheck(item, collection, spider)
            if spider.stop == 'stop':
                if item['follow_id'] == spider.target['user_id']:
                    treemaker(collection, self.db)
                    pathfinder(self.db, spider.target)

        return item
