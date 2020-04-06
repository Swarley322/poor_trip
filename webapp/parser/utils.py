import random
import requests


def get_random_proxy():
    proxy_list = [
        "http://learn:python@t1.learn.python.ru:1080/",
        "http://learn:python@t2.learn.python.ru:1080/",
        "http://learn:python@t3.learn.python.ru:1080/"
    ]
    proxy = proxy_list[random.randint(0, 2)]
    return proxy


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
    proxy = {"http": get_random_proxy()}
    try:
        result = requests.get(url, headers=headers, proxies=proxy)
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
