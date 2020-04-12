from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired


class StartForm(FlaskForm):
    city = StringField('City outbound', render_kw={"class": "form-control"})
    checkin = DateTimeField('Checkin Date (mm/dd/yyyy)', format='%d/%m/%Y',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    dt = DateTimeField('Pick a Date', format="%m/%d/%Y")
    checkout = DateTimeField('Chekout Date (mm/dd/yyyy)', format='%d/%m/%Y',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    money = IntegerField('Money',
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('GO', render_kw={"class": "btn btn-primary"})
