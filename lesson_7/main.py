from datetime import datetime
from pprint import pprint
import dateutil.parser
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)

client = MongoClient('localhost', 27017)
mongobase = client.mail_ru
collection = mongobase['mail']

driver.get('https://account.mail.ru/login')

login = driver.find_element(By.NAME, "username")
driver.implicitly_wait(10)
login.send_keys("test_parsing@mail.ru")
login.send_keys(Keys.ENTER)

pwd = driver.find_element(By.NAME, "password")
driver.implicitly_wait(10)
pwd.send_keys("xMkG$k44")
submit = driver.find_element(By.XPATH, "//button[@data-test-id='submit-button']")
submit.click()

mails_list = set()

page = driver.find_element(By.XPATH, "//div[@id='sideBarContent']//a[1]").get_attribute("title").split()

for i in range(int(page[1]) // 5):
    mails = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")
    for mail in mails:
        if link := mail.get_attribute('href'):
            mails_list.add(link)
    actions = ActionChains(driver)
    actions.scroll_to_element(mails[-3])
    actions.perform()

for mail in mails_list:
    driver.get(mail)
    title = driver.find_element(By.TAG_NAME, 'h2').text
    author = driver.find_element(By.XPATH, "//div[@class='letter__author']/span").get_attribute('title')
    date = driver.find_element(By.XPATH, "//div[@class='letter__date']").text
    mail_body = driver.find_element(By.XPATH, "//div[@class='letter__body']").text.strip()

    collection.insert_one({'title': title, 'author': author, 'date': date, 'body': mail_body})


driver.close()
