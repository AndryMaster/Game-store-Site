from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField, TextAreaField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, length, EqualTo, number_range


class SettingsForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), length(min=5, max=25)])
    new_password = PasswordField('Ноывй пароль', validators=[EqualTo('new_password_again'), length(min=0, max=64)])
    new_password_again = PasswordField('Повторите пароль')
    about = TextAreaField("Немного о себе", validators=[length(max=256)])
    old_password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64)])
    submit = SubmitField('Подтвердить изменения')


class AddBalanceForm(FlaskForm):
    password = PasswordField('Подтвердите действие паролем:', validators=[DataRequired()])
    add_balance = FloatField('Пополнить счёт на сумму (₽):', validators=[DataRequired(), number_range(min=0, max=10_000,
                             message='Вы ввели отрицательную или слишком большую (более 10 000) сумму')])
    submit = SubmitField('Пополнить')


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), length(min=4, max=25)])
    email = EmailField('Почта', validators=[DataRequired(), length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64), EqualTo('password_again')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), length(min=5, max=64)])
    about = TextAreaField("Немного о себе", validators=[length(max=256)])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=5, max=64)])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')
