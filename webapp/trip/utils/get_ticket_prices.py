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


def get_user_ticket(city_outbound, city_inbound, outbound_date, inbound_date, adults_number=1):

    url = URL.format(
        id_outbound=get_id(city_outbound),
        city_out=city_outbound,
        id_inbound=get_id(city_inbound),
        city_in=city_inbound,
        outbound_date=outbound_date.strftime("%Y-%m-%d"),  # YYYY-mm-dd
        inbound_date=inbound_date.strftime("%Y-%m-%d"),  # YYYY-mm-dd
        adults_number=adults_number
    )

    parsing_date = datetime.now().strftime("%Y-%m-%d %H")

    city_outbound_id = AirportId.query.filter_by(city=city_outbound.lower()).first().id
    city_inbound_id = City.query.filter_by(ru_name=city_inbound.lower()).first().id

    ticket_exist = db.session.query(
                    db.exists().where(Ticket.city_outbound_id == city_outbound_id)
                               .where(Ticket.city_inbound_id == city_inbound_id)
                               .where(Ticket.outbound_date == outbound_date.strftime("%Y-%m-%d"))
                               .where(Ticket.inbound_date == inbound_date.strftime("%Y-%m-%d"))
                               .where(Ticket.parsing_date == parsing_date)).scalar()

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
        ticket = Ticket.query.filter(Ticket.city_outbound_id == city_outbound_id) \
                             .filter(Ticket.city_inbound_id == city_inbound_id) \
                             .filter(Ticket.outbound_date == outbound_date.strftime("%Y-%m-%d")) \
                             .filter(Ticket.inbound_date == inbound_date.strftime("%Y-%m-%d")) \
                             .filter(Ticket.parsing_date == parsing_date).first()
        if not ticket.price:
            print(f"No ticket outbound-{city_outbound}/inbound-{city_inbound}")
            return False
        else:
            return ticket.price
