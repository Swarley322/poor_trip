from webapp.trip.tickets import get_data, get_html


def get_tickets_prices(city_in, city_out, outbounddate, inbounddate, adults_number="2"):
    html = get_html(city_in, city_out, outbounddate, inbounddate, adults_number)
    tickets_list = get_data(html)

    return tickets_list
