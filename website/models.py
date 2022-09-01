from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(150))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    team = db.Column(db.String(150))
    company_id= db.Column(db.Integer,db.ForeignKey('company.id'))
    tickets = db.relationship('Ticket')

class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    company_name=db.Column(db.String(150))
    users = db.relationship('User')

