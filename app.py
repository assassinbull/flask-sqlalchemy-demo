from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Items, Item
from resources.store import Stores, Store
from security import authenticate, identity as identity_function
from resources.user import UserRegister
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "erdemjwt"
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
jwt = JWT(app, authenticate, identity_function)  # /auth


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token':
            access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), 400  # error.status_code


api.add_resource(Items, "/items")
api.add_resource(Item, "/items/<name>")
api.add_resource(Stores, "/stores")
api.add_resource(Store, "/stores/<name>")
api.add_resource(UserRegister, "/register")

db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
