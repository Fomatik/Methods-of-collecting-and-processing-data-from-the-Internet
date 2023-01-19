import os
import sys

sys.path.append(os.path.abspath(__file__))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.book24 import Book24Spider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(Book24Spider)
    process.start()
