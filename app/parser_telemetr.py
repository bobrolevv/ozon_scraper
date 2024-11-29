from app.services.browser_init import browser_init_undetected
import time, json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import collect_product_info

URL = 'https://ozon.ru/'
# URL = 'https://telemetr.me/analytics/?name=Интересная+Москва'

driver = browser_init_undetected()

# try:
#     driver.get(url=URL)
#     time.sleep(1)
#
#     # for cookie in pickle.load(open('cookes', "rb")):
#     #     driver.add_cookie(cookie)
#     #     print(cookie)
#
#     # driver.refresh()
#     # driver.get(URL)
#     input('exit?')
#     # pickle.dump(driver.get_cookies(), open('cookes', "wb"))
#     time.sleep(5)
#
# except Exception as Ex:
#     print(Ex)
# finally:
#     driver.close()
#     driver.quit()

def get_products_links(item_name='наушники hyperx'):
    # driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}&sorting=rating'
    driver.get(url=current_url)
    time.sleep(2)

    # page_down(driver=driver)
    time.sleep(2)

    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))

        print('[+] Ссылки на товары собраны!')
    except:
        print('[!] Что-то сломалось при сборе ссылок на товары!')

    products_urls_dict = {}

    for k, v in enumerate(products_urls):
        products_urls_dict.update({k: v})

    with open('../data/products_urls_dict.json', 'w', encoding='utf-8') as file:
        json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)

    time.sleep(2)

    products_data = []

    for url in products_urls:
        data = collect_product_info(driver=driver, url=url)
        print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
        time.sleep(2)
        products_data.append(data)

    with open('../data/PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()

if __name__ == '__main__':
    get_products_links()