# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from unicodedata import normalize
from pymongo import MongoClient


class JobParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.python_vacancies

    def process_item(self, item, spider):
        item = self.normalize_salary(item)

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    @staticmethod
    def normalize_salary(item):
        item['salary'] = normalize('NFKD', ''.join(item['salary']))
        return item
