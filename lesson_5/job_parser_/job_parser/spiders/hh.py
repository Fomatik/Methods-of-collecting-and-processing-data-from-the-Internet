import os
import sys

sys.path.append(os.path.abspath('../job_parser'))

import scrapy
from scrapy.http import HtmlResponse
from items import JobParserItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python']

    def parse(self, response, **kwargs):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath(
            "//div[@class='serp-item']//a[@data-qa='serp-item__title']/@href").getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        vacancy_url = response.url

        yield JobParserItem(
            name=vacancy_name,
            salary=vacancy_salary,
            url=vacancy_url
        )
