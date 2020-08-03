from flask import Flask
from extension.extension import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__="user"

    # relation
    books = db.relationship('Book', back_populates='users')
    cars = db.relationship('Car', back_populates='users')
    
    # information
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = True)
    email = db.Column(db.String(), nullable = True)
    password = db.Column(db.String(), nullable = True)

    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()


class Book(db.Model):
    __tablename__ = "book"

    # relation
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete = 'CASCADE'))
    users = db.relationship('User',back_populates='books')

    # information
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable = True)
    author = db.Column(db.String(), nullable = True)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()


class Car(db.Model):
    __tablename__ = "car"

    # relation
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete = 'CASCADE'))
    users = db.relationship('User', back_populates='cars')

    # information
    id = db.Column(db.Integer(), primary_key = True)
    model = db.Column(db.String(), nullable =True)
    color = db.Column(db.String(), nullable = True)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()