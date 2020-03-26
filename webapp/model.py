from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import flask


db = SQLAlchemy()


class Hotel(db.Model):
    __tablename__ = 'Hotels'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String, db.ForeignKey("City.id"))
    name = db.Column(db.String)
    week_price = db.Column(db.Integer, nullable=True)
    checkin_date = db.Column(db.String)
    checkout_date = db.Column(db.String)
    hotel_link = db.Column(db.String)
    parsing_date = db.Column(db.String)
    week_number = db.Column(db.Integer)
    rating = db.Column(db.Float, nullable=True)
    reviews = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.String, nullable=True)
    distance_from_center = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=True)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"Hotel(city={self.city_id}, name={self.name}, week_price={self.week_price}"


class AvgPriceReviews(db.Model):
    __tablename__ = "AvgPricesReviews"
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String, db.ForeignKey("City.id"))
    avg_reviews = db.Column(db.Integer)
    avg_week_price = db.Column(db.Integer)
    avg_day_price = db.Column(db.Integer)
    parsing_date = db.Column(db.String)
    week_number = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"""AvgReviews(city={self.city},
                avg_price={self.avg_price},
                avg_reviews={self.avg_reviews},
                date={self.date}"""


class City(db.Model):
    __tablename__ = "City"
    id = db.Column(db.Integer, primary_key=True)
    eng_part_of_the_world = db.Column(db.String)
    ru_part_of_the_world = db.Column(db.String)
    eng_name = db.Column(db.String, unique=True)
    ru_name = db.Column(db.String, unique=True)
    eng_country = db.Column(db.String)
    ru_country = db.Column(db.String)
    city_img = db.Column(db.String, nullable=True)
    hotels = db.relationship("Hotel", backref="city")
    avginfo = db.relationship("AvgPriceReviews", backref="city")

    def __repr__(self):
        return f"""City information (name={self.ru_name},
                country={self.ru_country},
                part_of_the_world={self.ru_part_of_the_world}"""
