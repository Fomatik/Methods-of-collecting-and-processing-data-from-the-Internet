import os
import sys

sys.path.append(os.path.abspath('../job_parser'))

import scrapy
from scrapy.http import HtmlResponse
from items import JobParserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']
    list_job = []

    def parse(self, response):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath(
            "//div[contains(@class, 'f-test-vacancy-item')]/div/div/div/div/div/div/div/div/span/a[contains(@class, 'f-test-link')]/@href").getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        print(response.url)
        SuperjobSpider.list_job.append(response.url)
        print(len(SuperjobSpider.list_job))
        vacancy_name = response.xpath("//h1/text()").get()
        vacancy_salary = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]/div/div[1]/div/span//text()").getall()
        vacancy_url = response.url

        yield JobParserItem(
            name=vacancy_name,
            salary=vacancy_salary,
            url=vacancy_url
        )
