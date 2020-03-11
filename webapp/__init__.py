from flask import Flask, render_template, request, url_for, redirect, flash
from webapp.get_all_hotels import get_best_hotels
# from webapp.skyscanner import get_tickets
from webapp.model import db
from webapp.forms import LoginForm


def create_app():  # export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def start():
        form = LoginForm()
        if form.validate_on_submit():
            city = request.form["city"]
            return redirect(url_for("index", city=city))
        return render_template('start.html', form=form)

    @app.route('/index')
    def index():
        hotel_list = get_best_hotels(request.args.get("city"))
        return render_template('index.html', hotel_list=hotel_list)

    return app
