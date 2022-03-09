from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length, number_range


# class RegForm(FlaskForm):
#     name = StringField('Имя пользователя (логин)', validators=[DataRequired(), length(min=4, max=25)])
#     email = EmailField('Почта', validators=[DataRequired(), length(max=64)])
#     password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64), EqualTo('password_again')])
#     password_again = PasswordField('Повторите пароль', validators=[DataRequired(), length(min=5, max=64)])
#     about = TextAreaField("Немного о себе")
#     remember_me = BooleanField('Запомнить меня', default=True)
#     submit = SubmitField('Войти')


class CreateComment(FlaskForm):
    rating = IntegerField("Оценка игры (от 1 до 10)", validators=[DataRequired(), number_range(1, 10)])
    content = TextAreaField("Описание", validators=[length(max=256)])
    submit = SubmitField("Опубликовать")
