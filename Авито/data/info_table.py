import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Info(SqlAlchemyBase, UserMixin):
    __tablename__ = "info"
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True, unique=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
