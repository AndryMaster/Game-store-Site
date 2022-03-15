import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"))
    game = orm.relation('Games')

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    published_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def update_date(self):
        self.published_date = datetime.datetime.now()
