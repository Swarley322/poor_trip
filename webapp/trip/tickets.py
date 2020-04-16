import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from webapp.trip.models import AirportId, City


# Parameters
inbounddate = "2020-05-10"  # Дата возвращения
inbounddate_sk = inbounddate[2:].replace("-", "")
# cabinclass = "economy"  # класс
# number_of_children = "0"  # Кол-ва детей
# infants = "0"  # Карапузы (до 12 месяцев)
country = "RU"  # Страна в которой находится пользователь
currency = "RUB"  # Валюта (результат в данной валюте)
locale = "ru-RU"  # Региональные настройки
outbounddate = "2020-05-05"  # Дата вылета
adults_number = "1"  # Количество взрослых пассажиров


# Getting places IDs
def get_ids(city_out, city_in):
    city_out_id = AirportId.query.filter(AirportId.city == city_out.title()).first()
    city_in_id = AirportId.query.filter(AirportId.city == city_in.title()).first()
    return {"city_out": city_out_id.airport_id, "city_in": city_in_id.airport_id}


# def get_IDs(city_in, city_out):
#     url = "https://avia.yandex.ru/city/mow/-moskva/"
#     # chromedriver = "/Users/dmitrykim/projects/booking/chromedriver"
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     browser = webdriver.Chrome(executable_path="/Users/dmitrykim/projects/booking/chromedriver", chrome_options=options)
#     browser.get(url)
#     # Filling origin place name
#     city_origin = browser.find_element_by_name("fromName")
#     city_origin.send_keys(Keys.BACK_SPACE*20)
#     city_origin.send_keys(city_out)
#     time.sleep(1)
#     city_origin.send_keys(Keys.ENTER)
#     # Filling destination place name
#     city_destination = browser.find_element_by_name("toName")
#     city_destination.send_keys(Keys.BACK_SPACE*20)
#     city_destination.send_keys(city_in)
#     time.sleep(1)
#     city_destination.send_keys(Keys.ENTER)
#     time.sleep(1)

#     new_url = browser.current_url

#     # Getting ID of origin city
#     start_origin = new_url.find("fromId=") + len("fromId=")
#     end_origin = new_url.find("&toId")
#     fromID = new_url[start_origin:end_origin]
#     # print(fromID)

#     # Getting ID of destination city
#     start_destination = new_url.find("toId=") + len("toId=")
#     end_destination = new_url.find("&when")
#     toID = new_url[start_destination:end_destination]
#     browser.quit()
#     return(fromID, toID)


def get_html(city_in, city_out, outbounddate, inbounddate, adults_number):
    ids = get_ids(city_out, city_in)
    url = ("https://avia.yandex.ru/search/result/?fromId="
           + ids['city_in'] + "&fromName=" + city_out + "&toId="
           + ids['city_out'] + "&toName=" + city_in + "&when="
           + outbounddate + "&return_date="
           + inbounddate + "&oneway=2&adult_seats=" + adults_number
           + "&children_seats0&infant_seats=0&klass=economy&fromBlock=FormSearch#tt=1,0,0,0,0,0")

    chromedriver = "/Users/dmitrykim/projects/booking/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
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
    tickets = [{}]
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
                    "forward_departue_time": depatrue_time_forward.text,
                    "forward_arrival_time": arrival_time_visual(arrival_time_forward.text),
                    "forward_flight_daration": flight_daruation_visual(flight_daruation_forward.text),
                    "forward_airport_origin_and_destination": airports_forward.text,
                    "buy_link": buy_link
                })
            backward_tickets = tickets_data.find_all("tr", class_="flight_list__backward")
            for backward_data in backward_tickets:
                depatrue_time_backward = backward_data.find("td", class_="flight_list__departure-time")
                arrival_time_backward = backward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_backward = backward_data.find("td", class_="flight_list__flight-duration")
                airports_backward = backward_data.find("div", class_="flight_list__airports")
                tickets[-1].update({
                    "backward_departue_time": depatrue_time_backward.text,
                    "backward_arrival_time": arrival_time_visual(arrival_time_backward.text),
                    "backward_flight_duration": flight_daruation_visual(flight_daruation_backward.text),
                    "backward_aiport_origin_and_destination": airports_backward.text
                })
    except(AttributeError):
        return False

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
                    "forward_departue_time": depatrue_time_forward.text,
                    "forward_arrival_time": arrival_time_visual(arrival_time_forward.text),
                    "forward_flight_daration": flight_daruation_visual(flight_daruation_forward.text),
                    "forward_airport_origin_and_destination": airports_forward.text,
                    "buy_link": buy_link
                })
            backward_tickets = tickets_data.find_all("tr", class_="flight_list__backward")
            for backward_data in backward_tickets:
                depatrue_time_backward = backward_data.find("td", class_="flight_list__departure-time")
                arrival_time_backward = backward_data.find("td", class_="flight_list__arrival-time")
                flight_daruation_backward = backward_data.find("td", class_="flight_list__flight-duration")
                airports_backward = backward_data.find("div", class_="flight_list__airports")
                tickets[-1].update({
                    "backward_departue_time": depatrue_time_backward.text,
                    "backward_arrival_time": arrival_time_visual(arrival_time_backward.text),
                    "backward_flight_duration": flight_daruation_visual(flight_daruation_backward.text),
                    "backward_aiport_origin_and_destination": airports_backward.text
                })
    except(AttributeError):
        print("No common tickets for this dates")
    del tickets[0]
    return tickets
