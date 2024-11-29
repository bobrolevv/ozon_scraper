import multiprocessing
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
# import undetected_chromedriver as uc
# from pkg_resources import parse_version
from bs4 import BeautifulSoup
from requests import options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait

# from app.parser_telemetr import driver
from .services.functions import page_down, collect_product_info, collect_img
from .services.browser_init import browser_init_undetected as uc
from bs4 import BeautifulSoup


# driver = uc()
# ac = ActionChains(driver)


def get_products_links():

    driver = uc()
    ac = ActionChains(driver)

    driver.implicitly_wait(5)

    URL = 'https://www.ozon.ru/'

    print('[INFO] Сбор данных начался. Пожалуйста ожидайте...')
    driver.get(url=URL)
    time.sleep(5)

    try:
        # поиск текста "топ-выгода", поиск родителя типа "а" и извлечение ссылки из неё
        link_top_cash = (driver.find_element(By.XPATH,
            "//*[contains(text(), 'Топ-выгода')]/ancestor::a").get_attribute("href"))
        print(link_top_cash)

        driver.switch_to.new_window('tab')
        time.sleep(1)
        driver.get(url=link_top_cash)
        time.sleep(3)

        # сбор ссылок на товары со всех видимых карточек
        # (ac.send_keys(Keys.PAGE_DOWN).
         # pause(1).send_keys(Keys.PAGE_DOWN).
         # pause(1).send_keys(Keys.PAGE_DOWN).
         # pause(1).send_keys(Keys.PAGE_DOWN).
         # pause(1).send_keys(Keys.PAGE_DOWN).
         # pause(1).send_keys(Keys.PAGE_DOWN).
         # perform())
        # time.sleep(5)
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))
        print(len(products_urls))

        print('[+] Ссылки на товары собраны!')
    except Exception as ex:
        print(f'[!] Что-то сломалось при сборе ссылок на товары! ({ex})')

    products_urls_dict = {}

    for k, v in enumerate(products_urls):
        products_urls_dict.update({k: v})

    with open('data/products_urls_dict.json', 'w', encoding='utf-8') as file:
        json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)

    # сортировка по рейтингу
    # current_url = f'{driver.current_url}&sorting=rating'
    # driver.get(url=current_url)
    # time.sleep(2)

    products_data = []

    for url in products_urls:
        data = collect_product_info(driver=driver, url=url)
        print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
        time.sleep(2)
        products_data.append(data)

    with open('data/PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()

    print('[INFO] Работа выполнена успешно!')

if __name__ == '__main__':
    pass

    # print('start')
    # collect_img(driver=driver, url='')

    # print('[INFO] Сбор данных начался. Пожалуйста ожидайте...')
    # get_products_links(driver=driver)
    #     # item_name='наушники hyperx'
    # print('[INFO] Работа выполнена успешно!')

