import sqlalchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField, SubmitField, FloatField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Название продукта', validators=[DataRequired()])
    about_product = StringField('Описание продукта', validators=[DataRequired()])
    price = FloatField('Стоимость', validators=[DataRequired()])
    chat = StringField('Чат', validators=[DataRequired()])
    img = FileField('Загрузить фото', validators=[FileRequired()])
    submit = SubmitField('Сохранить')
