import csv

from app import app, db
from models import Migrate, User, Dish, Category, Order


dishes = db.session.query(Dish).all()
for d in dishes:
    print(d.id, d.title, d.price)
