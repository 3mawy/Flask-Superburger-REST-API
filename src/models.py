from sqlalchemy import (
    Column, String, Integer,
    Boolean, create_engine, ForeignKey
)
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import os

default_path = 'postgres://postgres:0153@localhost:5432/capstone'

database_path = os.getenv('DATABASE_URL', default_path)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Association tables
'''
menu_items_sizes = db.Table(
    'menu_items_sizes',
    db.Column(
        'item_id',
        Integer,
        ForeignKey('menu_items.id'),
        primary_key=True),
    db.Column(
        'size_id',
        Integer,
        ForeignKey('sizes.id'),
        primary_key=True))


def update():
    db.session.commit()


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    active = Column(Boolean)

    category = relationship("Category", back_populates="menu_items")
    sizes = relationship(
        "Size",
        secondary=menu_items_sizes,
        back_populates="menu_items")

    # def __init__(self, name, catchphrase=""):
    #     self.name = name
    #     self.catchphrase = catchphrase

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category_id,
            'description': self.description,
            'ingredients': self.ingredients,
            'active': self.active
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    menu_items = relationship("MenuItem", back_populates="category")

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Size(db.Model):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    menu_items = relationship(
        "MenuItem",
        secondary=menu_items_sizes,
        back_populates="sizes")

    def format(self):
        return {
            'id': self.id,
            'name': self.name}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
