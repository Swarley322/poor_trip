import random
from datetime import datetime

from webapp.trip.models import City
from webapp.trip.utils.get_ticket_prices import get_user_ticket
from webapp.trip.utils.get_recommended_hotels import get_best_hotels


def get_random_city(city_outbound, outbound_date, inbound_date, user_money):
    city_list = [city.ru_name for city in City.query.all()]
    random.shuffle(city_list)
    ticket_count = 0
    for city in city_list:
        if city == city_outbound.lower():
            continue

        tickets = get_user_ticket(city_outbound, city, outbound_date, inbound_date, adults_number=2)

        if tickets:
            ticket_count += 1
            cheapest_ticket = min(tickets["recommended"], key=lambda x: x["price"])
            if cheapest_ticket["forward"]["arrival_date"]:
                checkin = cheapest_ticket["forward"]["arrival_date"]
                checkin = datetime.strptime(checkin, "%d-%m-%Y").strftime("%d/%m/%Y")
            else:
                checkin = outbound_date.strftime("%d/%m/%Y")

            checkout = inbound_date.strftime("%d/%m/%Y")

            money_amount = user_money - cheapest_ticket["price"]
            if money_amount <= 0:
                continue
            try:
                hotels = get_best_hotels(city, checkin, checkout, money_amount)
                if hotels:
                    return city
                else:
                    continue
            except Exception as e:
                print(e)
                continue
        else:
            continue
    if ticket_count == 0 :
        return "No tickets"
    else:
        return "Not enough money"
