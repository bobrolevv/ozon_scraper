import time as tm
import os
import app.services.browser_init
from sys import path_hooks

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import RelativeBy, locate_with

from app.services.browser_init import browser_init_undetected


def page_down(driver):
    driver.execute_script('''
                            const scrollStep = 200; // Размер шага прокрутки (в пикселях)
                            const scrollInterval = 100; // Интервал между шагами (в миллисекундах)

                            const scrollHeight = document.documentElement.scrollHeight;
                            let currentPosition = 0;
                            const interval = setInterval(() => {
                                window.scrollBy(0, scrollStep);
                                currentPosition += scrollStep;

                                if (currentPosition >= scrollHeight) {
                                    clearInterval(interval);
                                }
                            }, scrollInterval);
                        ''')


def collect_img(driver):
    # url = 'https://www.ozon.ru/product/nastolnaya-igra-dlya-vzroslyh-nuar-gaga-games-148541477/?_bctx=CAYQ8qtI&asb2=ei84WKytQGam8f8iHKnQemlyZ4UUFy5Zo47H7N1DVn79oK0Id1L00GeweNzYYmH7SktI7d2XkI0DX1ij79IH3A&avtc=1&avte=4&avts=1732891577&reviewsVariantMode=2'
    # driver=driver
    #
    # driver.switch_to.new_window('tab')
    #
    # tm.sleep(3)
    # driver.get(url=url)
    # tm.sleep(3)

    media = []

    try:
        # ищем галерею картинок и проходимся по ней сохраняя ссылки на изображения
        webgallery = driver.find_element(By.XPATH, '//div[@data-widget="webGallery"]')
        divs_img = webgallery.find_elements(By.XPATH, "//div[@data-index]")
        print('найдено элементов галереи:',len(divs_img))

        for el in divs_img[:5]:
            el.click()
            print('img click', el.get_attribute('data-index'))
            tm.sleep(1)

            if (webgallery.find_element(By.XPATH, "//img[@data-lcp-name]")):
                img = webgallery.find_element(By.XPATH, "//img[@data-lcp-name]")
                img_src = img.get_attribute('src')
                media.append(img_src)
            elif (driver.find_element(By.TAG_NAME, 'video-player')):
                vid_src = driver.find_element(By.TAG_NAME, 'video-player').get_attribute('src')
                media.append(vid_src)
            else:
                continue

        # ищем последний элемент (ссылку на видео) и сохраняем ее
        terget = driver.find_element(locate_with(By.TAG_NAME, 'div').below(divs_img[-1]))
        terget.click()

        tm.sleep(2)
        if driver.find_element(By.TAG_NAME, 'video-player'):
            vid_src = driver.find_element(By.TAG_NAME, 'video-player').get_attribute('src')
            media.append(vid_src)



    except Exception as ex:
        print(ex)

    return media


def collect_product_info(driver, url=''):

    driver.switch_to.new_window('tab')

    tm.sleep(3)
    driver.get(url=url)
    tm.sleep(3)

    # product_id
    product_id = driver.find_element(
        By.XPATH, '//div[contains(text(), "Артикул: ")]'
    ).text.split('Артикул: ')[1]

    media = collect_img(driver=driver)

    page_source = str(driver.page_source)
    soup = BeautifulSoup(page_source, 'lxml')

    path = f'data/{product_id}/product_{product_id}.html'
    dir_name = os.path.dirname(path)
    os.makedirs(dir_name, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(page_source)

    product_name = soup.find('div', attrs={"data-widget": 'webProductHeading'}).find(
        'h1').text.strip().replace('\t', '').replace('\n', ' ')

    # product_id
    # try:
    #     product_id = soup.find('div', string=re.compile(
    #         'Артикул:')).text.split('Артикул: ')[1].strip()
    # except:
    #     product_id = None

    # product statistic
    try:
        product_statistic = soup.find(
            'div', attrs={"data-widget": 'webSingleProductScore'}).text.strip()

        if " • " in product_statistic:
            product_stars = product_statistic.split(' • ')[0].strip()
            product_reviews = product_statistic.split(' • ')[1].strip()
        else:
            product_statistic = product_statistic
    except:
        product_statistic = None
        product_stars = None
        product_reviews = None

    # product price
    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
        product_ozon_card_price = ozon_card_price_element.text.strip(
        ) if ozon_card_price_element else ''

        price_element = soup.find(
            'span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

        product_discount_price = price_element[0].text.strip(
        ) if price_element[0] else ''
        product_base_price = price_element[1].text.strip(
        ) if price_element[1] is not None else ''
    except:
        product_ozon_card_price = None
        product_discount_price = None
        product_base_price = None

    # product price
    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
    except AttributeError:
        card_price_div = soup.find(
            'div', attrs={"data-widget": "webPrice"}).findAll('span')

        product_base_price = card_price_div[0].text.strip()
        product_discount_price = card_price_div[1].text.strip()

    product_data = (
        {
            'product_url': url,
            'product_id': product_id,
            'product_name': product_name,
            'product_ozon_card_price': product_ozon_card_price,
            'product_discount_price': product_discount_price,
            'product_base_price': product_base_price,
            'product_statistic': product_statistic,
            'product_stars': product_stars,
            'product_reviews': product_reviews,
            'media': media
        }
    )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return product_data


if __name__ == '__main__':
    driver = browser_init_undetected()
    # print(collect_img(driver))
