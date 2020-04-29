import re
import time
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
from pytz import timezone
from statistics import median
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from sqlalchemy import or_

from webapp.db import db
from webapp.trip.models import Hotel, AvgPriceReviews, City
from webapp.parser.utils import get_html, get_random_sleep_time


URL = ("https://www.booking.com/searchresults.ru.html?label=gen173nr-1FCAEogg"
       "I46AdIM1gEaMIBiAEBmAEhuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKs6O3yBcACAQ&sid="
       "a3ff7e955c79345eb9c9b141ef56fb5d&sb=1&sb_lp=1&src=index&src_elem=sb&e"
       "rror_url=https%3A%2F%2Fwww.booking.com%2Findex.ru.html%3Flabel%3Dgen1"
       "73nr-1FCAEoggI46AdIM1gEaMIBiAEBmAEhuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKs6O"
       "3yBcACAQ%3Bsid%3Da3ff7e955c79345eb9c9b141ef56fb5d%3Bsb_price_type%3Dt"
       "otal%26%3B&sr_autoscroll=1&ss={city}&is_ski_area=0&checkin_year="
       "{in_year}&checkin_month={in_month}&checkin_monthday={in_day}&che"
       "ckout_year={out_year}&checkout_month={out_month}&checkout_monthday="
       "{out_day}&group_adults={adults}&group_children={children}&"
       "no_rooms={rooms}&b_h4u_keep_filters=&from_sf=1")

URL2 =("https://www.booking.com/searchresults.ru.html?aid=376376&label=bdot-hZ"
       "BHoyX7oowYFZ8BpwaLIwS410902425028%3Apl%3Ata%3Ap1%3Ap22.590.000%3Aac%3A"
       "ap%3Aneg%3Afi%3Atikwd-299974808121%3Alp9040938%3Ali%3Adec%3Adm%3Appccp"
       "%3DUmFuZG9tSVYkc2RlIyh9Yf23yREhrOV9YczHwt1OUN4&lang=ru&sid=201994ecbd9"
       "174dd1e493f1990dd086b&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=htt"
       "ps%3A%2F%2Fwww.booking.com%2Findex.ru.html%3Faid%3D376376%3Blabel%3Dbd"
       "ot-hZBHoyX7oowYFZ8BpwaLIwS410902425028%253Apl%253Ata%253Ap1%253Ap22.59"
       "0.000%253Aac%253Aap%253Aneg%253Afi%253Atikwd-299974808121%253Alp904093"
       "8%253Ali%253Adec%253Adm%253Appccp%253DUmFuZG9tSVYkc2RlIyh9Yf23yREhrOV9"
       "YczHwt1OUN4%3Bsid%3D201994ecbd9174dd1e493f1990dd086b%3Bsb_price_type%3"
       "Dtotal%26%3B&ss={city}&is_ski_area=0&ssne=%D0%A2%"
       "D0%BE%D0%BA%D0%B8%D0%BE&ssne_untouched=%D0%A2%D0%BE%D0%BA%D0%B8%D0%BE&"
       "checkin_year={in_year}&checkin_month={in_month}&checkin_monthday={in_day}&checkout_year={out_year}"
       "&checkout_month={out_month}&checkout_monthday={out_day}&group_adults={adults}&group_children={children}&"
       "no_rooms={rooms}&b_h4u_keep_filters=&from_sf=1&ss_raw=Toron&ac_position=0&ac_"
       "langcode=en&ac_click_type=b&dest_id=-574890&dest_type=city&iata=YTO&pla"
       "ce_id_lat=43.652&place_id_lon=-79.381966&search_pageview_id=bea27c971c1"
       "0001a&search_selected=true&search_pageview_id=bea27c971c10001a&ac_sugge"
       "stion_list_length=5&ac_suggestion_theme_list_length=0")


# current_date = datetime.now(timezone("Europe/Moscow")).strftime('%Y-%m-%d')
yesterday_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=1)).strftime('%Y-%m-%d')


