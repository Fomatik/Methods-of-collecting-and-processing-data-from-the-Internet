# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose


def dict_from_lst(lst):
    keys = lst[::2]
    val = lst[1::2]
    characteristics_list = [{k: v for k, v in zip(keys, val)}]
    return characteristics_list


def strip_whitespace_in_item(item):
    item = [v.strip() for v in item]
    item = [v for v in item if v != '']
    return item


def process_price(value):
    money = 0
    currency = ''
    if value:
        money = int(value[0].replace(' ', ''))
        currency = value[1]
    return {'money': money, 'currency': currency}


class CastoramaParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(strip_whitespace_in_item))
    price = scrapy.Field(input_processor=Compose(strip_whitespace_in_item),
                         output_processor=Compose(process_price))
    photos = scrapy.Field()
    characteristics = scrapy.Field(input_processor=Compose(strip_whitespace_in_item),
                                   output_processor=Compose(dict_from_lst))
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
