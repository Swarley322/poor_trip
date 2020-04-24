from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class StartForm(FlaskForm):
    city_outbound = StringField('City outbound', render_kw={"class": "form-control"})
    outbound_date = DateField(
                        'Outbound date',
                        validators=[DataRequired()],
                        render_kw={"class": "form-control", "type": "date"}
    )
    inbound_date = DateField(
                'Inbound date',
                validators=[DataRequired()],
                render_kw={"class": "form-control", "type": "date"}
    )
    money = IntegerField('Money',
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('GO', render_kw={"class": "btn btn-primary"})
