from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from models import User, Dish, Category, Order


@app.route('/')
def render_index():
    return render_template('main.html')


@app.route('/cart/')
def render_cart():
    return render_template('cart.html')


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



