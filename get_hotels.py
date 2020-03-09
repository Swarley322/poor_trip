from webapp import create_app
from webapp.get_all_hotels import get_hotels

app = create_app()
with app.app_context():
    get_hotels("Токио", "01/05/2020", "08/05/2020")
