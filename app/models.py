from app import db
from sqlalchemy import Column, String, Integer, Text
from flask_login import UserMixin
from app import login_manager


class user(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200))
    password = Column(String(200))
    email = Column(String(200))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class admin(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(200))
    password = Column(String(200))

    def __init__(self, account, password):
        self.account = account
        self.password = password


class product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_product = Column(String(200))
    price = Column(Integer)
    images = Column(String(200))

    def __init__(self, name_product, price, images):
        self.name_product = name_product
        self.price = price
        self.images = images


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))
