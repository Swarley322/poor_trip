from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import argparse

parser = argparse.ArgumentParser(description='Hotel prices')
parser.add_argument('city', type=str, help='City destination')
parser.add_argument('checkin', type=str, help='checkin date (dd/mm/yyyy)')
parser.add_argument('checkout', type=str, help='checkout date (dd/mm/yyyy)')
parser.add_argument('pages', type=int, help='Hotels page count')
args = parser.parse_args()

basedir = os.path.abspath(os.path.dirname(__file__))

a = 'sqlite:///' + os.path.join(basedir, 'mydb.db')
engine = create_engine(a, echo=False)
base = declarative_base()


class Hotel(base):
    __tablename__ = 'Hotels'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    name = Column(String)
    week_price = Column(String, nullable=True)
    living_date = Column(String)
    hotel_link = Column(String)
    parsing_date = Column(String)
    rating = Column(Float)
    reviews = Column(Integer)
    stars = Column(String, nullable=True)
    distance_from_center = Column(String)
    img_url = Column(String)

    def __repr__(self):
        return f"Hotel(city={city}, name={name}, week_price={week_price}, living_date={living_date}, hotel_link={hotel_link}, parsing_date={parsing_date}, rating={rating}, reviews={reviews}, stars={stars}, distance_from_center={distance_from_center}, img_url={img_url}"


class AvgPriceReviews(base):
    __tablename__ = "City"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    avg_reviews = Column(Integer)
    avg_price = Column(Integer)

    def __repr__(self):
        return f"AvgReviews(city={city}, avg_price={avg_price}, avg_reviews={avg_reviews}"


base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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


def get_url(city, checkin_date, checkout_date):
    checkin = checkin_date.split('/')
    checkout = checkout_date.split('/')
    url = URL.format(
        city=city, in_year=int(checkin[2]), in_month=int(checkin[1]),
        in_day=int(checkin[0]), out_year=int(checkout[2]),
        out_month=int(checkout[1]), out_day=int(checkout[0]),
        adults=2, children=0, rooms=1
    )
    return url


def get_html(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver.page_source


def get_hotel_information(html):
    soup = BS(html, 'html.parser')
    hotels = soup.find('div', id='hotellist_inner').find_all('div', {'data-hotelid': re.compile('.*')})
    # result = {}
    # result = []
    for hotel in hotels:
        hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()

        try:
            raw_price = hotel.find('div', class_='bui-price-display__value prco-inline-block-maker-helper').text.strip()
            week_price = ''
            for sym in raw_price:
                try:
                    int(sym)
                    week_price += sym
                except ValueError:
                    continue
        except AttributeError:
            week_price = None

        hotel_link = 'https://www.booking.com' + hotel.find('a', class_='hotel_name_link url')['href']

        try:
            rating = float(hotel.find('div', class_='bui-review-score__badge').text.strip().replace(',', '.'))
        except AttributeError:
            rating = None

        try:
            raw_reviews = hotel.find('div', class_='bui-review-score__text').text.strip()
            reviews = ''
            for sym in raw_reviews:
                try:
                    int(sym)
                    reviews += sym
                except ValueError:
                    continue
        except AttributeError:
            reviews = None
        
        try:
            img_url = hotel.find('img', class_='hotel_image')['data-highres']
        except AttributeError:
            img_url = "no photo"

        try:
            distance = hotel.find('span', {'data-tooltip-position': "top"}).text.strip()
        except AttributeError:
            distance = 'no information'
        # result.update({hotel_name: price})

        try:
            stars = hotel.find('span', class_='sr-hotel__title-badges').find('span', class_='invisible_spoken').text.strip()
        except AttributeError:
            stars = None
            
        if not session.query(Hotel).filter(Hotel.name == hotel_name).filter(Hotel.parsing_date == datetime.now().strftime('%Y-%m-%d')).count():
            hotel = Hotel(
                name=hotel_name, week_price=week_price,  # one_day_price=one_day_price,
                living_date=args.checkin + '-' + args.checkout, 
                hotel_link=hotel_link, parsing_date=datetime.now().strftime('%Y-%m-%d'),
                rating=rating, reviews=reviews, stars=stars,
                distance_from_center=distance, img_url=img_url, city=args.city.title()
            )
            session.add(hotel)
            session.commit()
        # print(hotel_name, rating, reviews, img_url, '\n')
        # result.append(hotel_link)
        # print(hotel_name, distance)
    # return result


def get_avg_price(city):
    count_hotels = 0
    price = 0
    for hotel in session.query(Hotel).filter(Hotel.city == city.title()):
        if hotel.week_price:
            price += int(hotel.week_price)
            count_hotels += 1
    return int(price / count_hotels)


def get_avg_reviews(city):
    count_hotels = 0
    reviews = 0
    for hotel in session.query(Hotel).filter(Hotel.city == city.title()):
        if hotel.reviews:
            reviews += int(hotel.reviews)
        count_hotels += 1
    return int(reviews / count_hotels)


def get_hotel_description(html):
    soup = BS(html, 'html.parser')
    rows = soup.find('div', id='property_description_content').find_all('p')
    description = ' '.join([row.text for row in rows])
    # picture = soup.find('div', id='photo_wrapper').find('img')['src']
    return description


def get_page_count(html):
    soup = BS(html, 'html.parser')
    paggination = soup.find_all('ul', class_='bui-pagination__list')[0]
    return int(paggination.find_all('div', class_='bui-u-inline')[-1].text)


def get_next_page_href(html):
    soup = BS(html, 'html.parser')
    href = soup.find('a', {'data-page-next': re.compile('.*')})['href']
    return('https://www.booking.com' + href)


def get_city_picture(city):
    # html = requests.get(f'https://ru.wikipedia.org/wiki/{city}')
    html = get_html(f'https://ru.wikipedia.org/wiki/{city}')
    soup = BS(html, 'html.parser')
    href = soup.find('td', class_='infobox-image').find('a')['href']
    # picture_soup = BS(get_html('https:' + href), 'html.parser')
    # picture_link = picture_soup.find('div', class_='fullImageLink').find('a')['href']
    return picture_link


if __name__ == "__main__":
    # get_hotel_information(HTML)
    start = datetime.now()
    # page_count = get_page_count(get_html(get_url(args.city, args.checkin, args.checkout)))
    # print('Pages found:', page_count)
    # print(get_next_page_href(HTML))
    # result = {}
    current_page_url = get_url(args.city, args.checkin, args.checkout)
    for page in range(args.pages):
        print("Parsing process {:05.2f}%".format(page / (args.pages) * 100))
        html = get_html(current_page_url)
        # result.update(get_hotel_information(html))
        get_hotel_information(html)
        # for hotel in get_hotel_information(html):
        #     print(get_hotel_description(get_html(hotel)))
        current_page_url = get_next_page_href(html)
    if not session.query(AvgPriceReviews).filter(AvgPriceReviews.city == args.city).count():
        session.add(AvgPriceReviews(
            city=args.city,
            avg_reviews=get_avg_reviews(args.city),
            avg_price=get_avg_price(args.city)
            )
        )
        session.commit()
    else:
        x = session.query(AvgPriceReviews).filter(AvgPriceReviews.city == args.city).first()
        x.avg_price = get_avg_price(args.city)
        x.avg_reviews = get_avg_reviews(args.city)
        session.commit()

    finish = datetime.now() - start
    print(finish)
    # print(get_city_picture("Москва"))