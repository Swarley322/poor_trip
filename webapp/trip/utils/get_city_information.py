from webapp.trip.utils.get_ticket_prices import get_user_ticket
from webapp.trip.utils.get_attractions import get_attractions_list
from webapp.trip.utils.get_living_prices import get_living_prices


def get_city_information(city_outbound, city_inbound, outbound_date, inbound_date, user_money):
    result = {}
    tickets = get_user_ticket(city_outbound, city_inbound, outbound_date, inbound_date, adults_number=2)
    attractions = get_attractions_list(city_inbound)
    living_prices = get_living_prices(city_inbound)
    result.update({"tickets": tickets})
    result.update({"attractions": attractions})
    result.update({"living_prices": living_prices})
    return result
