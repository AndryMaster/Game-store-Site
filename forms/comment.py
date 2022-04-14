from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length, number_range


class CreateComment(FlaskForm):
    rating = IntegerField("Оценка игры (от 1 до 10):", validators=[DataRequired(), number_range(1, 10)])
    content = TextAreaField("Описание игры:", validators=[length(max=256)])
    submit = SubmitField("Опубликовать")
