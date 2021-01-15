from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from models import User, Dish, Category, Order


@app.errorhandler(404)
def render_not_found(error):
    """ 404 error custom handler """
    return 'Ничего не нашлось! Вот неудача, отправляйтесь на главную!\n<a href="/">TINYSTEPS</a>'


@app.route('/')
def render_index():
    # проверка авторизации пользователя, доработать в виде декоратора
    is_auth = False
    if session.get("user_id"):
        is_auth = True
    if not session.get("cart"):
        session["cart"] = []
    dishes_amount = len(session.get("cart"))
    dishes_sum = 0
    for dish_id in session.get("cart"):
        dishes_sum += db.session.query(Dish).get(dish_id).price
    categories = db.session.query(Category).all()
    return render_template('main.html',
                           categories=categories,
                           is_auth=is_auth,
                           dishes_amount=dishes_amount,
                           dishes_sum=dishes_sum)


@app.route('/addtocart/<int:dish_id>')
def add_to_cart(dish_id):

    dish = db.session.query(Dish).get_or_404(int(dish_id))
    if not session.get("cart"):
        session["cart"] = []
    session["cart"].append(dish_id)
    return redirect('/cart/')


@app.route('/cart/')
def render_cart():
    # проверка авторизации пользователя, доработать в виде декоратора
    is_auth = False
    dishes_sum = 0
    if session.get("user_id"):
        is_auth = True
    if not session.get("cart"):
        session["cart"] = []
    dishes_amount = len(session.get("cart"))
    dishes_sum = 0
    dishes = []
    for dish_id in session.get("cart"):
        dish = db.session.query(Dish).get(dish_id)  # добавить проверку валидности id
        dishes.append(dish)
        dishes_sum += dish.price
    return render_template('cart.html',
                           is_auth=is_auth,
                           dishes_amount=dishes_amount,
                           dishes_sum=dishes_sum)


@app.route('/account/')
def render_account():
    return render_template('account.html')


@app.route('/auth/')
def render_auth():
    return render_template('auth.html')


@app.route('/register/')
def route_register():
    return render_template('register.html')


@app.route('/login/')
def route_login():
    return render_template('login.html')


@app.route('/logout/')
def route_logout():
    return 'logout'


@app.route('/ordered/')
def route_ordered():
    return render_template('ordered.html')



