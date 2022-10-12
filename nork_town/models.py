from email.policy import default
from flask import render_template, session
from nork_town import db
from flask_login import UserMixin, current_user
from datetime import datetime
import pytz
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def houres():
    houres = datetime.now(pytz.utc)
    return houres

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=True, default='Perfil.png')
    registration_date = db.Column(db.DateTime, nullable=False, default=houres())
    
    def date_registration(self):
        self.date = self.registration_date
        format_date = self.date.strftime("%d/%m/%Y")
        return format_date


class Peoples(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=True)
    profile_picture = db.Column(db.String, nullable=True, default='null')
    registration_date = db.Column(db.DateTime, nullable=False, default=houres())

    cars = db.relationship("Cars", back_populates="user", lazy=True)
    
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        
    def __repr__(self):
        return str(self)

    def __str__(self):
        self.name_id = f"{self.id} - {self.name}"
        return self.name_id

    def date_registration(self):
        self.date = self.registration_date
        format_date = self.date.strftime("%d/%m/%Y")
        return format_date

    def count_cars(self):
        self.cont = len(self.cars)
        return self.cont

    def count_cars_for_user(self):
        self.cont = len(self.cars)
        return self.cont

    def oportunity(self):
        cont = len(self.cars)
        if self.cont < 3:
            self.oportunidade = 'Oporunidade'
            return self.oportunidade
        else:
            pass

    def name_cars(self):
        self.cont = self.cars
        return list(self.cont)


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, nullable=False)
    color_car = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.DateTime,  nullable=False, default=houres())

    #relation user
    id_user = db.Column(db.Integer, db.ForeignKey('peoples.id'), nullable=False)
    user = db.relationship("Peoples", back_populates="cars", lazy=True)

    
    def __str__(self):
        self.model = f"{self.model}"
        return self.model

    def date_registration(self):
        self.date = self.publication_date
        format_date = self.date.strftime("%d/%m/%Y")
        return format_date

    def name_cars(self):
            self.model = self.model
            return self.model


db.create_all()
db.session.commit()

name = 'admin'
phone_number = '551100000000'
email = 'admin@example.com'
password = '123456'

user = User(name=name, phone_number=phone_number, email=email, password=password)
db.session.add(user)
db.session.commit()