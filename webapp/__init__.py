from flask import Flask, render_template, request, url_for, redirect, flash
from webapp.get_all_hotels import get_best_hotels, get_all_hotels
from webapp.get_city import get_city_dict
# from webapp.skyscanner import get_tickets
from webapp.model import db
from webapp.forms import Form


def create_app():  # export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def start():
        form = Form()
        if form.validate_on_submit():
            city = request.form["city"].strip().capitalize()
            checkin = request.form["checkin"].strip()
            checkout = request.form["checkout"].strip()
            money = request.form["money"]
            # print(checkin)
            # print(checkout)
            return redirect(url_for("city", city=city, checkin=checkin, checkout=checkout, money=money))
        return render_template('start.html', form=form)

    @app.route('/city', methods=["GET", "POST"])
    def city():
        checkin = request.args["checkin"]
        checkout = request.args["checkout"]
        money = int(request.args["money"])
        city_list = get_city_dict(money, checkin, checkout)
        return render_template("cards2.html", city_list=city_list)

    @app.route('/index')
    def index():
        city = request.args["city"]
        checkin = request.args["checkin"]
        checkout = request.args["checkout"]
        money = int(request.args["money"])
        hotel_list = get_best_hotels(city, checkin, checkout, money)
        return render_template('index2.html', hotel_list=hotel_list)

    @app.route('/cards')
    def cards():
        return render_template("cards.html")

    return app
