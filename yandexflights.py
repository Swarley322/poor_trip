import selenium
import html5lib
import requests
import time
import re
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# Parameters
inbounddate = "2020-05-10"  # Дата возвращения
inbounddate_sk = inbounddate[2:].replace("-", "")
cabinclass = "economy"  # класс
number_of_children = "0"  # Кол-ва детей
infants = "0"  # Карапузы (до 12 месяцев)
country = "RU"  # Страна в которой находится пользователь
currency = "RUB"  # Валюта (результат в данной валюте)
locale = "ru-RU"  # Региональные настройки
outbounddate = "2020-05-05"  # Дата вылета
adults_number = "1"  # Количество взрослых пассажиров


# Getting places IDs
def get_IDs():
    connection = sqlite3.connect("cities_ids.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM citiesids")
    ans = crsr.fetchall()  # making list of lists
    for city_name, city_id in ans:
        if city_name == city_out:
            fromID = city_id
        if city_name == city_in:
            toID = city_id
    return(fromID, toID)


def get_html():
    Ids = get_IDs()
    url = "https://avia.yandex.ru/search/result/?fromId="+Ids[0]+"&fromName="+city_out+"&toId="+Ids[1]+"&toName="+city_in+"&when="+outbounddate+"&return_date="+inbounddate+"&oneway=2&adult_seats="+adults_number+"&children_seats"+number_of_children+"&infant_seats="+infants+"&klass="+cabinclass+"&fromBlock=FormSearch#tt=1,0,0,0,0,0"
    chromedriver = "C:/Users/Ikaro/Desktop/projects/yandexflights/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    browser.quit()
    return html


def price_visual(price):
    price_visual = price.replace("\xa0", "").replace("\xa0Р", "")
    return price_visual


def flight_daruation_visual(flight_daruation):
    flight_daruation_forward_visual = flight_daruation.replace("\xa0", "")
    return flight_daruation_forward_visual


def arrival_time_visual(arrival_time):
    arrival_time_visual = arrival_time[0:5]+" "+arrival_time[5:]
    return arrival_time_visual


# Getting tickets prices
def get_data(html):
    tickets = []
    soup = BeautifulSoup(html, 'html.parser')
    # Recommended tickets data
    try:
        tickets_recommended = soup.find("table", class_="cards_kb__table").find_all("tbody", class_="flight_list _init")
        for tickets_data in tickets_recommended:
            forward_tickets = tickets_data.find_all("tr", class_="flight_list__forward")
            for forward_data in forward_tickets:
                company_name = forward_data.find("span", class_="flight_list__company-names")
                price = forward_data.find("span", class_="price_kb _init")
                # price_text = price.text
                # price_normal = price_visual(price_text)
                depatrue_time_forward = forward_data.find("td", class_="flight_list__departure-time")
                arrival_time_forward = forward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_forward = forward_data.find("td", class_="flight_list__flight-duration")
                airports_forward = forward_data.find("div", class_="flight_list__airports")
                buy_link = 'https://avia.yandex.ru' + forward_data.find("a", class_="y-button _centralize _active _theme_buy _size_m _init")["href"]
                tickets.append({
                    "company": company_name.text,
                    "price": price_visual(price.text),
                    "forward departue time": depatrue_time_forward.text,
                    "forward arrival time": arrival_time_visual(arrival_time_forward.text),
                    "forward flight daration": flight_daruation_visual(flight_daruation_forward.text),
                    "forward airport origin and destination": airports_forward.text,
                    "buy link": buy_link
                })
            backward_tickets = tickets_data.find_all("tr", class_="flight_list__backward")
            for backward_data in backward_tickets:
                depatrue_time_backward = backward_data.find("td", class_="flight_list__departure-time")
                arrival_time_backward = backward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_backward = backward_data.find("td", class_="flight_list__flight-duration")
                airports_backward = backward_data.find("div", class_="flight_list__airports")
                tickets.append({
                    "backward departue time": depatrue_time_backward.text,
                    "backward arrival time": arrival_time_visual(arrival_time_backward.text),
                    "backward flight duration": flight_daruation_visual(flight_daruation_backward.text),
                    "backward aiport origin and destination": airports_backward.text
                })
    except(AttributeError):
        print("No recommended tickets for this dates")

    # Common tickets data
    try:
        tickets_not_recommended = soup.find("table", class_="flights-list_kb__inner-table").find_all("tbody", class_="flight_list _init")
        for tickets_data in tickets_not_recommended:
            forward_tickets = tickets_data.find_all("tr", class_="flight_list__forward")
            for forward_data in forward_tickets:
                company_name = forward_data.find("span", class_="flight_list__company-names")
                price = forward_data.find("span", class_="price_kb _init")
                depatrue_time_forward = forward_data.find("td", class_="flight_list__departure-time")
                arrival_time_forward = forward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_forward = forward_data.find("td", class_="flight_list__flight-duration")
                airports_forward = forward_data.find("div", class_="flight_list__airports")
                buy_link = 'https://avia.yandex.ru' + forward_data.find("a", class_="y-button _centralize _active _theme_buy _size_m _init")["href"]
                tickets.append({
                    "company": company_name.text,
                    "price": price_visual(price.text),
                    "forward departue time": depatrue_time_forward.text,
                    "forward arrival time": arrival_time_visual(arrival_time_forward.text),
                    "forward flight daration": flight_daruation_visual(flight_daruation_forward.text),
                    "forward airport origin and destination": airports_forward.text,
                    "buy link": buy_link
                })
            backward_tickets = tickets_data.find_all("tr", class_="flight_list__backward")
            for backward_data in backward_tickets:
                depatrue_time_backward = backward_data.find("td", class_="flight_list__departure-time")
                arrival_time_backward = backward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_backward = backward_data.find("td", class_="flight_list__flight-duration")
                airports_backward = backward_data.find("div", class_="flight_list__airports")
                tickets.append({
                    "backward departue time": depatrue_time_backward.text,
                    "backward arrival time": arrival_time_visual(arrival_time_backward.text),
                    "backward flight duration": flight_daruation_visual(flight_daruation_backward.text),
                    "backward aiport origin and destination": airports_backward.text
                })
    except(AttributeError):
        print("No common tickets for this dates")
    return tickets


print("Direct flights only")
city_out = input("Enter origin city name: ")
city_in = input("Enter destination city name: ")
print(get_data(get_html()))
