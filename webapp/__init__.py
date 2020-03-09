from flask import Flask, render_template
from webapp.get_all_hotels import get_best_hotels
# from webapp.skyscanner import get_tickets
from webapp.model import db


def create_app():  # export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        hotel_list = get_best_hotels('Токио')
        # tickets_list = get_tickets("Moscow", "Rome")
        # return render_template('index.html',
        #                        hotel_list=hotel_list,
        #                        tickets_list=tickets_list)
        return render_template('index.html', hotel_list=hotel_list)

    return app
