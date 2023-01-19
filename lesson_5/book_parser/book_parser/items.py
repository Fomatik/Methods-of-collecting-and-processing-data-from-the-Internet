# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookParserItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    main_price = scrapy.Field()
    discount_price = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
