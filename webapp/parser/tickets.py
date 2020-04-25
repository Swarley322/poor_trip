import locale
import platform
import re

from datetime import datetime, timedelta
from bs4 import BeautifulSoup as BS

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def get_valid_arrival_date(date):
    current_date = datetime.now()
    current_year = datetime.now().strftime("%Y")
    next_year = (datetime.now() + timedelta(days=365)).strftime("%Y")

    date = date.replace("янв", "января") \
               .replace("фев", "февраля") \
               .replace("апр", "апреля") \
               .replace("мар", "марта") \
               .replace("июн", "июня") \
               .replace("июл", "июля") \
               .replace("авг", "августа") \
               .replace("сен", "сентября") \
               .replace("окт", "октября") \
               .replace("ноя", "ноября") \
               .replace("дек", "декабря")
    current_year_date = " ".join([date, current_year])

    if datetime.strptime(current_year_date, '%d %B %Y') > current_date:
        return datetime.strptime(current_year_date, '%d %B %Y')
    else:
        next_year_date = " ".join([date, next_year])
        return datetime.strptime(next_year_date, '%d %B %Y')


def get_ticket_information(soup):
    price = soup.find("div", class_="original-price_kb__main-price").text.replace("\xa0", "").replace("Р", "")
    if "€" in price:
        price = int(price.replace("€", "")) * 85

    buy_url = "https://avia.yandex.ru" + soup.find("a", class_="y-button _centralize _active _theme_buy _size_m _init")['href']

    try:
        luggage = soup.find("span", class_="type-of-ticket_kb__baggage-info").find("span", class_="type-of-ticket_kb__type").text
    except AttributeError:
        luggage = soup.find("span", class_="type-of-ticket_kb__baggage-tariff").find("span", class_="type-of-ticket_kb__type").text

    def get_data(tag):
        try:
            company = tag.find("td", class_="flight_list__companies").text
        except AttributeError:
            company = False
        try:
            logo_url = tag.find("div", class_="flight_list__company-logo")["style"].replace("background-image: url(", "").replace(")", "")
        except (AttributeError, TypeError):
            logo_url = False

        departure_time = tag.find("td", class_="flight_list__departure-time").text
        flight_duration = tag.find("td", "flight_list__flight-duration").text.replace("\xa0", "")
        arrival_time = tag.find("td", class_="flight_list__arrival-time").text[:5]

        try:
            arrival_date = tag.find("div", class_="flight_list__arrival-date").text.strip()
            arrival_date = get_valid_arrival_date(arrival_date).strftime("%d/%m/%Y")
        except AttributeError:
            arrival_date = False

        airports = tag.find("div", class_="flight_list__airports").text

        try:
            direct_flight = tag.find("div", class_="flight_list__direct-flight").text
            transfer_city = False
            transfer_duration = False
        except AttributeError:
            direct_flight = False
            transfer_city = tag.find("div", class_="flight_list__transfer").find("span", class_=re.compile("flight_list.*")).text
            transfer_duration = tag.find("span", class_="flight_list__transfer-duration").text

        return {
            "company": company,
            "logo_url": logo_url,
            "departure_time": departure_time,
            "flight_duration": flight_duration,
            "arrival_time": arrival_time,
            "arrival_date": arrival_date,
            "airports": airports,
            "direct_flight": direct_flight,
            "transfer_city": transfer_city,
            "transfer_duration": transfer_duration
        }

    forward = soup.find("tr", class_="flight_list__forward")
    backward = soup.find("tr", class_="flight_list__backward")
    return {
        "price": int(price),
        "buy_url": buy_url,
        "luggage": luggage,
        "forward": get_data(forward),
        "backward": get_data(backward)
    }


def get_tickets_data(html):
    
    soup = BS(html, 'html.parser')
    result = {"recommended": [], "common": []}
    tickets = soup.find("div", class_="serp-layout_kb__content")

    try:
        recommended_tickets = tickets.find("div", class_="tabs-container_kb _init").find("table", class_="cards_kb__table").find_all("tbody", class_="flight_list _init")
    except AttributeError:
        print("No recommended tickets")
        return False

    for ticket in recommended_tickets:
        result["recommended"].append(get_ticket_information(ticket))

    try:
        common_tickets = tickets.find("div", class_="flights-list_kb__table").find("table", class_="flights-list_kb__inner-table").find_all("tbody", class_="flight_list _init")
    except AttributeError:
        print("No common tickets")
        return result
    for ticket in common_tickets:
        result["common"].append(get_ticket_information(ticket))

    return result
