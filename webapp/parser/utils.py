import random
import requests
import time
from selenium import webdriver


def get_random_sleep_time():
    return random.randint(1, 5)


def get_random_proxy():
    proxy_list = [
        {"http": "", "https": ""},
        {"http": "http://kimdima93:W2i7WcZ@193.233.78.190:65233", "https": "https://kimdima93:W2i7WcZ@193.233.78.190:65233"},
        {"http": "http://kimdima93:W2i7WcZ@89.191.225.120:65233", "https": "https://kimdima93:W2i7WcZ@89.191.225.120:65233"},
        {"http": "http://kimdima93:W2i7WcZ@194.113.232.57:65233", "https": "https://kimdima93:W2i7WcZ@194.113.232.57:65233"},
        {"http": "http://kimdima93:W2i7WcZ@5.188.55.12:65233", "https": "https://kimdima93:W2i7WcZ@5.188.55.12:65233"},
        {"http": "http://kimdima93:W2i7WcZ@85.239.43.92:65233", "https": "https://kimdima93:W2i7WcZ@85.239.43.92:65233"},
        {"http": "http://kimdima93:W2i7WcZ@146.120.110.239:65233", "https": "https://kimdima93:W2i7WcZ@146.120.110.239:65233"},
        {"http": "http://kimdima93:W2i7WcZ@92.63.195.229:65233", "https": "https://kimdima93:W2i7WcZ@92.63.195.229:65233"},
        {"http": "http://kimdima93:W2i7WcZ@91.236.120.33:65233", "https": "https://kimdima93:W2i7WcZ@91.236.120.33:65233"},
        {"http": "http://kimdima93:W2i7WcZ@45.128.184.67:65233", "https": "https://kimdima93:W2i7WcZ@45.128.184.67:65233"},
        {"http": "http://kimdima93:W2i7WcZ@80.66.85.181:65233", "https": "https://kimdima93:W2i7WcZ@80.66.85.181:65233"},
    ]
    proxy = proxy_list[random.randint(0, 10)]
    return proxy


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    proxy = get_random_proxy()
    try:
        result = requests.get(url, headers=headers, proxies=proxy)
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_html_selenium(url):
    # chromedriver = "/Users/dmitrykim/projects/poor_trip/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # browser = webdriver.Chrome(executable_path=chromedriver, options=options)
    capabilities = options.to_capabilities()
    browser = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", desired_capabilities=capabilities)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    browser.quit()
    return html
