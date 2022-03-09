from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя (логин)', validators=[DataRequired(), length(min=4, max=25)])
    email = EmailField('Почта', validators=[DataRequired(), length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64), EqualTo('password_again')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), length(min=5, max=64)])
    about = TextAreaField("Немного о себе")
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64)])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')
