# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import json

import requests

user = 'gvanrossum'  # Имя аккаунта
url = f'https://api.github.com/users/{user}/repos'  # URL на пользовательские публичные репозитории
headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

request_user_repo = requests.get(url=url, headers=headers)
data = request_user_repo.json()

# Полная запись все данных всех репозиториев пользователя
with open(f'{user}_repo_full.json', 'w') as repo_file:
    json.dump(data, repo_file)

# Запись имени и времени создания репозиториев пользователя
repo_name = {}
for repo in data:
    repo_name[repo['name']] = repo['created_at']

with open(f'{user}_repo_name.json', 'w') as repo_file:
    json.dump(repo_name, repo_file)
