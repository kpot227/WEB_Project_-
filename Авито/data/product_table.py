import sqlalchemy
from flask import Flask
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = "product"
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, primary_key=True, autoincrement=True)
    chat = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about_product = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True, unique=True)
    title = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True, unique=True)
    name_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('info.id'), nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, unique=True)
    info = orm.relationship('Info')
