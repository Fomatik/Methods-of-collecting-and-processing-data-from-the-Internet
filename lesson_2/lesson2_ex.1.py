"""
1. Написать приложение или функцию, которые собирают основные новости с сайта на выбор lenta.ru, Yandex-новости.
Для парсинга использовать XPath.

Структура данных в виде словаря должна содержать:
 -*название источника;
 -наименование новости;
 -ссылку на новость;
 -дата публикации.

Минимум один сайт, максимум - все два.
"""
from pprint import pprint
import requests
from urllib.parse import urlparse
from lxml import html

main_url = 'https://lenta.ru/'  # Лента.ру
headers_chrome = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
lenta_main_news_xpath = "//div[contains(@class, 'topnews')]/div/a[contains(@class, 'topnews')]"  # XPath к блокам основных новостей


def get_main_news(url: str, headers: dict[str, str], path: str) -> list:
    """
    Функция для получения html url-а и парсинга основной части по XPath
    :param url:str ссылка на сайт
    :param headers:dict[str, str] изменение заголовков в запросе
    :param path:str XPath путь к основному блоку(ам)
    :return:list html объект(ы) документа
    """
    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=True)
    dom = html.fromstring(response.text)
    main_news_list = dom.xpath(path)
    print(type(main_news_list))
    return main_news_list


def create_dict_lenta_news_title_link_date(news: list) -> dict:
    """
    Функция для получения словаря с основными новостями с lenta.ru
    :param news:list объекты html документа
    :return: dict key: источник новости, value:список списков [заголовок, ссылка, время публикации]
    """
    news_dict = dict()
    for item in news:
        title = item.xpath(".//*[contains(@class, 'title')]/text()")[0]
        date = item.xpath(".//time/text()")[0]
        if item.xpath("@href")[0].startswith("http"):
            link = item.xpath("@href")[0]
        else:
            link = main_url + item.xpath("@href")[0]
        source = urlparse(link).hostname
        if source not in news_dict:
            news_dict[source] = []
        news_dict[source].append([title, link, date])
    return news_dict


if __name__ == "__main__":
    # Распарсил только Ленту, так как Яндекс без JS не работает уже.
    main_news = get_main_news(main_url, headers_chrome, lenta_main_news_xpath)
    news_from_lenta = create_dict_lenta_news_title_link_date(main_news)
    pprint(news_from_lenta)
