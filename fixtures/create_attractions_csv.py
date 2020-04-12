import re
import time
import csv

from bs4 import BeautifulSoup as BS

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


def get_valid_city(city):
    url = f"https://www.translate.ru/grammar/ru-en/{city}"
    html = get_html(url)
    soup = BS(html, "html.parser")
    result = soup.find("table", class_="wordforms").find_all("tr")[2].find("span").text.strip()
    return result


def get_pages(html):
    soup = BS(html, "html.parser")
    pages = soup.find("ul", class_="paginator-tt js-paginator-tt").find_all("li", class_=re.compile("js-NavP.*"))[-1].find("a").text
    return int(pages)


def get_next_page(html):
    soup = BS(html, "html.parser")
    url = soup.find("li", class_="paginator-tt__next js-NavNext").find("a")["href"]
    return "https://tonkosti.ru" + url


def get_attractions(html):
    soup = BS(html, "html.parser")
    attractions = soup.find("ul", class_="places-list").find_all("li", class_=re.compile("places-list__item.*"))
    result = []
    for attraction in attractions:
        name = attraction.find("h3", class_="places-list__item-header").find("a", rel="nofollow").text.strip()
        href = "https://tonkosti.ru" + attraction.find("a", class_="places-list__item-img places-list__item-img--rc")["href"]
        img_url = attraction.find("a", class_="places-list__item-img places-list__item-img--rc").find("img")["src"]
        try:
            address = attraction.find("div", class_="places-list__address places-list__address--rc").text.strip()
        except AttributeError:
            address = None
        description = attraction.find("div", class_="places-list__text")
        description_text = " ".join([description.text.strip(), description.find("a", rel="nofollow").text.strip()])
        result.append({
            "name": name,
            "address": address,
            "description": description_text,
            "img_url": img_url,
            "link": href
            })
    return result


def get_all_attractions(city):
    valid_city = get_valid_city(city)
    url = f"https://tonkosti.ru/Достопримечательности_{valid_city.title()}"
    # url = f"https://tonkosti.ru/Достопримечательности_{city}"
    html = get_html(url)
    try:
        pages = get_pages(html)
    except AttributeError:
        pages = 1
    result = []
    for page in range(1, pages + 1):
        try:
            attractions = get_attractions(html)
            for attraction in attractions:
                attraction.update({"city": city})
            result.append(attractions)
        except Exception as e:
            print(e)
            print(f"error {page}/{pages - 1}")
            if page != pages:
                html = get_html(get_next_page(html))
            time.sleep(5)
            continue
        if page != pages:
            html = get_html(get_next_page(html))
        time.sleep(5)
        print(f"Page {page}/{pages} parsed")
    return result


if __name__ == "__main__":
    # cities = ["Лас-Вегаса"]
    cities = []
    with open('fixtures/cities_list.csv', 'r', encoding='utf-8', newline='') as f:
        fields = ['eng_name', 'eng_country', 'eng_part_of_the_world', 'ru_name', 'ru_country', "ru_part_of_the_world"]
        rows = csv.DictReader(f, fields, delimiter=';')
        for row in rows:
            cities.append(row["ru_name"])

    with open("fixtures/attractions.csv", "a+", encoding="utf-8", newline="") as f:
        fields = ['city', 'name', 'address', 'description', 'img_url', "link"]
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
        for city in cities:
            attractions_list = get_all_attractions(city)
            for attractions in attractions_list:
                for attraction in attractions:
                    writer.writerow(attraction)
            print(f"{city} parsed")
