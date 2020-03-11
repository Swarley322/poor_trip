from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('GO')