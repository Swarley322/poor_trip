from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
import re


dates = {'checkin': {'year': 2020, 'month': 4, 'day': 13},
         'checkout': {'year': 2020, 'month': 4, 'day': 25}}
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# options=chrome_options


def get_html(url, city, dates):
    driver.get(url)
    elem = driver.find_element_by_name("ss")
    elem.send_keys(city)
    elem.send_keys(Keys.RETURN)
    user_checkin = (
            'checkin_year={year}&checkin_month={month}'
            '&checkin_monthday={day}'.format(**dates['checkin'])
    )
    user_checkout = (
            'checkout_year={year}&checkout_month='
            '{month}&checkout_monthday={day}'.format(**dates['checkout'])
    )
    incorrect_checkin = 'checkin_year=&checkin_month='
    incorrect_checkout = 'checkout_year=&checkout_month='
    correct_url = driver.current_url.replace(incorrect_checkin, user_checkin).replace(incorrect_checkout, user_checkout)
    print(correct_url)
    driver.get(correct_url)
    # with open('text.html', 'w', encoding='utf-8') as f:
    #     f.write(driver.page_source)
    return driver.page_source


def get_hotel_price(city, dates):
    html = get_html("https://www.booking.com/", city, dates)
    if html:
        soup = BS(html, 'html.parser')
        hotels = soup.find('div', id='hotellist_inner').find_all('div', {'data-hotelid': re.compile('.*')})
        result = []
        for hotel in hotels:
            hotel_name = hotel.find('span', class_="sr-hotel__name").text.strip()
            try:
                price = hotel.find('div', class_='bui-price-display__value prco-inline-block-maker-helper').text.strip()
            except AttributeError:
                price = 'no room'
            print(hotel_name, price)
            result.append({hotel_name: price})
        print(len(result))

        # print(hotels[0])
        # with open('text2.html', 'w', encoding='utf-8') as f:
        #     for hotel in hotels:
        #         f.write(hotel.prettify())


if __name__ == "__main__":
    get_hotel_price("Moscow", dates)
