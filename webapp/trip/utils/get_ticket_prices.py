from datetime import datetime

from webapp.db import db
from webapp.parser.utils import get_html_selenium
from webapp.parser.tickets import get_tickets_data
from webapp.trip.models import AirportId, City, Ticket

URL = ("https://avia.yandex.ru/search/result/?fromId={id_outbound}"
       "&fromName={city_out}&toId={id_inbound}&toName={city_in}&wh"
       "en={outbound_date}&return_date={inbound_date}&oneway=2&adu"
       "lt_seats={adults_number}&children_seats=0&infant_seats=0&k"
       "lass=economy&fromBlock=FormSearch#tt=0,0,1,0,0,0")


def get_id(city):
    return AirportId.query.filter(AirportId.city == city.lower()).first().airport_id


def checking_parsing_date(request_date):
    """"request_date - string object in format %d/%m/%Y %H:%M
    returning True if delta between request_date and current_time lower than 1 hour"""

    current_time = datetime.now()
    delta = current_time - datetime.strptime(request_date, "%Y-%m-%d %H:%M")
    if delta.days == 0 and (delta.seconds//60) % 60 <= 61 and delta.seconds//3600 <= 1:
        return True
    else:
        return False


def get_user_ticket(city_outbound, city_inbound, outbound_date, inbound_date, adults_number=1):
    """
    """

    url = URL.format(
        id_outbound=get_id(city_outbound),
        city_out=city_outbound,
        id_inbound=get_id(city_inbound),
        city_in=city_inbound,
        outbound_date=outbound_date.strftime("%Y-%m-%d"),  # YYYY-mm-dd
        inbound_date=inbound_date.strftime("%Y-%m-%d"),  # YYYY-mm-dd
        adults_number=adults_number
    )

    parsing_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    city_outbound_id = AirportId.query.filter_by(city=city_outbound.lower()).first().id
    city_inbound_id = City.query.filter_by(ru_name=city_inbound.lower()).first().id
    tickets_list = Ticket.query.filter_by(city_outbound_id=city_outbound_id) \
                               .filter_by(city_inbound_id=city_inbound_id) \
                               .filter_by(outbound_date=outbound_date.strftime("%Y-%m-%d")) \
                               .filter_by(inbound_date=inbound_date.strftime("%Y-%m-%d")).all()

    ticket_exist = [ticket for ticket in tickets_list if checking_parsing_date(ticket.parsing_date)]

    if not ticket_exist:
        print(f"parsing tickets for {city_inbound}, {outbound_date}///{inbound_date}")
        html = get_html_selenium(url)
        tickets = get_tickets_data(html)
        if tickets:
            ticket = Ticket(
                city_outbound_id=city_outbound_id,
                city_inbound_id=city_inbound_id,
                outbound_date=outbound_date.strftime("%Y-%m-%d"),
                inbound_date=inbound_date.strftime("%Y-%m-%d"),
                parsing_date=parsing_date,
                price=tickets
            )
            db.session.add(ticket)
            db.session.commit()
            return tickets
        else:
            ticket = Ticket(
                city_outbound_id=city_outbound_id,
                city_inbound_id=city_inbound_id,
                outbound_date=outbound_date.strftime("%Y-%m-%d"),
                inbound_date=inbound_date.strftime("%Y-%m-%d"),
                parsing_date=parsing_date,
                price=None
            )
            db.session.add(ticket)
            db.session.commit()
            print(f"No ticket outbound-{city_outbound}/inbound-{city_inbound}")
            return False
    else:
        ticket = ticket_exist[0]
        print(ticket)
        if not ticket.price:
            print(f"No ticket outbound-{city_outbound}/inbound-{city_inbound}")
            return False
        else:
            return ticket.price


def find_ticket(
        city_outbound, city_inbound, outbound_date, inbound_date,
        forward_flight_duration, backward_flight_duration, price
):
    city_outbound_id = AirportId.query.filter_by(city=city_outbound.lower()).first().id
    city_inbound_id = City.query.filter_by(ru_name=city_inbound.lower()).first().id
    tickets = Ticket.query.filter_by(city_outbound_id=city_outbound_id) \
                          .filter_by(city_inbound_id=city_inbound_id) \
                          .filter_by(outbound_date=datetime.strptime(outbound_date, "%d-%m-%Y").strftime("%Y-%m-%d")) \
                          .filter_by(inbound_date=datetime.strptime(inbound_date, "%d-%m-%Y").strftime("%Y-%m-%d")).all()
    for ticket_list in tickets:
        valid_parsing_date = checking_parsing_date(ticket_list.parsing_date)
        if valid_parsing_date:
            for ticket in ticket_list.price:
                result = [ticket for _, tickets in ticket_list.price.items() for ticket in tickets if ticket['price'] == price and ticket['forward']['flight_duration'] == forward_flight_duration and ticket['backward']['flight_duration'] == backward_flight_duration]
                if result:
                    return result[0]
    return False
