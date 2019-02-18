import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field is required.")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field is required.")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists!"}, 400

        user = UserModel(**data)
        user.upsert()

        return {"message": "User created successfuly."}, 201
