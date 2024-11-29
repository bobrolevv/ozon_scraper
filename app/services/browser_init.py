import pathlib as p
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

# для WIN
BIN_LOCATION_BROWSER = str(p.Path.cwd() / 'wdrivers' / 'chrome-win64-121' / 'chrome.exe')
BIN_LOCATION_DRIVER = str(p.Path.cwd() / 'wdrivers' / 'chromedriver-win64-121' / 'chromedriver.exe')

def browser_init_undetected():
    return uc.Chrome(
        use_subprocess=False,
    )

def browser_init2(opt={}):

    # useragent
    my_useragent = UserAgent().chrome
    # options

    options = webdriver.ChromeOptions()
    # options.binary_location = BIN_LOCATION_BROWSER
    options.add_argument(f'--user-agent={my_useragent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation")
    if opt.get('page_load_strategy'):
        options.page_load_strategy = opt.get('page_load_strategy')   # не дожидаться загрузки страницы, опция полезна для VC.RU
    if opt.get('disable-notifications'):
        options.add_argument('disable-notifications')

    return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


def browser_init(opt={}): # общий вариант

    # useragent
    my_useragent = UserAgent().chrome
    # options

    options = webdriver.ChromeOptions()
    options.binary_location = BIN_LOCATION_BROWSER
    options.add_argument(f'--user-agent={my_useragent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-automation")
    # options.add_argument("--start-maximized")
    options.add_argument("--window-size=1400,770")
    if opt.get('page_load_strategy'):
        options.page_load_strategy = opt.get('page_load_strategy')   # не дожидаться загрузки страницы, опция полезна для VC.RU
    if opt.get('disable-notifications'):
        options.add_argument('disable-notifications')
    # service
    service = None
    # service = webdriver.ChromeService()
    # service = webdriver.ChromeService(service_args=['--disable-build-check'])  # проверять совместимость браузера и драйвера
    # service = webdriver.ChromeService(executable_path=BIN_LOCATION_DRIVER)

    # proxy
    return webdriver.Chrome(options=options, service=service)


if __name__ == '__main__':
    pass
    # browser_init()