from googletrans import Translator
import csv

translator = Translator()

result = []

for world_part, country_list in PART_OF_THE_WORLD.items():
    for country, city_list in country_list.items():
        for city in city_list:
            result.append(
                {
                    "eng_name": city,
                    "eng_country": country,
                    "eng_part_of_the_world": world_part,
                    "ru_name": translator.translate(city, dest='ru').text,
                    "ru_country": translator.translate(country, dest='ru').text,
                    "ru_part_of_the_world": translator.translate(world_part, dest='ru').text
                }
            )


with open('cities_list.csv', 'a+', encoding='utf-8', newline='') as f:
    fields = ['eng_name', 'eng_country', 'eng_part_of_the_world', 'ru_name', 'ru_country', "ru_part_of_the_world"]
    writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
    for city in result:
        writer.writerow(city)
