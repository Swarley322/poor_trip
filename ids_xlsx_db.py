from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, UniqueConstraint
import os
import pandas
import xlrd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import xlsxwriter


# # Workbook() takes one, non-optional, argument  
# # which is the filename that we want to create. 
# workbook = xlsxwriter.Workbook('ids.xlsx')
# # The workbook object is then used to add new  
# # worksheet via the add_worksheet() method. 
# worksheet = workbook.add_worksheet()

# # id_lst = []
# # Give the location of the file 
loc2 = (r"C:\Users\Ikaro\Desktop\projects\skyscanner\ids.xlsx")
wb2 = xlrd.open_workbook(loc2)
sheet2 = wb2.sheet_by_index(0)
sheet2.cell_value(0, 0)

loc = (r"C:\Users\Ikaro\Desktop\projects\skyscanner\copy.xlsx")
# # To open Workbook 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
# # Printing 2-nd column
# for i in range(sheet.nrows):
#    # print(sheet.cell_value(i, 1))
#    url = "https://avia.yandex.ru/city/mow/-moskva/"
#    chromedriver = "C:/Users/Ikaro/Desktop/projects/skyscanner/chromedriver"
#    options = webdriver.ChromeOptions()
#    options.add_argument('headless')
#    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
#    browser.get(url)
#    city_origin = browser.find_element_by_name("fromName")
#    city_origin.send_keys(Keys.BACK_SPACE*20)
#    city_origin.send_keys(sheet.cell_value(i, 1))
#    print(sheet.cell_value(i, 1))
#    print(i)
#    time.sleep(1)
#    city_origin.send_keys(Keys.ENTER)
#    time.sleep(1)
#    new_url = browser.current_url
#    browser.quit()
#    start_origin = new_url.find("fromId=")+len("fromId=")
#    end_origin = new_url.find("&toId")
#    fromID = new_url[start_origin:end_origin]
#    # id_lst.append(fromID)
#    # print(id_lst)
#    # workbook = xlsxwriter.Workbook('ids.xlsx')
#    # worksheet = workbook.add_worksheet()
#    worksheet.write(i, 0, fromID)
#    browser.quit()
# workbook.close()  # IF NO CLOSE THEN XLSX NOT CREATING!!!!!!!!!!

# creating db
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
for city, ids in zip(range(sheet.nrows),range(sheet2.nrows)):
   ins = flights.insert().values(city=sheet.cell_value(city, 1), id=sheet2.cell_value(ids, 0))
   conn = engine.connect()
   result = conn.execute(ins)
