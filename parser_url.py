from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re
import json


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


def get_url(city):
    url = URL.format(city=city, in_year=2020, in_month=5,
                     in_day=1, out_year=2020, out_month=5, out_day=22)
    return url


def get_html(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver.page_source


HTML = get_html(get_url('москва'))


def get_hotel_price(html):
    soup = BS(html, 'html.parser')
    hotels = soup.find('div', id='hotellist_inner').find_all('div', {'data-hotelid': re.compile('.*')})
    result = {}
    for hotel in hotels:
        hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()
        try:
            price = hotel.find('div', class_='bui-price-display__value prco-inline-block-maker-helper').text.strip()
        except AttributeError:
            price = 'no room'
        result.update({hotel_name: price})
    return result


def get_page_count(html):
    soup = BS(html, 'html.parser')
    paggination = soup.find_all('ul', class_='bui-pagination__list')[0]
    return int(paggination.find_all('div', class_='bui-u-inline')[-1].text)


def get_next_page_href(html):
    soup = BS(html, 'html.parser')
    href = soup.find('a', {'data-page-next': re.compile('.*')})['href']
    return('https://www.booking.com' + href)


if __name__ == "__main__":
    # get_hotel_price(HTML)
    page_count = get_page_count(HTML)
    # print('Pages found:', page_count)
    # print(get_next_page_href(HTML))
    result = []
    current_page_url = get_url('москва')
    for page in range(page_count - 1):
        result.append(get_hotel_price(get_html(current_page_url)))
        print("Parsing process {:05.2f}%".format(page / (page_count - 1) * 100))
        current_page_url = get_next_page_href(get_html(current_page_url))
    with open('result.json', 'w', encoding='utf-8') as f:
        for page in result:
            json.dump(page, f, ensure_ascii=False)
