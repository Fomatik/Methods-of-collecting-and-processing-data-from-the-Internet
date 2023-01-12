"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
    Для парсинга использовать XPath. Структура данных должна содержать:
        название источника;
        наименование новости;
        ссылку на новость;
        дата публикации.
2. Сложить собранные новости в БД
    Минимум один сайт, максимум - все три
"""
from datetime import datetime
from pprint import pprint
from urllib.parse import urlparse

import requests
from lxml import html
from pymongo import MongoClient

headers_chrome = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
news_dict = {}


def get_main_news_block(url: str, headers: dict, path: str) -> list:
    """
    Запрос страницы
    :param str url: url адрес страницы
    :param dict headers: заголовки браузера
    :param str path: путь к блоку основных новостей
    :return: html страницы
    :rtype: list
    """
    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=True)
    dom = html.fromstring(response.text)
    main_news_list = dom.xpath(path)
    return main_news_list


def parse_title_date_link_source_from_main_news(main_url, news, title_path, link_path, date_path):
    title = news.xpath(title_path)[0]
    date = news.xpath(date_path)[0]
    if news.xpath(link_path)[0].startswith("http"):
        link = news.xpath(link_path)[0]
    else:
        link = main_url + news.xpath(link_path)[0]
    source = urlparse(link).hostname
    return [title, link, date, source]


def write_parse_results_to_dict(parse_result):
    if parse_result[3] not in news_dict:
        news_dict[parse_result[3]] = []
    news_dict[parse_result[3]].append(parse_result[:3])


def parse_lenta_news():
    """
    Функция для заполнения словаря основными новостями с lenta.ru
    :return: None
    """
    main_url = 'https://lenta.ru'
    path = '//div[contains(@class, "topnews")]/div/a[contains(@class, "topnews")]'
    main_news = get_main_news_block(main_url, headers_chrome, path)

    title = './/*[contains(@class, "title")]/text()'
    date = './/time/text()'
    link = '@href'

    for news in main_news:
        parse_result = parse_title_date_link_source_from_main_news(main_url, news, title, link, date)
        write_parse_results_to_dict(parse_result)


def parse_ria_news():
    """
    Функция для заполнения словаря основными новостями с lenta.ru
    :return: None
    """
    main_url = 'https://ria.ru/world/'
    path = '//div[@class="list-item"]'
    main_news = get_main_news_block(main_url, headers_chrome, path)

    title = './/div[@class="list-item__content"]/a[2]/text()'
    date = './/div[@class="list-item__info"]/div[1]/text()'
    link = './/div[@class="list-item__content"]/a[2]/@href'

    for news in main_news:
        parse_result = parse_title_date_link_source_from_main_news(main_url, news, title, link, date)
        write_parse_results_to_dict(parse_result)


def write_parse_results_to_db(results):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client['news']
    for source in results.keys():
        collection = db[source]
        for news in results[source]:
            title, link, date = news
            collection.insert_one({"title": title, "link": link, "date": date})


def main():
    parse_lenta_news()
    parse_ria_news()
    pprint(news_dict)
    write_parse_results_to_db(news_dict)


if __name__ == '__main__':
    main()
