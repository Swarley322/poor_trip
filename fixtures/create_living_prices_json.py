# -*- coding: utf-8 -*- 
import time
import json
import csv
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
from pytz import timezone

from webapp import create_app
from webapp.db import db
from webapp.parser.utils import get_html, get_random_sleep_time
app = create_app()
db.init_app(app)

def get_live_prices(html):
    soup = BS(html, "html.parser")
    info = soup.find("table", class_="data_wide_table").find_all('tr')
    result = {}
    for price in info:
        # a.append(price)
        try:
            name = price.find("td").text.strip()
            value = price.find("td", class_="priceValue").text.strip()
            result.update({name: float(value.replace(",", "").replace("\xa0руб", ""))})
        except AttributeError:
            try:
                name = price.find("td", class_="tr_highlighted").text.strip()
                value = price.find("td", class_="priceValue tr_highlighted").text.strip()
                result.update({name: float(value.replace(",", "").replace("\xa0руб", ""))})
            except AttributeError:
                continue

    # print(result)
    return result


def safe_city_prices(city):
    """city - eng city name (Moscow)"""
    url = "https://www.numbeo.com/cost-of-living/in/{city}?displayCurrency=RUB".format(city=city)
    html = get_html(url)
    if not html:
        print("HTML for {city} live_prices doesn't returned".format(city=city))
        time.sleep(get_random_sleep_time())
        html = get_html(url)
        if not html:
            return False
    try:
        prices = get_live_prices(html)
    except Exception as e:
        print(e)
        print("Wrong HTML for live prices {city} trying again".format(city=city))
        try:
            time.sleep(get_random_sleep_time())
            html = get_html(url)
            prices = get_live_prices(html)
        except Exception as e:
            print(e)
            print("Wrong HTML for live prices {city} second time".format(city=city))
            return False
    return prices


def create():
    cities = []
    with open('fixtures/cities_list.csv', 'r', encoding='utf-8', newline='') as f:
        fields = ['eng_name', 'eng_country', 'eng_part_of_the_world', 'ru_name', 'ru_country', "ru_part_of_the_world"]
        rows = csv.DictReader(f, fields, delimiter=';')
        for row in rows:
            cities.append(row["eng_name"])

    for city in cities:
        price = safe_city_prices(city.title())
        if not price:
            time.sleep(get_random_sleep_time())
            price = safe_city_prices(city.title())
        with open(f'fixtures/living_prices/{city.lower()}.json', 'w') as f:
            json.dump(price, f)
        print("Prices for {city} parsed and inserted".format(city=city))
        time.sleep(get_random_sleep_time())

if __name__ == "__main__":
    with app.app_context():
        create()