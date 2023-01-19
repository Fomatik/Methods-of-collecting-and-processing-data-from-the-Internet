import os
import sys

sys.path.append(os.path.abspath(__file__))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.hh import HhSpider
from spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(HhSpider)
    process.crawl(SuperjobSpider)
    process.start()
