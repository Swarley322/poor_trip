import random
import requests
import time
from selenium import webdriver


def get_random_sleep_time():
    return random.randint(1, 3)


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    try:
        result = requests.get(url, headers=headers)
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_html_selenium(url):
    # for local using
    # chromedriver = "/Users/dmitrykim/projects/poor_trip/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # for local using
    # browser = webdriver.Chrome(executable_path=chromedriver, options=options)
    capabilities = options.to_capabilities()
    browser = webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub",
                desired_capabilities=capabilities
    )
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    browser.quit()
    return html
