from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, number_range


class FilterForm(FlaskForm):
    # categories, price, date, rating, id
    choices = [(1, 'Популярности: сначала больше'), (2, 'Популярности: сначала меньше'),
               (3, 'Цене: сначала больше'), (4, 'Цене: сначала меньше'),
               (5, 'Дате публикации: сначала позже'), (6, 'Дате публикации: сначала раньше')]
    select = SelectField(label="Сортировать по:", coerce=int, choices=choices)
    price_start = IntegerField("Цена: от ", validators=[number_range(0, 10_000)], default=0)
    price_end = IntegerField(" до ", validators=[number_range(0, 10_000)], default=10_000)
    submit = SubmitField('Поиск')


class FindForm(FlaskForm):
    keywords = StringField("Ключевые слова (нежелательно писать более 1 слова)", validators=[length(max=32)])
    result_count = IntegerField("Максимальное кол-во результатов (не более 5)",
                                validators=[DataRequired(), number_range(1, 5)], default=3)
    submit = SubmitField('Поиск')
