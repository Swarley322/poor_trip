from datetime import datetime

from flask import Blueprint, flash, render_template, redirect, request, url_for, session, request

from webapp.trip.forms import StartForm
from webapp.trip.utils.get_affordable_cities import get_cities_dict
from webapp.trip.utils.get_attractions import get_attractions_list
from webapp.trip.utils.get_recommended_hotels import get_best_hotels
from webapp.trip.utils.get_tickets_prices import get_tickets_prices

from webapp.trip.models import AirportId


# from webapp.trip.tickets import get_data, get_html
# from datetime import datetime

blueprint = Blueprint("trip", __name__)


@blueprint.route('/')
def start():
    form = StartForm()
    title = "Welcome"
    return render_template('trip/start.html', form=form, page_title=title,)


@blueprint.route('/city', methods=["GET", "POST"])
def city():
    if request.method == 'GET':
        # return session['city'].title()
        # return session['checkin'].strftime("%d/%m/%Y")
        return session['checkout'].strftime("%d/%m/%Y")
        # return session['money']

    form = StartForm()
    title = "Your cities"
    if form.validate_on_submit():
        city = form.city.data
        user_money = form.money.data
        checkin = form.checkin.data
        checkout = form.checkout.data

        airports = AirportId.query.filter(AirportId.city == city.lower().strip()).count()
        if airports:
            session['city'] = city.lower()
        else:
            flash("Incorrect outbound city, please choose russian city with airport")
            return redirect(url_for('trip.start'))

        if checkin > checkout or checkin == checkout or checkin <= datetime.now():
            flash("Incorrect dates")
            return redirect(url_for('trip.start'))
        else:
            session['checkin'] = checkin
            session['checkout'] = checkout
            session['money'] = user_money


        # tickets_price = get_tickets_prices(city.strip(), checkin.strftime("%d/%m/%Y")
        # money = user_money - int(tickets_price[0]["price"].replace("Р", ""))

        city_list = get_cities_dict(user_money, checkin.strftime("%d/%m/%Y"), checkout.strftime("%d/%m/%Y"))
        return render_template("trip/cards.html", city_list=city_list, page_title=title)
    flash("Incorrect money value")
    return redirect(url_for('trip.start'))


@blueprint.route('/index')
def index():
    city = session['city'].lower()
    checkin = session["checkin"]
    checkout = session["checkout"]
    money = session["money"]
    hotel_list = get_best_hotels(city, checkin, checkout, money)
    attractions_list = get_attractions_list(city)
    # html = get_html(city, "Новосибирск", datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y-%m-%d"), datetime.strptime(checkout, "%d/%m/%Y").strftime("%Y-%m-%d"), "2")
    # tickets_list = get_data(html)
    # print(tickets_list)
    # return render_template('trip/index.html', hotel_list=hotel_list, tickets_list=tickets_list)
    return render_template('trip/index.html', hotel_list=hotel_list, attractions_list=attractions_list)


@blueprint.route('/guest')
def guest():
    pass
