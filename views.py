import datetime

from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from models import User, Dish, Category, Order
from forms import LoginForm, RegistrationForm, OrderForm


@app.errorhandler(404)
def render_not_found(error):
    """ 404 error custom handler """
    return 'Ничего не нашлось! Вот неудача, отправляйтесь на главную!\n<a href="/">Сюда!</a>'


@app.route('/')
def render_index():
    # проверка авторизации пользователя выгрузка данных из сессии для передачи в шаблон,
    # доработать в виде декоратора
    is_auth = False
    if session.get("user_id"):
        is_auth = True
    order_cart = session.get("cart", [])
    order_sum = session.get("sum", 0)
    categories = db.session.query(Category).all()
    return render_template('main.html',
                           categories=categories,
                           is_auth=is_auth,
                           order_cart=order_cart,
                           order_sum=order_sum)


@app.route('/categories/<category_id>')
def render_category(category_id):
    # проверка авторизации пользователя выгрузка данных из сессии для передачи в шаблон,
    # доработать в виде декоратора
    is_auth = False
    if session.get("user_id"):
        is_auth = True
    order_cart = session.get("cart", [])
    order_sum = session.get("sum", 0)
    # запрос из базы объекта выбранной категори блюд для пережачи в шаблон
    category = db.session.query(Category).get_or_404(category_id)
    return render_template('category.html',
                           is_auth=is_auth,
                           order_cart=order_cart,
                           order_sum=order_sum,
                           category=category)


@app.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    dish = db.session.query(Dish).get_or_404(int(dish_id))

    # append dish to cart
    order_cart = session.get("cart", [])
    order_cart.append(dish_id)
    session["cart"] = order_cart

    # append dishes price to order_sum
    order_sum = session.get("sum", 0)
    order_sum += dish.price
    session["sum"] = order_sum
    return redirect('/cart/')


@app.route('/cart/', methods=["GET", "POST"])
def render_cart():
    is_deleted = False
    if session.get("is_deleted"):
        is_deleted = True
        session["is_deleted"] = False
    # проверка авторизации пользователя, доработать в виде декоратора
    is_auth = False
    user_id = session.get("user_id")
    if user_id:
        is_auth = True
    order_cart = session.get("cart", [])
    order_sum = session.get("sum", 0)
    form = OrderForm()

    dishes = []
    for dish_id in order_cart:
        dish = db.session.query(Dish).get_or_404(dish_id)  # добавить проверку валидности id
        dishes.append(dish)

    if request.method == "POST":
        if form.validate_on_submit():
            mail = form.mail.data
            phone = form.phone.data
            address = form.address.data
            #проверка наличия и совпадения id и mail с данными из базы
            user = db.session.query(User).filter(db.and_(User.mail == mail, User.id == user_id)).first()
            if user:
                data = datetime.datetime.now()
                order = Order(data=data, total=order_sum, status=True,
                              email=mail, phone=phone, address=address, dishes=dishes, user=user, user_id=user.id)
                db.session.add(order)
                db.session.commit()
                session["cart"] = []
                session["sum"] = 0
                return redirect('/ordered/')
            else:
                # если пользователь не найден, то выводим ошибку
                form.mail.errors.append("введите корректную почту")
    return render_template('cart.html',
                           form=form,
                           is_auth=is_auth,
                           is_deleted=is_deleted,
                           order_cart=order_cart,
                           order_sum=order_sum,
                           dishes=dishes)


@app.route('/delete_from_card/<int:dish_id>')
def delete_from_card(dish_id):
    dish = db.session.query(Dish).get_or_404(int(dish_id))

    # delete dish from cart and sum
    order_cart = session.get("cart", [])
    order_sum = session.get("sum", 0)
    if dish_id in order_cart:
        order_cart.remove(dish_id)
        order_sum -= dish.price
    session["cart"] = order_cart
    session["sum"] = order_sum

    session["is_deleted"] = True
    return redirect('/cart/')


@app.route('/account/')
def render_account():
    # провекра авторизации пользователя, доработать в виде декоратора
    user_id = session.get("user_id")
    if not user_id:
        return redirect('/')
    order_cart = session.get("cart", [])
    order_sum = session.get("sum", 0)
    is_auth = True
    user = db.session.query(User).get_or_404(user_id)
    # добавить отображение регистрационных данных пользователя
    return render_template('account.html',
                           is_auth=is_auth,
                           order_cart=order_cart,
                           order_sum=order_sum,
                           orders=user.orders)


@app.route('/auth/', methods=["GET", "POST"])
def render_auth():
    if session.get("user_id"):
        return redirect('/')
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User).filter(User.mail == form.username.data).first()
            if not user:
                form.username.errors.append("Неверное имя")
            elif not user.password_valid(form.password.data):
                form.username.errors.append("Неверный пароль")
            else:
                session["user_id"] = user.id
                session["cart"] = session.get("cart", [])
                session["sum"] = session.get("sum", 0)
                return redirect('/')
    return render_template('auth.html', form=form)


@app.route('/register/', methods=["GET", "POST"])
def route_register():
    if session.get("user_id"):
        return redirect('/')
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not form.password.data == form.confirm_password.data:
                form.password.errors.append("Пароль не подтвержден")
            elif db.session.query(User).filter(User.mail == form.username.data).first():
                form.username.errors.append("Пользователь с такой почтой уже существует")
            else:
                user = User(mail=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return render_template('registration_done.html')
    return render_template('register.html', form=form)


@app.route('/logout/')
def route_logout():
    session.pop("user_id")
    session.pop("cart")
    session.pop("sum")
    return redirect('/')


@app.route('/ordered/')
def route_ordered():
    user_id = session.get("user_id")
    if not user_id:
        return redirect('/')
    return render_template('ordered.html')



