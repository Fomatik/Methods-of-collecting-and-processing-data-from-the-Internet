# Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.
import json
import requests

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

querystring = {"country": "Russia"}

headers = {
    "X-RapidAPI-Key": "0d8db1a59fmsh50bae794405e941p179569jsne0983d7c8d3e",
    "X-RapidAPI-Host": "covid-19-coronavirus-statistics.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

with open('covid_stat.json', 'w') as f:
    json.dump(response.json(), f)
