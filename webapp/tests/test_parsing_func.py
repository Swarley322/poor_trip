from webapp import create_app
from webapp.parser.live_prices import get_live_prices
from webapp.parser.utils import get_html


app = create_app()


def test_get_living_prices():
    with app.app_context():
        url = "https://www.numbeo.com/cost-of-living/in/{}?displayCurrency=RUB".format("Moscow")
        html = get_html(url)
        result = get_live_prices(html)
        assert result
