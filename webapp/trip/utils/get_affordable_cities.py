from datetime import datetime, timedelta
from pytz import timezone
from webapp.trip.models import AvgPriceReviews, City
from webapp.trip.utils.get_ticket_prices import get_user_ticket


def get_affordable_cities(city_outbound, outbound_date, inbound_date, user_money):
    """Function 
    """
    # parsing_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=2)).strftime("%d/%m/%Y")
    # parsing_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=1)).strftime("%d/%m/%Y")
    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")

    # result = {
    #     "europe": {
    #         "england": [],
    #         "russia": [],
    #         "germany": [],
    #         "spain": [],
    #         "france": []
    #         },
    #     "asia": {
    #         "japan": [],
    #         "south korea": [],
    #         "china": [],
    #         "singapore": []
    #         },
    #     "america": {
    #         "usa": [],
    #         "canada": []
    #         }
    # }
    result = {}
    ticket_count = 0
    hotel_count = 0
    city_list = [city for city in City.query.all()]

    for city in city_list:
        if city.ru_name == city_outbound.lower():
            continue

        tickets = get_user_ticket(city_outbound, city.ru_name, outbound_date, inbound_date, adults_number=2)

        if tickets:
            cheapest_ticket = min(tickets["recommended"], key=lambda x: x["price"])
            if cheapest_ticket["forward"]["arrival_date"]:
                checkin = cheapest_ticket["forward"]["arrival_date"]
            else:
                checkin = outbound_date.strftime("%d/%m/%Y")

            checkout = inbound_date.strftime("%d/%m/%Y")
            days_staying = int(abs((datetime.strptime(checkin, "%d/%m/%Y") - datetime.strptime(checkout, "%d/%m/%Y")).days))
            week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))

            money_without_tickets = user_money - cheapest_ticket["price"]

            try:
                avg_day_living_price = AvgPriceReviews.query.filter_by(week_number=week_number) \
                                                            .filter_by(parsing_date=parsing_date) \
                                                            .filter_by(city_id=city.id).first().avg_day_price
            except Exception as e:
                print(e)
                print(f"No avg_day_price for {city.ru_name}, for week={week_number}")
                continue

            if money_without_tickets - avg_day_living_price * days_staying > 0:
                city_info = {
                    "city_outbound": city_outbound,
                    "city_inbound": city.ru_name,
                    "outbound_date": outbound_date,
                    "inbound_date": inbound_date,
                    "checkin": checkin,
                    "checkout": checkout,
                    "money_without_tickets": money_without_tickets
                }
                try:
                    result[city.eng_country.title()].append(city_info)
                except (KeyError, AttributeError):
                    result.update({city.eng_country.title(): []})
                    result[city.eng_country.title()].append(city_info)

                hotel_count += 1
            else:
                continue
            ticket_count += 1

    if ticket_count == 0:
        return "No tickets"
    elif hotel_count == 0:
        return "Not enough money"
    else:
        return result
