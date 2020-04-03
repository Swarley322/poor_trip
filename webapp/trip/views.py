from flask import Blueprint, render_template, redirect, request, url_for
from webapp.trip.forms import StartForm
from webapp.trip.get_city import get_city_dict
from webapp.trip.get_all_hotels import get_best_hotels


blueprint = Blueprint("trip", __name__)


@blueprint.route('/', methods=["GET", "POST"])
def start():
    form = StartForm()
    title = "Welcome"
    if form.validate_on_submit():
        city = request.form["city"].strip().capitalize()
        checkin = request.form["checkin"].strip()
        checkout = request.form["checkout"].strip()
        money = request.form["money"]
        # print(checkin)
        # print(checkout)
        return redirect(url_for("trip.city", city=city, checkin=checkin, checkout=checkout, money=money))
    return render_template('trip/start.html', form=form, page_title=title)


@blueprint.route('/city', methods=["GET", "POST"])
def city():
    title = "Your cities"
    checkin = request.args["checkin"]
    checkout = request.args["checkout"]
    money = int(request.args["money"])
    city_list = get_city_dict(money, checkin, checkout)
    return render_template("trip/cards.html", city_list=city_list, page_title=title)


@blueprint.route('/index')
def index():
    city = request.args["city"]
    checkin = request.args["checkin"]
    checkout = request.args["checkout"]
    money = int(request.args["money"])
    hotel_list = get_best_hotels(city, checkin, checkout, money)
    return render_template('trip/index.html', hotel_list=hotel_list)
