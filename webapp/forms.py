from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired


class Form(Form):
    city = StringField('City', validators=[DataRequired()])
    checkin = DateTimeField('Checkin Date (mm/dd/yyyy)', format='%d/%m/%Y', validators=[DataRequired()])
    checkout = DateTimeField('Chekout Date (mm/dd/yyyy)', format='%d/%m/%Y', validators=[DataRequired()])
    money = IntegerField('Money', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('GO')
