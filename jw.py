from functools import wraps
from flask import request, jsonify
import jwt

from controllers.user_controller import SECRET_KEY
from db.user_db import UserDB


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY)
            user_db = UserDB()
            user_output = user_db.get_user_by_id(data["public_id"])
            if not user_output:
                return jsonify({"message": "Token is invalid !!"}), 401
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f(user_output, *args, **kwargs)

    return decorated
