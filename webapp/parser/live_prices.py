from bs4 import BeautifulSoup as BS

from webapp.db import db
from webapp.trip.models import City
from webapp.parser.utils import get_html


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
    url = f"https://www.numbeo.com/cost-of-living/in/{city}?displayCurrency=RUB"
    html = get_html(url)
    prices = get_live_prices(html)
    update = City.query.filter_by(eng_name=city).first()
    update.inexpensive_meal_price = int(prices['Meal, Inexpensive Restaurant'])
    update.restaurant_2_persons = int(prices['Meal for 2 People, Mid-range Restaurant, Three-course'])
    update.water_033 = int(prices['Water (0.33 liter bottle)'])
    update.one_way_ticket = int(prices['One-way Ticket (Local Transport)'])
    update.internet = int(prices['Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)'])
    db.session.commit()
