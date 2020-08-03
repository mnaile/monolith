from flask import Flask, request, jsonify
from app.model import User, Book, Car
from app.serializer import UserSchema, BookSchema, CarSchema, UpdateUserSchema, UpdateBookSchema,UpdateCarSchema
from app_init.app_factory import create_app
from marshmallow import ValidationError
from http import HTTPStatus
import os, requests

settings_name = os.getenv("settings")
app = create_app(settings_name)


# CREATE USERS

@app.route('/users', methods=["POST"])
def create_user():
    user_data = request.get_json()
    user = User.query.filter_by(email=user_data.get("email")).first()
    if user:
        return jsonify(msg="User exsist"),HTTPStatus.BAD_REQUEST
    try:
        user = UserSchema().load(user_data)
        user.set_password()
        user.save_db()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema().jsonify(user),HTTPStatus.OK

# CREATE BOOKS

@app.route('/users/<int:id>/books', methods=["POST"])
def create_books(id):
    user = User.query.get(id)
    if user:
        user_books = request.get_json()
        book_data = BookSchema().load(user_books)
        book_data.user_id = user.id
        book_data.save_db()
        return BookSchema().jsonify(book_data),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND


# CREATE CARS

@app.route('/users/<int:id>/cars', methods=["POST"])
def create_cars(id):
    user = User.query.get(id)
    if user:
        car = request.get_json()
        car_info = CarSchema().load(car)
        car_info.user_id = user.id 
        car_info.save_db()
        return CarSchema().jsonify(car_info),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

# GET USERS

@app.route('/users', methods=["GET"])
def get_all_users():
    user_info = User.query.all()
    return UserSchema(exclude=["password"]).jsonify(user_info, many=True),HTTPStatus.OK

@app.route('/users/<int:id>', methods=["GET"])
def get_users(id):
    user_info = User.query.get(id)
    if user_info:
        return UserSchema(exclude=["password"]).jsonify(user_info),HTTPStatus.OK
    return jsonify(msg="Not found")

# UPDATE USERS INFO

@app.route('/users/<int:id>', methods=["PUT"])
def update_users(id):
    user = User.query.get(id)
    if user:
        new_user = request.get_json()
        user_data = UpdateUserSchema().load(new_user)
        user.update_db(**user_data)
        return UserSchema().jsonify(new_user),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

# UPDATE BOOKS INFO

@app.route('/users/<int:user_id>/books/<int:id>', methods=["PUT"])
def update_books(user_id, id):
    user_books = Book.query.filter_by(user_id=user_id,id=id).first()
    if user_books:
        new_book = request.get_json()
        book_data = UpdateBookSchema().load(new_book)
        user_books.update_db(**book_data)
        return BookSchema().jsonify(new_book),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND


# UPDATE CARS INFO


@app.route('/users/<int:user_id>/cars/<int:id>', methods=["PUT"])
def update_car(user_id, id):
    user_cars = Car.query.filter_by(user_id=user_id, id=id).first()
    if user_cars:
        new_car = request.get_json()
        car_data = UpdateCarSchema().load(new_car)
        user_cars.update_db(**car_data)
        return CarSchema().jsonify(car_data),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

# DELETE USERS FROM DB

@app.route('/users/<int:id>', methods=["DELETE"])
def delete_users(id):
    user_data = User.query.get(id)
    if user_data:
        user_data.delete_from_db()
        return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND


# DELETE BOOKS FROM DB

@app.route('/users/<int:user_id>/books/<int:id>', methods=["DELETE"])
def delete_books(user_id, id):
    user_books = Book.query.filter_by(user_id=user_id, id=id).first()
    if user_books:
        user_books.delete_from_db()
        return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

# DELETE CARS FROM DB

@app.route('/users/<int:user_id>/cars/<int:id>', methods=["DELETE"])
def delete_cars(user_id, id):
    user_cars = Car.query.filter_by(user_id=user_id, id=id).first()
    if user_cars:
        user_cars.delete_from_db()
        return jsonify(msg="OK"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND


