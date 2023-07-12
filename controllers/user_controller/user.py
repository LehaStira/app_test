from datetime import timedelta, datetime

import jwt
from flask import Blueprint, make_response, request, jsonify, abort
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.user_controller import EXPIRING_TIME, SECRET_KEY
from db.user_db import UserDB
from exceptions import UniqueException
from jw import token_required
from models.user_model import UserModel, UserModelOutput
from schemas import user_schema

user_routes = Blueprint("user_routes", __name__)


class UserController:
    @staticmethod
    @user_routes.route("/register", methods=["POST"])
    def register():
        # creates a dictionary of the form data
        user_data = None
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            make_response(err.messages, 400)

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
        )

        user_db = UserDB()
        output_user = None
        try:
            output_user = user_db.register_user(user)
        except UniqueException as err:  # not unique username or password
            abort(400, "Email or username must be unique!")
        return make_response(output_user.to_json(), 201)

    # route for logging user in
    @staticmethod
    @user_routes.route("/login", methods=["POST"])
    def login():
        # creates dictionary of form data
        user_data = None
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            make_response(err.messages, 400)

        user = UserModel(
            username=user_data["username"],
            password=user_data["password"],
            email=user_data["email"],
        )

        user_db = UserDB()

        output_user = user_db.login_user(user)
        if not output_user:
            # returns 401 if user does not exist
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
            )
        if check_password_hash(password=user.password, pwhash=output_user.password):
            # generates the JWT Token
            token = jwt.encode(
                {
                    "public_id": output_user.user_id,
                    "exp": datetime.utcnow() + timedelta(minutes=EXPIRING_TIME),
                },
                SECRET_KEY,
            )

            return make_response(jsonify({"token": token.decode("UTF-8")}), 201)
        # returns 403 if password is wrong
        return make_response(
            "Could not verify",
            403,
            {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
        )

    @staticmethod
    @user_routes.route("/users/<user_id>", methods=["PUT"])
    @token_required
    def update_user(user: UserModelOutput, user_id: str):
        # creates a dictionary of the form data
        user_data = None
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            make_response(err.messages, 400)

        update_user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
        )

        user_db = UserDB()
        output_user = None
        try:
            output_user = user_db.update_user(user_id=user_id, user=update_user)
        except UniqueException as err:  # not unique username or password
            abort(400, "Email or username must be unique!")
        return make_response(output_user.to_json(), 201)

    @staticmethod
    @user_routes.route("/users", methods=["GET"])
    def get_users():
        # creates a dictionary of the form data
        user_db = UserDB()
        list_users = user_db.get_all_users()
        json_data = [obj.to_json() for obj in list_users]
        return make_response(jsonify(json_data), 200)

    @staticmethod
    @user_routes.route("/users/<user_id>", methods=["GET"])
    def get_users_by_id(user_id: str):
        # creates a dictionary of the form data
        user_db = UserDB()
        user = user_db.get_user_by_id(user_id=user_id)
        return make_response(user.to_json(), 200)

    @staticmethod
    @user_routes.route("/users/<user_id>", methods=["DELETE"])
    @token_required
    def delete_user(user: UserModelOutput, user_id: str):
        # creates a dictionary of the form data

        user_db = UserDB()
        if user_db.delete_user_by_id(user_id=user_id):
            message = {
                "message": f"User with user_id = {user_id} was successfully deleted"
            }
            return make_response(message, 200)
