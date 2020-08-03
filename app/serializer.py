from flask import Flask
from extension.extension import ma
from marshmallow import validate, fields
from app.model import User, Book, Car

class UserSchema(ma.SQLAlchemyAutoSchema):

    name = fields.String(required=True, validate=[validate.Length(min=2, max=30)])
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8, max=100)])

    class Meta:
        model = User
        include_fk = True
        load_instance = True
        include_relationships = True
    books = fields.Nested("BookSchema", many=True)
    cars = fields.Nested("CarSchema", many=True)

class UpdateUserSchema(ma.Schema):

    name = fields.String(validate=[validate.Length(min=2, max=30)])
    email = fields.Email()
    password = fields.String(validate=[validate.Length(min=8, max=100)])


class BookSchema(ma.SQLAlchemyAutoSchema):

    title = fields.String(required=True, validate=[validate.Length(min=2, max=40)])
    author = fields.String(required=True, validate=[validate.Length(min=2, max=50)])

    class Meta:
        model = Book
        include_fk = True
        load_instance = True
        exclude=("user_id",)
    user = fields.Nested("UserSchema", exclude=("password",))

class UpdateBookSchema(ma.Schema):

    title = fields.String(validate=[validate.Length(min=2, max=40)])
    author = fields.String(validate=[validate.Length(min=2, max=50)])

class CarSchema(ma.SQLAlchemyAutoSchema):

    model = fields.String(required=True, validate=[validate.Length(min=2, max=50)])
    color = fields.String(required=True, validate=[validate.Length(min=2, max=30)])

    class Meta:
        model = Car
        include_fk = True
        load_instance = True
        exclude = ("user_id",)
    user = fields.Nested("UserSchema", exclude=("password",))

class UpdateCarSchema(ma.Schema):

    model = fields.String(validate=[validate.Length(min=2, max=50)])
    color = fields.String(validate=[validate.Length(min=2, max=30)])
