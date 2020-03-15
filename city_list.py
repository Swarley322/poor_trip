from googletrans import Translator
# from translate import Translator
from webapp import create_app
from webapp.model import db, City

translator = Translator()
app = create_app()
with app.app_context():
    PART_OF_THE_WORLD = {
            "Europe": {
                "England": ["London", "Liverpool"],
                "Russia": ["Moscow", "Krasnodar", "Domodedovo"]
                },
            "Asia": {
                "Japan": ["Tokyo", "Kyoto"]
                },
            "America": {
                "USA": ["New-York", "Detroit"]
                }
        }

    for world_part, country_list in PART_OF_THE_WORLD.items():
        for country, city_list in country_list.items():
            for city in city_list:
                city = City(
                    eng_name=city, eng_country=country,
                    eng_part_of_the_world=world_part,
                    ru_name=translator.translate(city, dest='ru').text,
                    ru_country=translator.translate(country, dest='ru').text,
                    ru_part_of_the_world=translator.translate(world_part, dest='ru').text
                )
                db.session.add(city)
                db.session.commit()

# PART_OF_THE_WORLD = {
#             "Europe": {
#                 "England": ["London", "Liverpool", "Brighton"],
#                 "Russia": ["Moscow", "Krasnodar"]
#                 },
#             "Asia": {
#                 "Japan": ["Tokyo", "Kyoto"]
#                 },
#             "America": {
#                 "USA": ["New-York", "Detroit"]
#                 }
#         }
# for world_part, country_list in PART_OF_THE_WORLD.items():
#     for country, city_list in country_list.items():
#         for city in city_list:
#             print(translator.translate(city))
