from webapp.trip.utils.get_ticket_prices import get_user_ticket
from webapp.trip.utils.get_recommended_hotels import get_best_hotels
from webapp.trip.utils.get_attractions import get_attractions_list


def get_city_information(city_outbound, city_inbound, outbound_date, inbound_date, user_money):
    result = {}

    tickets = get_user_ticket(city_outbound, city_inbound, outbound_date, inbound_date, adults_number=2)
    cheapest_ticket = min(tickets["recommended"], key=lambda x: x["price"])
    if cheapest_ticket["forward"]["arrival_date"]:
        checkin = cheapest_ticket["forward"]["arrival_date"]
    else:
        checkin = outbound_date.strftime("%d/%m/%Y")
    checkout = inbound_date.strftime("%d/%m/%Y")
    money_amount = user_money - cheapest_ticket["price"]
    attractions = get_attractions_list(city_inbound)
    hotels = get_best_hotels(city_inbound, checkin, checkout, money_amount)

    result.update({"tickets": tickets})
    result.update({"hotels": hotels})
    result.update({"attractions": attractions})

    return result