def get_url(city, checkin_arg, checkout_arg):
    checkin = checkin_arg.split('/')
    checkout = checkout_arg.split('/')
    url = URL.format(
        city=city, in_year=int(checkin[2]), in_month=int(checkin[1]),
        in_day=int(checkin[0]), out_year=int(checkout[2]),
        out_month=int(checkout[1]), out_day=int(checkout[0]),
        adults=2, children=0, rooms=1
    )
    return url


def get_valid_value(value):
    return value if value else None


def get_hotel_information(html, city, checkin, checkout):
    soup = BS(html, 'html.parser')
    # hotels = soup.find('div', id='hotellist_inner').find_all('div', {'data-hotelid': re.compile('.*')})
    hotels = soup.find_all('div', {'data-hotelid': re.compile('.*')})
    for hotel in hotels:
        hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()

        week_price = get_valid_value(hotel.find('div', class_="bui-price-display__value prco-inline-block-maker-helper"))
        if week_price:
            week_price = int(''.join([digit for digit in week_price.text.strip() if digit.isdigit()]))

        hotel_link = 'https://www.booking.com' + hotel.find('a', class_='hotel_name_link url')['href']

        rating = get_valid_value(hotel.find('div', class_='bui-review-score__badge'))
        if rating:
            rating = get_valid_value(float(rating.text.strip().replace(',', '.')))

        reviews = get_valid_value(hotel.find('div', class_='bui-review-score__text'))
        if reviews:
            reviews = int(''.join([digit for digit in reviews.text.strip() if digit.isdigit()]))

        img_url = get_valid_value(hotel.find('img', class_='hotel_image')['data-highres'])

        distance = get_valid_value(hotel.find('span', {'data-tooltip-position': "top"}))
        if distance:
            distance = distance.text.strip()

        stars = get_valid_value(hotel.find('span', class_='sr-hotel__title-badges')
                                     .find('span', class_='invisible_spoken'))
        if stars:
            stars = stars.text.strip()
        safe_information(city, hotel_name, week_price, hotel_link, rating,
                         reviews, img_url, distance, stars, checkin, checkout)


def safe_information(city, hotel_name, week_price, hotel_link, rating,
                     reviews, img_url, distance, stars, checkin, checkout):

    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    if week_price:
        avg_day_price = int(week_price / 7)
    else:
        avg_day_price = None
    city_id = City.query.filter(or_(City.ru_name == city.lower(),
                                    City.eng_name == city.lower())).first()
    hotel_exist = db.session.query(db.exists().where(Hotel.name == hotel_name)
                                              .where(Hotel.parsing_date == parsing_date)
                                              .where(Hotel.week_number == week_number)
                                              .where(Hotel.year == year)).scalar()
    if not hotel_exist:
        hotel = Hotel(
            name=hotel_name,
            week_price=week_price,
            avg_day_price=avg_day_price,
            checkin_date=checkin,
            checkout_date=checkout,
            hotel_link=hotel_link,
            parsing_date=parsing_date,
            rating=rating,
            reviews=reviews,
            stars=stars,
            distance_from_center=distance,
            img_url=img_url,
            week_number=week_number,
            city_id=city_id.id,
            year=year
        )
        db.session.add(hotel)
        db.session.commit()


def get_avg_price(city_id, week_number, year):
    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")
    price = []
    for hotel in Hotel.query.filter(Hotel.city_id == city_id) \
                            .filter(Hotel.parsing_date == parsing_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year):
        if hotel.week_price:
            price.append(int(hotel.week_price))
    return int(median(price))


def get_avg_reviews(city_id, week_number, year):
    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")
    count_hotels = 0
    reviews = 0
    for hotel in Hotel.query.filter(Hotel.city_id == city_id) \
                            .filter(Hotel.parsing_date == parsing_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year):
        if hotel.reviews:
            reviews += int(hotel.reviews)
            count_hotels += 1
    return int(reviews / count_hotels)


