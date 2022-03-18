from . import users
from . import games
from . import comments

import datetime


class Model:
    @staticmethod
    def date_to_str(date: datetime.datetime, str_month=False):
        if isinstance(date, datetime.datetime):
            if not str_month:
                if date.hour or date.minute:
                    return date.strftime("%Y-%m-%d %H:%M")
                return date.strftime("%Y-%m-%d")
            return date.strftime("%d %B %Y ")
        # raise TypeError("Неправильный тип для даты!")

    @staticmethod
    def value_to_str(value, is_total=False):
        if isinstance(value, int) or isinstance(value, float):
            if round(value, 2) or is_total:
                return f"{value:0.2f} ₽"
            return "Бесплатно"
        # raise TypeError("Неправильный тип для валюты!")
