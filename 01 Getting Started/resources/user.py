import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from blacklist import BLACKLIST

BLANK_ERROR = "'{}' cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found"
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid Credentials!"
USER_LOGGED_OUT = "User {} successfully logged out."

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="Username cannot be left blank.")
_user_parser.add_argument('password', type=str, required=True, help="Password cannot be left blank.")


class UserRegister(Resource):
    @classmethod
    def post(cls):

        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": USER_ALREADY_EXISTS.format(data['username'])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    """
    This resource can be useful when testing our flask app.
    """
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()    # returns a dict

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']  # jwt id, a unique identifier for a JWT
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

