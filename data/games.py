import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    # content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

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

    comments = orm.relation("Comments", back_populates='game')

    def show_all(self):
        self.is_open = True

    def get_img_urls(self) -> dict:
        return {'Wide': self.image_urls.split(';')[0],
                'Tall': self.image_urls.split(';')[1]}

    def set_img_urls(self, urls: dict):
        self.image_urls = ';'.join([urls['Wide'], urls['Tall']])

    def set_published_date(self, date_str: str):
        y, m, d = list(map(int, date_str.split('-')))
        self.published_date = datetime.date(year=y, month=m, day=d)  # datetime

    def value_to_str(self, value, is_total=False):
        if isinstance(value, int) or isinstance(value, float):
            if round(value, 2) or is_total:
                return f"{value:0.2f} ₽"
            else:
                return "Бесплатно"
        raise TypeError("Неправильный тип для валюты!")

    def __repr__(self):
        return f'<Game_{self.id}> "{self.title}"'