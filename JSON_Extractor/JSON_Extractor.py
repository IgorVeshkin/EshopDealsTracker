# Импорт BeautifulSoup - библиотеки для парсинга данных с web-страницы
from bs4 import BeautifulSoup

# Импорт Selenium - библиотеки для автоматизированого взаимодействия со страницей
from selenium import webdriver

# Работа с JSON
import json

import os

from datetime import datetime


def get_product_data(url: str = 'https://www.nintendo.com/us/store/products/sword-of-the-vagrant-switch/') -> None:

    # Данные начала парсинга
    start_datetime = datetime.now()

    # Базовая настройка selenium и запуск

    driver = webdriver.Edge()
    driver.get(url)

    page = driver.page_source

    driver.quit()


    # Запуск BeautifulSoup

    soup = BeautifulSoup(page, 'html.parser')

    script_tag = soup.find('script', type='application/ld+json')

    if script_tag:

        json_text = script_tag.string

        data = json.loads(json_text)

        name = data['@graph'][0]['name']

        # Меняю формат строки '2025-08-28_20-52-00'
        timestamp_str = start_datetime.strftime("%H-%M-%S__%d-%m-%Y")
        timestamp_str_short = start_datetime.strftime("%d.%m.%Y")

        if not os.path.exists(f'json_dumps/{timestamp_str_short}/basic'):
            os.makedirs(f'json_dumps/{timestamp_str_short}/basic')

        # Сохраняю результаты парсинга в json-файл
        with open(f'json_dumps/{timestamp_str_short}/basic/{name}__output_{timestamp_str}.json', 'w',
                  encoding='utf-8') as file:
            file.write(json_text)
    else:
        print("JSON-данные не были найдены")


# Link example: https://www.nintendo.com/us/store/products/the-liar-princess-and-the-blind-prince-switch/
