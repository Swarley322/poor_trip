from webapp import create_app
from webapp.parser.booking import get_hotel_information, get_url, safe_information
from webapp.parser.live_prices import get_live_prices
from webapp.parser.utils import get_html


app = create_app()


def test_parsing_one_page():
    with app.app_context():
        city = "Москва"
        checkin = "01/07/2020"
        checkout = "10/07/2020"
        correct_html = get_html(get_url(city, checkin, checkout))
        result1 = get_hotel_information(correct_html, city, checkin, checkout)
        assert result1 > 0


def test_safe_information():
    with app.app_context():
        result = safe_information(
                    city="Москва",
                    hotel_name="test hotel",
                    week_price=10000,
                    hotel_link="test_link",
                    rating=1.1,
                    reviews=1000,
                    img_url="test_url",
                    distance="test_distance",
                    stars="test_stars",
                    checkin="10/10/2020",
                    checkout="10/10/2020"
        )
        assert result == "information saved"


def test_get_living_prices():
    with app.app_context():
        url = "https://www.numbeo.com/cost-of-living/in/{}?displayCurrency=RUB".format("Moscow")
        html = get_html(url)
        result = get_live_prices(html)
        assert result
