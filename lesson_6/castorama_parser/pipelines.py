# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from logging import info
from itemadapter import ItemAdapter
import os
import platform
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urljoin, urlparse


class CastoramaParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.castorama

    def process_item(self, item, spider):
        self.write_to_mongodb(item, spider)
        return item

    def write_to_mongodb(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)


class CastoramaPhotosPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        if platform.system() == 'Linux':
            item['name'] = [v.replace('/', '\\') for v in item['name']]
            return f'{item["name"][0]}/{os.path.basename(urlparse(request.url).path)}'
        elif platform.system() == 'Windows':
            return fr'{item["name"][0]}\{os.path.basename(urlparse(request.url).path)}'

    def get_media_requests(self, item, info):
        if item.get('photos'):
            item['photos'] = [urljoin(info.spider.start_urls[0], url) for url in item['photos']]
            for img in item.get('photos'):
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
