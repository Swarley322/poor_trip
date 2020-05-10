from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class StartForm(FlaskForm):
    city_outbound = StringField('Город отправления', render_kw={
                                        "class": "typeahead tt-query",
                                        "autocomplete": "off",
                                        "spellcheck": "false",
                                        "type": "text"
    })
    outbound_date = DateField(
                        'Дата отправления',
                        validators=[DataRequired()],
                        render_kw={"class": "form-control", "type": "date"}
    )
    inbound_date = DateField(
                'Дата возврата',
                validators=[DataRequired()],
                render_kw={"class": "form-control", "type": "date"}
    )
    money = IntegerField('Сумма денег ₽',
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})

    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Поиск', render_kw={
                    "class": "btn btn-primary",
                    "id": "btnSubmit",
                    "onclick": "this.classList.toggle('running')",
                    "id": "btnSubmit",
    })
