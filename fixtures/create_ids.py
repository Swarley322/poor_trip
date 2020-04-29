import csv


with open('ru_cities.csv', 'r', encoding='utf-8', newline='') as f:
    fields = ['1', '2', '3', '4', '5', '6', 'name']
    cities = csv.DictReader(f, fields, delimiter=',')
    for city in cities:
        print(city['name'])



# with open('ids.csv', 'a+', encoding='utf-8', newline='') as f:
#     fields = ["city","id"]
#     writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
#     for city in result:
#         writer.writerow(city)