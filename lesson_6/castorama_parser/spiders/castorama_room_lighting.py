import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lesson_6.castorama_parser.items import CastoramaParserItem


class CastoramaRoomLightingSpider(scrapy.Spider):
    name = 'castorama_room_lighting'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/lighting/interior-lighting/led-strip/?PAGEN_3=1']

    def parse(self, response: HtmlResponse):
        try:
            next_page = response.xpath('//a[@class="next i-next"]')[0]
            if next_page:
                yield response.follow(next_page, callback=self.parse)
        except IndexError:
            print('Last page')

        product_links = response.xpath('//li[contains(@class, "product-card")]/a[2]')
        for product_link in product_links:
            yield response.follow(product_link, callback=self.product_parse)

    def product_parse(self, response):
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//div[1]/div[1]/div[1]/div[1]/span[1]/span[1]/span[1]//text()')
        loader.add_xpath('photos', '//span[@itemprop="image"]/@content')
        loader.add_xpath('characteristics', '//div[contains(@class, "product-specifications")]/dl//text()')
        loader.add_value('url', response.url)
        yield loader.load_item()
