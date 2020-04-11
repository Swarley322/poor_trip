from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, UniqueConstraint
import os
import pandas
import xlrd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import xlsxwriter

# connecting to db or creating if not found target file
basedir = os.path.abspath(os.path.dirname(__file__))

a = 'sqlite:///' + os.path.join(basedir, 'cities_ids.db')

engine = create_engine(a, echo=True)
meta = MetaData()

flights = Table(
   'citiesids', meta,
   Column('city', String),
   Column('id', String),
)
meta.create_all(engine)

loc = (r"C:/Users/Ikaro/Desktop/projects/yandexflights/worldcities.xlsx")
# # To open Workbook 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
# # Printing 2-nd column
for city in range(sheet.nrows):
    # getting cities names as strings
    # print(sheet.cell_value(city, 1)) # 1 - is a column number(means 2-nd), 0- value of the cell in 2-nd column
    url = "https://avia.yandex.ru/city/mow/-moskva/"
    chromedriver = "C:/Users/Ikaro/Desktop/projects/yandexflights/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    browser.get(url)
    city_origin = browser.find_element_by_name("fromName")
    city_origin.send_keys(Keys.BACK_SPACE*20)
    city_origin.send_keys(sheet.cell_value(city, 1))
    print(sheet.cell_value(city, 1))
    print(city)
    time.sleep(1)
    city_origin.send_keys(Keys.ENTER)
    time.sleep(1)
    new_url = browser.current_url
    browser.quit()
    start_origin = new_url.find("fromId=")+len("fromId=")
    end_origin = new_url.find("&toId")
    ID = new_url[start_origin:end_origin]
    # worksheet.write(city, 0, ID)
    ins = flights.insert().values(city=sheet.cell_value(city, 1), id=ID)
    conn = engine.connect()
    result = conn.execute(ins)
