from datetime import datetime, date
from flask import Blueprint, flash, render_template, redirect, session, url_for
from flask_login import current_user

from webapp.trip.forms import StartForm
from webapp.trip.models import AirportId
from webapp.trip.utils.get_random_city import get_random_city
from webapp.trip.utils.get_affordable_cities import get_affordable_cities
from webapp.trip.utils.get_city_information import get_city_information


blueprint = Blueprint("trip", __name__)


@blueprint.route('/')
def start():
    form = StartForm()
    title = "Welcome"
    return render_template('trip/start.html', form=form, page_title=title,)


@blueprint.route('/city', methods=["GET"])
def city():
    current_hour = datetime.now().strftime("%d/%m/%Y %H")
    title = "Your cities"
    if current_user.is_anonymous:
        flash("Please login")
        return redirect(url_for('trip.start'))

    try:
        if session["request_date"] == current_hour:
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
                flash("There are no tickets for this dates, please try another dates")
                return redirect(url_for('trip.start'))
            elif city_list == "Not enough money":
                flash("You are too poor, earn more money")
                return redirect(url_for('trip.start'))
            else:
                return render_template("trip/cards.html", city_list=city_list, page_title=title)

        else:
            flash("Fill the form again")
            return redirect(url_for('trip.start'))
    except KeyError:
        flash("Fill the form")
        return redirect(url_for('trip.start'))


@blueprint.route('/process-data', methods=["POST"])
def process_data():
    form = StartForm()
    if form.validate_on_submit():
        city_outbound = form.city_outbound.data
        user_money = form.money.data
        outbound_date = form.outbound_date.data
        inbound_date = form.inbound_date.data

        airports = AirportId.query.filter(AirportId.city == city_outbound.lower().strip()).count()
        if airports:
            session['city_outbound'] = city_outbound.lower()
        else:
            flash("Incorrect outbound city, please choose russian city with airport")
            return redirect(url_for('trip.start'))

        if outbound_date > inbound_date or outbound_date == inbound_date or outbound_date < date(2020, 7, 1) or outbound_date <= date.today():
            flash("Incorrect dates")
            return redirect(url_for('trip.start'))
        else:
            session["outbound_date"] = datetime.combine(outbound_date, datetime.min.time())
            session["inbound_date"] = datetime.combine(inbound_date, datetime.min.time())

        if user_money <= 0:
            flash("Incorrect money value")
            return redirect(url_for('trip.start'))
        else:
            session['user_money'] = user_money

        session["request_date"] = datetime.now().strftime("%d/%m/%Y %H")

        if current_user.is_anonymous:
            random_city = get_random_city(city_outbound, outbound_date, inbound_date, user_money)
            if random_city == "No tickets":
                flash("There are no tickets for this dates, please try another dates")
                return redirect(url_for('trip.start'))
            elif random_city == "Not enough money":
                flash("You are too poor, earn more money")
                return redirect(url_for('trip.start'))
            else:
                return redirect(url_for('trip.index', city_inbound=random_city))
        else:
            return redirect(url_for('trip.city'))

    flash("Something goes wrong")
    return redirect(url_for('trip.start'))


@blueprint.route('/index/<string:city_inbound>', methods=["GET"])
def index(city_inbound):
    current_hour = datetime.now().strftime("%d/%m/%Y %H")
    try:
        if session["request_date"] == current_hour:

            city_outbound = session["city_outbound"]
            outbound_date = session["outbound_date"]
            inbound_date = session["inbound_date"]
            user_money = session["user_money"]
            title = city_inbound.title()
            data = get_city_information(city_outbound, city_inbound,  outbound_date, inbound_date, user_money)
            hotel_list = data["hotels"]
            attractions_list = data["attractions"]
            tickets_list = [ticket for _, tickets in data["tickets"].items() for ticket in tickets]
            return render_template(
                        'trip/index.html',
                        title=title,
                        hotel_list=hotel_list,
                        attractions_list=attractions_list,
                        tickets_data=tickets_list
            )
        else:
            flash("Fill the form again")
            return redirect(url_for('trip.start'))
    except:
        flash("Fill the form")
        return redirect(url_for('trip.start'))



@blueprint.route('/test')
def test():

    return render_template("test/test.html")
