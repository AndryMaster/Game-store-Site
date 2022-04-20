# -*- coding: utf-8 -*-
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .model import Model


class Games(SqlAlchemyBase, SerializerMixin, Model):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    original_price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    discount_price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    image_urls = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    placement_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    published_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    developer_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    is_open = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    comments = orm.relationship("Comments", back_populates='game')

    def show_all(self):
        self.is_open = True
        self.placement_date = datetime.datetime.now()

    def get_img_urls(self) -> dict:
        return {'Wide': self.image_urls.split(';')[0],
                'Tall': self.image_urls.split(';')[1]}

    def set_img_urls(self, urls: dict):
        self.image_urls = ';'.join([urls['Wide'], urls['Tall']])

    def set_published_date(self, date_str: str):
        y, m, d = list(map(int, date_str.split('-')))
        self.published_date = datetime.datetime(year=y, month=m, day=d)

    def add_rating(self, delta_rating):
        if self.is_open:
            self.rating += delta_rating

    # @staticmethod
    # def value_to_str(value, is_total=False):
    #     if isinstance(value, int) or isinstance(value, float):
    #         if round(value, 2) or is_total:
    #             return f"{value:0.2f} ₽"
    #         else:
    #             return "Бесплатно"
    #     # raise TypeError("Неправильный тип для валюты!")

    def __repr__(self):
        return f'<Game_{self.id}> "{self.title}"'
