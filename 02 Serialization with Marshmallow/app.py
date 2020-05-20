from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from ma import ma

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # propagate jwt exceptions
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = 'ashish' # app.config['JWT_SECRET_KEY]
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(error):
    return jsonify(error.messages), 400


jwt = JWTManager(app)


# The following decorator is going to modify the function
# below `add_claims_to_jwt` and going to link it up with JWT manager
# which as a result is linked to app.
# @jwt.user_claims_loader
# def add_claims_to_jwt(identity): # parameter must be identity
#     """
#     When ever we create a new access token,
#     we're gonna run this function to see
#     if we should add extra data to the jwt.
#     """
#     if identity == 1: # read from database
#         return {'is_admin': True}
#     return {'is_admin': False}
#


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format.
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'eror': 'token_expired'
    }), 401


# This method will check if a toke is blacklisted,
# and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# we have to keep the argument here, since its'
# passed in by the caller internally
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    })


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)