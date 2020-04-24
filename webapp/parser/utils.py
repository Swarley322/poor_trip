import random
import requests
import time
from selenium import webdriver


def get_random_sleep_time():
    return random.randint(0, 4)


def get_random_proxy():
    proxy_list = [
            {
                "http": "http://kimdima93:W2i7WcZ@185.41.161.110:65233",
                "https": "https://kimdima93:W2i7WcZ@185.41.161.110:65233"
            }

    ]
    proxy = proxy_list[random.randint(0, 2)]
    return proxy


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    proxy = {"http": "http://kimdima93:W2i7WcZ@185.41.161.110:65233",
             "https": "https://kimdima93:W2i7WcZ@185.41.161.110:65233"}
    try:
        # result = requests.get(url, headers=headers, proxies=proxy)
        result = requests.get(url, headers=headers)
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_html_selenium(url):
    chromedriver = "/Users/dmitrykim/projects/poor_trip/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=chromedriver, options=options)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    browser.quit()
    return html
