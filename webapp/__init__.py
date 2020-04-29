from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from webapp.db import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.trip.views import blueprint as trip_blueprint


def create_app():  # export FLASK_APP=webapp && export FLASK_ENV=development && FLASK_APP_PORT=5000 && flask run --host=0.0.0.0
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(trip_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