def get_page_count(html):
    soup = BS(html, 'html.parser')
    paggination = soup.find_all('ul', class_='bui-pagination__list')[0]
    return int(paggination.find_all('div', class_='bui-u-inline')[-1].text)


def get_next_page_href(html):
    soup = BS(html, 'html.parser')
    href = soup.find('a', {'data-page-next': re.compile('.*')})['href']
    return('https://www.booking.com' + href)


def repeat_get_html(url):
    html = get_html(url)
    if not html:
        return False
    return html


def get_all_hotels(city, checkin, checkout):
    """Parsing all hotels in the city in 7 days range, adding all hotels information and averageinfo in db

    params:
    - city: string object, city name in russian
    - checkin: string object, checkin date in format dd/mm/YYYY
    - checkout: string object, checkout date in format dd/mm/YYYY

    return: bool object "False or True"
    """

    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")
    url = get_url(city, checkin, checkout)
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    html = get_html(url)
    if not html:
        print("First HTML doesn't returned, requesting again")
        time.sleep(get_random_sleep_time())
        html = get_html(url)
        if not html:
            print("First HTML doesn't returned at all")
            return False
    try:
        pages = get_page_count(html)
    except Exception as e:
        print(e)
        print(f"HTML for pages, {city}-{checkin}-{checkout} doesn't returned")
        return False
    print(f"Parsing process {city} - {checkin} - {checkout} - started")

    for page in range(pages - 1):
        html = get_html(url)
        if not html:
            time.sleep(get_random_sleep_time())
            print(f"HTML for {page + 1}/{pages} doesn't returned, requesting again")
            html = get_html(url)
            if not html:
                time.sleep(get_random_sleep_time())
                print(f"HTML for {page + 1}/{pages} doesn't returned, requesting again 2")
                html = get_html(url)
                if not html:
                    print(f"HTML for {page + 1}/{pages}doesn't returned at all")
                    return True
        try:
            get_hotel_information(html, city, checkin, checkout)
            url = get_next_page_href(html)
        except Exception as e:
            print(e)
            print(f"Page {page + 1}/{pages} crashed, trying again")
            try:
                time.sleep(get_random_sleep_time())
                print(f"Parsing page {page + 1}/{pages} again")
                html = get_html(url)
                get_hotel_information(html, city, checkin, checkout)
                url = get_next_page_href(html)
            except Exception as e:
                print(e)
                print(f"Page {page + 1}/{pages} crashed, second TIME")
                continue
        # print(f"page {page + 1}/{pages} parsed  time={datetime.now()}")
        time.sleep(get_random_sleep_time())
    city_id = City.query.filter(or_(City.ru_name == city.lower(),
                                    City.eng_name == city.lower())).first().id
    avg_exist = db.session.query(
                    db.exists().where(AvgPriceReviews.city_id == city_id)
                               .where(AvgPriceReviews.week_number == week_number)
                               .where(AvgPriceReviews.year == year)).scalar()
    if avg_exist:
        x = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id) \
                                 .filter(AvgPriceReviews.week_number == week_number) \
                                 .filter(AvgPriceReviews.year == year).first()
        x.avg_week_price = get_avg_price(city_id, week_number, year)
        x.avg_reviews = get_avg_reviews(city_id, week_number, year)
        x.avg_day_price = int(get_avg_price(city_id, week_number, year) / 7)
        x.parsing_date = parsing_date
        x.year = year
        db.session.commit()
    else:
        db.session.add(AvgPriceReviews(
            city_id=city_id,
            avg_reviews=get_avg_reviews(city_id, week_number, year),
            avg_week_price=get_avg_price(city_id, week_number, year),
            avg_day_price=int(get_avg_price(city_id, week_number, year) / 7),
            parsing_date=parsing_date,
            week_number=week_number,
            year=year)
        )
        db.session.commit()
    return True
