from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re

from webapp.model import db, Hotel, AvgPriceReviews

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


CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')


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
            stars = hotel.find('span', class_='sr-hotel__title-badges') \
                         .find('span', class_='invisible_spoken').text.strip()
        except AttributeError:
            stars = None

        safe_information(hotel_name, week_price, hotel_link, rating,
                         reviews, img_url, distance, stars)


def safe_information(hotel_name, week_price, hotel_link, rating,
                     reviews, img_url, distance, stars):
    hotel_exist = Hotel.query.filter(Hotel.name == hotel_name) \
                             .filter(Hotel.parsing_date == CURRENT_DATE).count()
    if not hotel_exist:
        hotel = Hotel(
            name=hotel_name, week_price=week_price,
            living_date="01/05/2020-10/05/2020",
            hotel_link=hotel_link, parsing_date=CURRENT_DATE,
            rating=rating, reviews=reviews, stars=stars,
            distance_from_center=distance, img_url=img_url, city="Токио"
        )
        db.session.add(hotel)
        db.session.commit()


def get_avg_price(city):
    count_hotels = 0
    price = 0
    for hotel in Hotel.query.filter(Hotel.city == city.title()) \
                            .filter(Hotel.parsing_date == CURRENT_DATE):
        if hotel.week_price:
            price += int(hotel.week_price)
            count_hotels += 1
    return int(price / count_hotels)


def get_avg_reviews(city):
    count_hotels = 0
    reviews = 0
    for hotel in Hotel.query.filter(Hotel.city == city.title()) \
                            .filter(Hotel.parsing_date == CURRENT_DATE):
        if hotel.reviews:
            reviews += int(hotel.reviews)
        count_hotels += 1
    return int(reviews / count_hotels)


# def get_hotel_description(html):
#     soup = BS(html, 'html.parser')
#     rows = soup.find('div', id='property_description_content').find_all('p')
#     description = ' '.join([row.text for row in rows])
#     # picture = soup.find('div', id='photo_wrapper').find('img')['src']
#     return description


def get_page_count(html):
    soup = BS(html, 'html.parser')
    paggination = soup.find_all('ul', class_='bui-pagination__list')[0]
    return int(paggination.find_all('div', class_='bui-u-inline')[-1].text)


def get_next_page_href(html):
    soup = BS(html, 'html.parser')
    href = soup.find('a', {'data-page-next': re.compile('.*')})['href']
    return('https://www.booking.com' + href)


def get_hotels(city, in_date, out_date):
    url = get_url(city, in_date, out_date)
    pages = get_page_count(get_html(url))
    current_page_url = url
    for page in range(pages - 1):
        print("Parsing process {:05.2f}%".format(page / (pages - 1) * 100))
        html = get_html(current_page_url)
        get_hotel_information(html)
        current_page_url = get_next_page_href(html)
    if not AvgPriceReviews.query.filter(AvgPriceReviews.city == "Токио").count():
        db.session.add(AvgPriceReviews(
            city="Токио",
            avg_reviews=get_avg_reviews("Токио"),
            avg_price=get_avg_price("Токио"),
            date=CURRENT_DATE
        ))
        db.session.commit()
    else:
        x = AvgPriceReviews.query.filter(AvgPriceReviews.city == "Токио").first()
        x.avg_price = get_avg_price("Токио")
        x.avg_reviews = get_avg_reviews("Токио")
        x.date = CURRENT_DATE
        db.session.commit()


def get_best_hotels(city):
    result = []
    avg_reviews = AvgPriceReviews.query.filter(AvgPriceReviews.city == city) \
                                       .filter(AvgPriceReviews.date == CURRENT_DATE) \
                                       .first().avg_reviews
    max_price = 0 # здесь должна быть максимальная стоимость проживания для рекомендации отелей
    for hotel in Hotel.query.filter(Hotel.parsing_date == CURRENT_DATE):
        if hotel.reviews and hotel.week_price:
            if hotel.reviews < avg_reviews:
                continue
            else:
                result.append({
                    "hotel_name": hotel.name,
                    "rating": hotel.rating,
                    "stars": hotel.stars,
                    "url": hotel.hotel_link,
                    "price": hotel.week_price
                })
        else:
            continue
    return sorted(result, key=lambda x: x['rating'], reverse=True)