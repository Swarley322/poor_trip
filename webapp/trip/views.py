import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, flash, render_template, redirect, session, url_for
from flask_login import current_user, login_required

from webapp.trip.forms import StartForm
from webapp.trip.models import AirportId
from webapp.trip.utils.get_affordable_cities import get_affordable_cities
from webapp.trip.utils.get_city_information import get_city_information
from webapp.trip.utils.get_random_city import get_random_city
from webapp.trip.utils.get_recommended_hotels import get_best_hotels
from webapp.trip.utils.get_redirect_url import get_redirect_target
from webapp.trip.utils.get_ticket_prices import find_ticket

blueprint = Blueprint("trip", __name__)


def checking_request_time(request_date):
    """"request_date - string object in format %d/%m/%Y %H:%M
    returning True if delta between request_date and current_time lower than 1 hour"""

    current_time = datetime.now()
    delta = current_time - datetime.strptime(request_date, "%d/%m/%Y %H:%M")
    if delta.days == 0 and delta.seconds//3600 == 0:
        return True
    else:
        return False


def check_outbound_date(outbound_date):
    """outbound_date - date object"""
    if outbound_date <= date.today() or outbound_date < date(2020, 7, 1):
        return False
    else:
        if date.today() < date(2020, 7, 1):
            three_months = date(2020, 7, 1) + relativedelta(months=+3)
            if outbound_date > three_months:
                return False
        else:
            three_months = date.today() + relativedelta(months=+3)
            if outbound_date > three_months:
                return False
        return True


@blueprint.route('/')
def start():
    form = StartForm()
    title = "Welcome"
    return render_template('trip/start.html', form=form, page_title=title,)


@blueprint.route('/city', methods=["GET"])
@login_required
def city():
    title = "Доступные страны"
    try:
        valid_request = checking_request_time(session["login_request_date"])
        if valid_request:
            city_outbound = session['city_outbound']
            outbound_date = session['outbound_date']
            inbound_date = session['inbound_date']
            user_money = session['user_money']

            city_list = get_affordable_cities(
                            city_outbound,
                            outbound_date,
                            inbound_date,
                            user_money
            )

            if city_list == "No tickets":
                flash("Нет билетов на выбранные даты")
                return redirect(url_for('trip.start'))
            elif city_list == "Not enough money":
                flash("Ты слишком беден, иди работай")
                return redirect(url_for('trip.start'))
            else:
                return render_template("trip/cards.html", city_list=city_list, page_title=title)

        else:
            flash("Заполните форму еще раз, информация могла устареть")
            return redirect(url_for('trip.start'))
    except KeyError:
        flash("Заполните форму")
        return redirect(url_for('trip.start'))


