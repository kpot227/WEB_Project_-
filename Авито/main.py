import os

from flask import Flask, render_template, redirect, request, abort
from werkzeug.utils import secure_filename

from data import db_session
from data.info_table import Info
from data.product_table import Product
from forms.info import LoginForm
from forms.info_two import RegisterForm
from forms.form_product import ProductForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Info).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    product_table = session.query(Product).all()
    return render_template("index.html", title='Главная', slides=product_table)


@app.route("/lk/<int:id>", methods=['GET', 'POST'])
@login_required
def lk(id):
    form = RegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(Info).filter(Info.id == id).first()
        if user:
            form.name.data = user.name
            form.number.data = user.number
            form.password.data = user.password
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Info).filter(Info.id == id).first()
        if user:
            user.name = form.name.data
            user.number = form.number.data
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html', title='Личный кабинет', form=form)


@app.route("/out", methods=['GET', 'POST'])
def out():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Info).filter(Info.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('LK.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('LK.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Info).filter(Info.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Info(
            name=form.name.data,
            number=form.number.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/out')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/prods")
def prods():
    db_sess = db_session.create_session()
    prods = db_sess.query(Product).all()
    return render_template("Prod's.html", title='Товары', prods=prods)


@app.route("/product/<int:id>")
def product(id):
    db_sess = db_session.create_session()
    prod = db_sess.query(Product).filter(Product.id == id).first()
    user = db_sess.query(Info).filter(Info.id == prod.name_id).first()
    return render_template("product_card.html", title=prod.title, prod=prod, user=user, src=prod.img)


@app.route("/product_form", methods=['GET', 'POST'])
def product_form():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        f = form.img.data
        filename = secure_filename(f.filename)
        f.save(f'static/img/{filename}')
        prod = Product(
            title=form.title.data,
            about_product=form.about_product.data,
            price=form.price.data,
            chat=form.chat.data,
            img=f'static/img/{filename}',
            name_id=db_sess.query(Info).filter(Info.id == current_user.id).first().id
        )
        db_sess.add(prod)
        db_sess.commit()
        return redirect('/')
    return render_template('product_form.html', title='Оформление товара', form=form)


@app.route('/user_prod')
def user_prod():
    db_sess = db_session.create_session()
    prods = db_sess.query(Product).filter(Product.name_id == current_user.id).all()
    return render_template("Prod's.html", title='Ваши товары', prods=prods)


@app.route('/pokupka/<int:id>')
def pokupka(id):
    db_sess = db_session.create_session()
    prods = db_sess.query(Product).filter(Product.id == id).first()
    db_sess.delete(prods)
    db_sess.commit()
    return redirect('/')


def main():
    db_session.global_init("db/info.db")
    app.run()


if __name__ == '__main__':
    main()
