import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from .model import Model


class User(SqlAlchemyBase, UserMixin, SerializerMixin, Model):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(64), index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    balance = sqlalchemy.Column(sqlalchemy.Float, default=0.0)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_favorites = sqlalchemy.Column(sqlalchemy.String(), default='')   # ++orm.relationship
    user_basket = sqlalchemy.Column(sqlalchemy.String(), default='')      # ++orm.relationship
    user_library = sqlalchemy.Column(sqlalchemy.String(), default='')     # ++orm.relationship

    games = orm.relation("Games", back_populates='user')
    comments = orm.relationship("Comments", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def add_balance(self, money):
        self.balance += money

    # favorites
    def set_favorites(self, favorites: list):
        self.user_favorites = ';'.join([str(item_id) for item_id in set(favorites)])

    def get_favorites(self) -> list:
        return [int(item_id) for item_id in self.user_favorites.split(';') if item_id]

    def add_favorites(self, item_id):
        favorites = self.get_favorites()
        favorites.append(item_id)
        self.set_favorites(favorites)

    def del_favorites(self, item_id):
        favorites = self.get_favorites()
        if item_id in favorites:
            favorites.remove(item_id)
            self.set_favorites(favorites)

    # basket
    def set_basket(self, basket: list):
        self.user_basket = ';'.join([str(item_id) for item_id in set(basket)])

    def get_basket(self) -> list:
        return [int(item_id) for item_id in self.user_basket.split(';') if item_id]

    def add_basket(self, item_id):
        basket = self.get_basket()
        basket.append(item_id)
        self.set_basket(basket)

    def del_basket(self, item_id):
        basket = self.get_basket()
        if item_id in basket:
            basket.remove(item_id)
            self.set_basket(basket)

    # library
    def set_library(self, library: list):
        self.user_library = ';'.join([str(item_id) for item_id in set(library)])

    def get_library(self) -> list:
        return [int(item_id) for item_id in self.user_library.split(';') if item_id]

    def add_library(self, item_id):
        library = self.get_library()
        library.append(item_id)
        self.set_library(library)

    # def del_library(self, item_id):
    #     library = self.get_library()
    #     if item_id in library:
    #         library.remove(item_id)
    #         self.set_library(library)
