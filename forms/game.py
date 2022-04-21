# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, number_range

choices = [(1, 'Популярности: с начала больше'), (2, 'Популярности: с начала меньше'),
           (3, 'Цене: с начала больше'), (4, 'Цене: с начала меньше'),
           (5, 'Дате публикации: с начала позже'), (6, 'Дате публикации: с начала раньше'),
           (7, 'По алфавиту: с конца'), (8, 'По алфавиту: с начала')]


class FilterForm(FlaskForm):
    search_text = StringField("Поиск по названию:", validators=[length(max=20)])
    select = SelectField(label="Сортировать по:", coerce=int, choices=choices)
    price_start = IntegerField("Цена: от ", validators=[number_range(0, 10000)], default=0)
    price_end = IntegerField(" до ", validators=[number_range(0, 10000)], default=10000)
    submit = SubmitField('Поиск')


class FindForm(FlaskForm):
    keywords = StringField("Ключевое слово:", validators=[length(max=10)])
    result_count = IntegerField("Максимальное кол-во игр:",
                                validators=[DataRequired(), number_range(1, 5)], default=3)
    choices = [(1, 'Маленький'), (2, 'Средний'), (3, 'Большой')]
    select = SelectField(label="Диапазон поиска:", coerce=int, default=2, choices=choices)
    submit = SubmitField('Поиск')
