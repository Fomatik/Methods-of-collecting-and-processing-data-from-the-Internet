"""
Собрать информацию о вакансиях на вводимую должность с сайтов hh.ru и/или Superjob и/или работа.ру.
Приложение должно анализировать несколько страниц сайта.
Получившийся список должен содержать в себе минимум:
 1. Наименование вакансии.
 2. Предлагаемую зарплату (дополнительно: разносим в три поля: минимальная и максимальная и валюта.
 Цифры преобразуем к цифрам).
 3. Ссылку на саму вакансию.
 4. Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с всех сайтов.
Общий результат можно вывести с помощью dataFrame через pandas, сохранить в json, либо csv.
"""
import csv
from pprint import pprint
from time import sleep
from types import NoneType

import requests
from bs4 import BeautifulSoup, Tag

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
vacancies = {}


def check_for_none(data: Tag) -> list[str] | str:
    """
    В некоторых вакансиях не указана зарплата.
    Проверяем на None.
    Убираем Unicode пробелы.
    :param data: строка с указанной зарплатой
    :type data: Tag
    :return: словарь с зарплатой или пустую строку
    :rtype: list[str] | str
    """
    if isinstance(data, NoneType):
        return ''
    return data.get_text().replace('\u202f', '').split(' ')


def get_page_count(link: str, headers: dict, params: dict) -> int:
    """
    Получение номера последней страницы
    :param str link: ссылка
    :param dict headers: заголовки браузера
    :param dict params: параметры запроса
    :return: номер последней страницы
    :rtype: int
    """
    response = response_for_request(link, headers, params)
    soup = get_soup_from_response(response)
    last_page = soup.find_all('span', class_='pager-item-not-in-short-range')[-1].get_text()
    return int(last_page)


def response_for_request(link: str, headers: dict, params: dict) -> str:
    """
    Запрос страницы
    :param str link: url страницы
    :param dict headers: заголовки браузера
    :param dict params: параматры запроса
    :return: html страницы
    :rtype: str
    """
    response = requests.get(link, headers=headers, params=params)
    return response.text


def get_soup_from_response(response: str) -> BeautifulSoup:
    """
    Преобразование html в объект BeautifulSoup
    :param str response: html строка
    :return: объект BeautifulSoup
    :rtype: BeautifulSoup
    """
    soup = BeautifulSoup(response, 'lxml')
    return soup


def hh_vacancies(search_query: str):
    """
    Получение страницы с поисковым параметром с сайта hh.ru и дальнейший парсинг вакансий.
    Запись полученных вакансий в словарь
    :param str search_query: строка запроса
    :return: None
    """
    hh_url = f'https://hh.ru/search/vacancy'
    params = {'text': search_query}
    if 'hh.ru' not in vacancies:
        vacancies['hh.ru'] = []
    max_page = 5    # для быстрой работы указано определённое количество страниц
    # max_page = get_page_count(hh_url, headers, params)   # получение всех страниц
    for page in range(max_page):
        params['page'] = page
        response = response_for_request(hh_url, headers, params)
        soup = get_soup_from_response(response)
        vacancies_cards = soup.find_all('div', class_='vacancy-serp-item__layout')
        for card in vacancies_cards:
            title = card.find('a').get_text()
            salary = check_for_none(card.find('span', class_='bloko-header-section-3'))
            if isinstance(salary, list):
                if salary[0] == 'от':
                    min_salary = int(salary[1])
                    max_salary = '-'
                    currency = salary[2]
                elif salary[0] == 'до':
                    min_salary = '-'
                    max_salary = int(salary[1])
                    currency = salary[2]
                else:
                    min_salary = int(salary[0])
                    max_salary = int(salary[2])
                    currency = salary[3]
            else:
                min_salary = 0
                max_salary = 0
                currency = '-'

            link = card.find('a')['href']
            vacancies['hh.ru'].append([title, min_salary, max_salary, currency, link])
        sleep(3)


def write_vacancies_to_csv(data: list):
    """
    Запись результатов парсинга в csv файл
    :param list data: списки с вакансиями
    :return: None
    """
    with open('vacancies.csv', 'w') as v:
        headlines = ['title', 'min_salary', 'max_salary', 'currency', 'link']
        write = csv.writer(v)
        write.writerow(headlines)
        for lists in data:
            write.writerow(lists)


def main():
    hh_vacancies('Python')
    pprint(vacancies)
    write_vacancies_to_csv(vacancies['hh.ru'])


if __name__ == '__main__':
    main()
