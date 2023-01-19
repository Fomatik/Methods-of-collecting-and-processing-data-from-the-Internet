# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from unicodedata import normalize

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.bookstore

    def process_item(self, item, spider):
        item = self.normalize_price(item)
        item = self.strip_values(item)
        self.write_to_mongodb(item, spider)
        return item

    @staticmethod
    def normalize_price(item):
        if item['main_price']:
            item['main_price'] = normalize('NFKD', item['main_price']).strip()
        if item['discount_price']:
            item['discount_price'] = normalize('NFKD', item['discount_price']).strip()
        return item

    @staticmethod
    def strip_values(item):
        for k, v in item.items():
            if isinstance(v, list):
                for n, i in enumerate(v):
                    v[n] = i.strip()
                item[k] = ', '.join(v)
            elif isinstance(v, str):
                item[k] = v.strip()
        return item

    def write_to_mongodb(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)

