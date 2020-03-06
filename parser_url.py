from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, Float
import os
import argparse
import requests

parser = argparse.ArgumentParser(description='Hotel prices')
parser.add_argument('city', type=str, help='City destination')
parser.add_argument('checkin', type=str, help='checkin date (dd/mm/yyyy)')
parser.add_argument('checkout', type=str, help='checkout date (dd/mm/yyyy)')
parser.add_argument('pages', type=int, help='Hotels page count')
args = parser.parse_args()

# basedir = os.path.abspath(os.path.dirname(__file__))

# a = 'sqlite:///' + os.path.join(basedir, 'mydb.db')
# engine = create_engine(a, echo=True)
# meta = MetaData()

# hotels1 = Table(
#    'Hotels', meta,
#    Column('id', Integer, primary_key=True),
#    Column('name', String),
#    Column('price', String),
#    Column('living_date', DateTime),
#    Column('hotel_link', String),
#    Column('parsing_date', DateTime),
#    Column('rating', Float),
#    Column('reviews', Integer),
#    Column('stars', Integer),
#    Column('distance_from_center', Float),
#    Column('img_url', String)
# )
# meta.create_all(engine)




URL = ("https://www.booking.com/searchresults.ru.html?label=gen173nr-1FCAEogg"
       "I46AdIM1gEaMIBiAEBmAEhuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKs6O3yBcACAQ&sid="
       "a3ff7e955c79345eb9c9b141ef56fb5d&sb=1&sb_lp=1&src=index&src_elem=sb&e"
       "rror_url=https%3A%2F%2Fwww.booking.com%2Findex.ru.html%3Flabel%3Dgen1"
       "73nr-1FCAEoggI46AdIM1gEaMIBiAEBmAEhuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKs6O"
       "3yBcACAQ%3Bsid%3Da3ff7e955c79345eb9c9b141ef56fb5d%3Bsb_price_type%3Dt"
       "otal%26%3B&sr_autoscroll=1&ss={city}&is_ski_area=0&checkin_year="
       "{in_year}&checkin_month={in_month}&checkin_monthday={in_day}&che"
       "ckout_year={out_year}&checkout_month={out_month}&checkout_monthday="
       "{out_day}&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filt"
       "ers=&from_sf=1")


def get_url(city, checkin_date, checkout_date):
    checkin = checkin_date.split('/')
    checkout = checkout_date.split('/')
    url = URL.format(city=city, in_year=int(checkin[2]), in_month=int(checkin[1]),
                     in_day=int(checkin[0]), out_year=int(checkout[2]),
                     out_month=int(checkout[1]), out_day=int(checkout[0]))
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
    for hotel in hotels:
        hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()
        
        try:
            raw_price = hotel.find('div', class_='bui-price-display__value prco-inline-block-maker-helper').text.strip()
            price = ''
            for sym in raw_price:
                try:
                    int(sym)
                    price += sym
                except ValueError:
                    continue
        except AttributeError:
            price = 0
        
        hotel_link = 'https://www.booking.com' + hotel.find('a', class_='hotel_name_link url')['href']
        
        try:
            rating = float(hotel.find('div', class_='bui-review-score__badge').text.strip().replace(',', '.'))
        except AttributeError:
            rating = 0.0
        
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
            reviews = 0
        
        try:
            img_url = hotel.find('img', class_='hotel_image')['data-highres']
        except AttributeError:
            img_url = "no photo"
        # result.update({hotel_name: price})
        # ins = hotels1.insert().values(
        #    name=hotel_name, price=price, living_date=, hotel_link=hotel_link,
        #    parsing_date=datetime.now(), rating=rating, reviews=reviews,
        #    stars=stars, distance_from_center=distance, img_url=img_url
        # )
        # conn = engine.connect()
        # result1 = conn.execute(ins)
        print(hotel_name, rating, reviews, img_url, '\n')
    # return result


def get_hotel_description(html):
    soup = BS(html, 'html.parser')
    rows = soup.find('div', id='property_description_content').find_all('p')
    description = ' '.join([row.text for row in rows])
    picture = soup.find('div', id='photo_wrapper').find('img')['src']


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
    picture_soup = BS(get_html('https:' + href), 'html.parser')
    picture_link = picture_soup.find('div', class_='fullImageLink').find('a')['href']
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
        current_page_url = get_next_page_href(html)
    # with open('result.json', 'w', encoding='utf-8') as f:
    #     for hotel, price in result.items():
    #         json.dump((hotel, price), f, ensure_ascii=False)
    #         f.write('\n')
    # for hotel, price in result.items():
    #     print(hotel, '-', price)
    finish = datetime.now() - start
    # print(get_city_picture("Москва"))