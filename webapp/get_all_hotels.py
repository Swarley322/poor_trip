from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re

from sqlalchemy import or_
from webapp.model import db, Hotel, AvgPriceReviews, City

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


current_date = datetime.now().strftime('%Y-%m-%d')


def get_url(city, checkcheckin, checkcheckout):
    checkin = checkcheckin.split('/')
    checkout = checkcheckout.split('/')
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


def get_valid_value(value):
    return value if value else None


def get_hotel_information(html, city, checkin, checkout):
    soup = BS(html, 'html.parser')
    hotels = soup.find('div', id='hotellist_inner').find_all('div', {'data-hotelid': re.compile('.*')})
    for hotel in hotels:
        hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()

        week_price = get_valid_value(hotel.find('div', class_="bui-price-display__value prco-inline-block-maker-helper"))
        # print(week_price)
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
        # print(hotel_name)

        safe_information(city, hotel_name, week_price, hotel_link, rating,
                         reviews, img_url, distance, stars, checkin, checkout)


def safe_information(city, hotel_name, week_price, hotel_link, rating,
                     reviews, img_url, distance, stars, checkin, checkout):
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    city_id = City.query.filter(or_(City.ru_name == city.title(),
                                    City.eng_name == city.title())).first()
    hotel_exist = db.session.query(db.exists().where(Hotel.name == hotel_name)
                                              .where(Hotel.parsing_date == current_date)
                                              .where(Hotel.week_number == week_number)
                                              .where(Hotel.year == year)).scalar()
    if not hotel_exist:
        hotel = Hotel(
            name=hotel_name, week_price=week_price,
            checkin_date=checkin, checkout_date=checkout,
            hotel_link=hotel_link, parsing_date=current_date,
            rating=rating, reviews=reviews, stars=stars,
            distance_from_center=distance, img_url=img_url,
            week_number=week_number, city=city_id, year=year
        )
        db.session.add(hotel)
        db.session.commit()


def get_avg_price(city_id, week_number, year):
    count_hotels = 0
    price = 0
    for hotel in Hotel.query.filter(Hotel.city_id == city_id) \
                            .filter(Hotel.parsing_date == current_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year):
        if hotel.week_price:
            price += int(hotel.week_price)
            count_hotels += 1
    return int(price / count_hotels)


def get_avg_reviews(city_id, week_number, year):
    count_hotels = 0
    reviews = 0
    for hotel in Hotel.query.filter(Hotel.city_id == city_id) \
                            .filter(Hotel.parsing_date == current_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year):
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


def get_all_hotels(city, checkin, checkout):
    url = get_url(city, checkin, checkout)
    pages = get_page_count(get_html(url))
    current_page_url = url
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    for page in range(pages - 1):
        print("Parsing process {:05.2f}%".format(page / (pages - 1) * 100))
        html = get_html(current_page_url)
        get_hotel_information(html, city, checkin, checkout)
        current_page_url = get_next_page_href(html)
    city_id = City.query.filter(or_(City.ru_name == city.title(),
                                    City.eng_name == city.title())).first()
    avg_exist = db.session.query(
                    db.exists().where(AvgPriceReviews.city_id == city_id.id)
                               .where(AvgPriceReviews.week_number == week_number)
                               .where(AvgPriceReviews.year == year)).scalar()
    if avg_exist:
        x = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id.id) \
                                 .filter(AvgPriceReviews.week_number == week_number) \
                                 .filter(AvgPriceReviews.year == year).first()
        x.avg_week_price = get_avg_price(city_id.id, week_number, year)
        x.avg_reviews = get_avg_reviews(city_id.id, week_number, year)
        x.avg_day_price = int(get_avg_price(city_id.id, week_number, year) / 7)
        x.parsing_date = current_date
        x.year = year
        db.session.commit()
    else:
        db.session.add(AvgPriceReviews(
            city=city_id,
            avg_reviews=get_avg_reviews(city_id.id, week_number, year),
            avg_week_price=get_avg_price(city_id.id, week_number, year),
            avg_day_price=int(get_avg_price(city_id.id, week_number, year) / 7),
            parsing_date=current_date,
            week_number=week_number,
            year=year)
        )
        db.session.commit()


def get_best_hotels(city, checkin, checkout, money):
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    city_id = City.query.filter(or_(
                            City.ru_name == city.title(),
                            City.eng_name == city.title()
                            )).first().id
    avg_reviews = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id) \
                                       .filter(AvgPriceReviews.parsing_date == current_date) \
                                       .filter(AvgPriceReviews.year == year) \
                                       .first().avg_reviews
    # avg_day_price = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id) \
    #                                      .filter(AvgPriceReviews.parsing_date == current_date) \
    #                                      .filter(AvgPriceReviews.year == year) \
    #                                      .first().avg_day_price
    result = []
    for hotel in Hotel.query.filter(Hotel.parsing_date == current_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year) \
                            .filter(Hotel.city_id == city_id):
        if hotel.reviews and hotel.week_price and \
           hotel.week_price <= money and avg_reviews <= hotel.reviews:
            result.append({
                "hotel_name": hotel.name,
                "rating": hotel.rating,
                "stars": hotel.stars,
                "url": hotel.hotel_link,
                "price": hotel.week_price,
                "img": hotel.img_url
            })
        else:
            continue
    return sorted(result, key=lambda x: x['rating'], reverse=True)