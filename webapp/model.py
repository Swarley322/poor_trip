from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Hotel(db.Model):
    __tablename__ = 'Hotels'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    name = db.Column(db.String)
    week_price = db.Column(db.String, nullable=True)
    living_date = db.Column(db.String)
    hotel_link = db.Column(db.String)
    parsing_date = db.Column(db.String)
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    stars = db.Column(db.String, nullable=True)
    distance_from_center = db.Column(db.String)
    img_url = db.Column(db.String)

    def __repr__(self):
        return f"""Hotel(city={city}, name={name}, week_price={week_price},
                  living_date={living_date}, hotel_link={hotel_link},
                  parsing_date={parsing_date}, rating={rating},
                  reviews={reviews}, stars={stars},
                  distance_from_center={distance_from_center},
                  img_url={img_url}"""


class AvgPriceReviews(db.Model):
    __tablename__ = "City"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    avg_reviews = db.Column(db.Integer)
    avg_price = db.Column(db.Integer)
    date = db.Column(db.String)

    def __repr__(self):
        return f"""AvgReviews(city={city},
                avg_price={avg_price},
                avg_reviews={avg_reviews},
                date={date}"""