import os
import sys

sys.path.append(os.path.abspath('../book_parser'))

import scrapy
from scrapy.http import HtmlResponse
from items import BookParserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']

    def parse(self, response, **kwargs):
        next_page = response.xpath("//a[contains(@class, '_next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_books = response.xpath(
            "//div[@class='product-list__item']//a[contains(@class, 'product-card__image-link')]/@href").getall()
        for url_book in urls_books:
            yield response.follow(url_book, callback=self.book_parse)

    @staticmethod
    def book_parse(response: HtmlResponse):
        book_url = response.url
        book_name = response.css("h1::text").get()
        if ':' in book_name:
            book_name = book_name.split(':')[1]
        book_price = response.xpath(
            "//div[@class='product-sidebar-price product-sidebar__price-holder']//text()").getall()
        if len(book_price) > 1:
            book_main_price = book_price[0]
            book_discount_price = book_price[1]
            book_discount = book_price[2]
        else:
            book_main_price = book_price[0]
            book_discount_price = None
            book_discount = None

        book_author = response.xpath("//div[dt//span[contains(text(), 'Автор')]]/dd//text()").getall()

        book_rating = response.xpath("//div[contains(@class, 'rating-widget')]//text()").getall()[:2]

        yield BookParserItem(
            url=book_url,
            name=book_name,
            author=book_author,
            main_price=book_main_price,
            discount_price=book_discount_price,
            discount=book_discount,
            rating=book_rating
        )
