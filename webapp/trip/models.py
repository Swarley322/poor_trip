from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from webapp.db import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eng_part_of_the_world = db.Column(db.String)
    ru_part_of_the_world = db.Column(db.String)
    eng_name = db.Column(db.String, unique=True)
    ru_name = db.Column(db.String, unique=True)
    eng_country = db.Column(db.String)
    ru_country = db.Column(db.String)
    city_img = db.Column(db.String, nullable=True)
    living_prices = db.Column(JSON, nullable=True)

    def __repr__(self):
        return f"""City information (name={self.ru_name},
                country={self.ru_country},
                part_of_the_world={self.ru_part_of_the_world}"""


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(
            db.Integer,
            db.ForeignKey("city.id", ondelete="CASCADE"),
            index=True
    )
    name = db.Column(db.String)
    week_price = db.Column(db.Integer, nullable=True)
    avg_day_price = db.Column(db.Integer, nullable=True)
    checkin_date = db.Column(db.String)
    checkout_date = db.Column(db.String)
    hotel_link = db.Column(db.String)
    parsing_date = db.Column(db.String)  # dd/mm/YYYY
    week_number = db.Column(db.Integer)
    rating = db.Column(db.Float, nullable=True)
    reviews = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.String, nullable=True)
    distance_from_center = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=True)
    year = db.Column(db.Integer)

    city = relationship("City", backref="hotels")

    def __repr__(self):
        return f"Hotel(city={self.city_id}, name={self.name}, week_price={self.week_price}"


class AvgPriceReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(
            db.Integer,
            db.ForeignKey("city.id", ondelete="CASCADE"),
            index=True
    )
    avg_reviews = db.Column(db.Integer)
    avg_week_price = db.Column(db.Integer)
    avg_day_price = db.Column(db.Integer)
    parsing_date = db.Column(db.String)  # dd/mm/YYYY
    week_number = db.Column(db.Integer)
    year = db.Column(db.Integer)

    city = relationship("City", backref="avg_price")

    def __repr__(self):
        return f"""AvgReviews(city={self.city_id},
                avg_day_price={self.avg_day_price},
                avg_reviews={self.avg_reviews},
                date={self.parsing_date}"""


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(
            db.Integer,
            db.ForeignKey("city.id", ondelete="CASCADE"),
            index=True
    )
    name = db.Column(db.String, unique=True)
    img_url = db.Column(db.String)
    address = db.Column(db.String)
    description = db.Column(db.String)
    link = db.Column(db.String)

    city = relationship("City", backref="attractions")

    def __repr__(self):
        return f"Attraction information (name={self.name}, link={link}"


class AirportId(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True)
    airport_id = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"Airport id = {self.airport_id}"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_outbound_id = db.Column(
            db.Integer,
            db.ForeignKey("airport_id.id", ondelete="CASCADE"),
            index=True
    )
    city_inbound_id = db.Column(
            db.Integer,
            db.ForeignKey("city.id", ondelete="CASCADE"),
            index=True
    )
    outbound_date = db.Column(db.String)  # dd/mm/YYYY
    inbound_date = db.Column(db.String)  # dd/mm/YYYY
    parsing_date = db.Column(db.String)
    price = db.Column(JSON, nullable=True)

    city_outbound = relationship("AirportId", backref="ticket")
    city_inbound = relationship("City", backref="ticket")

    def __repr__(self):
        return f""