@blueprint.route('/process-data', methods=["POST"])
def process_data():
    form = StartForm()
    time.sleep(0.3)
    if form.validate_on_submit():
        city_outbound = form.city_outbound.data
        user_money = form.money.data
        outbound_date = form.outbound_date.data
        inbound_date = form.inbound_date.data

        airports = AirportId.query.filter(AirportId.city == city_outbound.lower().strip()).count()
        # check valid airport
        if airports:
            session['city_outbound'] = city_outbound.lower()
        else:
            flash("Неверно указан город отправления, попробуйте заново")
            return redirect(url_for('trip.start'))

        valid_date = check_outbound_date(outbound_date)
        if outbound_date > inbound_date or outbound_date == inbound_date or not valid_date:
            flash("Самая ранняя дата вылета 1 июля 2020 года, и не более 3 месяцев вперед")
            return redirect(url_for('trip.start'))
        else:
            session["outbound_date"] = datetime.combine(outbound_date, datetime.min.time())
            session["inbound_date"] = datetime.combine(inbound_date, datetime.min.time())

        if user_money <= 0:
            flash("Некорректная сумма")
            return redirect(url_for('trip.start'))
        else:
            session['user_money'] = user_money

        session["request_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        if current_user.is_authenticated:
            session["login_request_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        if current_user.is_anonymous:
            random_city = get_random_city(city_outbound, outbound_date, inbound_date, user_money)
            if random_city == "No tickets":
                flash("Нет билетов на выбранные даты")
                return redirect(url_for('trip.start'))
            elif random_city == "Not enough money":
                flash("Ты слишком беден, иди работай")
                return redirect(url_for('trip.start'))
            else:
                return redirect(url_for('trip.index', city_inbound=random_city))
        else:
            return redirect(url_for('trip.city'))

    flash("Введены неверные данные")
    return redirect(url_for('trip.start'))


@blueprint.route('/index/<string:city_inbound>', methods=["GET"])
def index(city_inbound):
    try:
        if current_user.is_authenticated:
            valid_request = checking_request_time(session["login_request_date"])
        else:
            valid_request = checking_request_time(session["request_date"])

        if valid_request:
            city_outbound = session["city_outbound"]
            outbound_date = session["outbound_date"]
            inbound_date = session["inbound_date"]
            user_money = session["user_money"]
            title = city_inbound.title()
            data = get_city_information(city_outbound, city_inbound,  outbound_date, inbound_date, user_money)
            attractions_list = data["attractions"]
            living_prices = data["living_prices"]
            tickets_list = [ticket for _, tickets in data["tickets"].items() for ticket in tickets if ticket['price'] <= user_money * 0.8]
            sorted_tickets_by_price = sorted(tickets_list, key=lambda x: x["price"])

            return render_template(
                        'trip/index.html',
                        page_title=title,
                        attractions_list=attractions_list,
                        tickets_data=sorted_tickets_by_price,
                        living_prices=living_prices,
                        city_outbound=city_outbound,
                        city_inbound=city_inbound,
                        outbound_date=outbound_date.strftime("%d-%m-%Y"),
                        inbound_date=inbound_date.strftime("%d-%m-%Y")
            )
        else:
            flash("Заполните форму заново, информация могла устареть")
            return redirect(url_for('trip.start'))
    except Exception as e:
        print(e)
        flash("Заполните форму")
        return redirect(url_for('trip.start'))


@blueprint.route("""/hotels/<int:ticket_price>/<string:city_inbound>
                    /<string:checkin>/<string:checkout>/<string:outbound_date>
                    /<string:city_outbound>/<string:forward_flight_duration>
                    /<string:backward_flight_duration>/""", methods=["GET"])
def hotels(ticket_price, city_inbound, checkin, checkout,
           outbound_date, city_outbound, forward_flight_duration,
           backward_flight_duration):
    try:
        if current_user.is_authenticated:
            valid_request = checking_request_time(session["login_request_date"])
        else:
            valid_request = checking_request_time(session["request_date"])
        if not valid_request:
            flash("Заполните форму заново, информация могла устареть")
            return redirect(url_for('trip.start'))
    except:
        flash("Заполните форму заново, информация могла устареть")
        return redirect(url_for('trip.start'))

    money_amount = session["user_money"] - ticket_price
    ticket = find_ticket(
                    city_outbound,
                    city_inbound,
                    outbound_date,
                    checkout,
                    forward_flight_duration,
                    backward_flight_duration,
                    ticket_price
    )
    if not ticket:
        flash("Заполните форму заново, информация по билетам могла устареть")
        return redirect(url_for('trip.start'))

    checkin = datetime.strptime(checkin, "%d-%m-%Y").strftime("%d/%m/%Y")
    checkout = datetime.strptime(checkout, "%d-%m-%Y").strftime("%d/%m/%Y")
    hotel_list = get_best_hotels(city_inbound, checkin, checkout, money_amount)
    if hotel_list:
        return render_template(
                    "trip/hotels.html",
                    hotel_list=hotel_list,
                    page_title=city_inbound.title(),
                    ticket=ticket
        )
    else:
        flash("Нет доступных отелей с выбранным билетом")
        return redirect(get_redirect_target())
