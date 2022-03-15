import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(64), index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    balance = sqlalchemy.Column(sqlalchemy.Float, default=0.0)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_favorites = sqlalchemy.Column(sqlalchemy.String(), nullable=True)   # ++orm.relationship
    user_basket = sqlalchemy.Column(sqlalchemy.String(), nullable=True)      # ++orm.relationship
    user_library = sqlalchemy.Column(sqlalchemy.String(), nullable=True)     # ++orm.relationship

    games = orm.relation("Games", back_populates='user')
    comments = orm.relationship("Comments", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_favorites(self, favorites: list):
        self.user_favorites = ';'.join(favorites)

    def get_favorites(self):
        return self.user_favorites.split(';')

    def set_basket(self, basket: list):
        self.user_basket = ';'.join(basket)

    def get_basket(self):
        return self.user_basket.split(';')

    def set_library(self, library: list):
        self.user_library = ';'.join(library)

    def get_library(self):
        return self.user_library.split(';')
