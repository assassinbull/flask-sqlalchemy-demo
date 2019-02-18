from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.store import StoreModel

MSG_NO_STORE_FOUND_WITH_NAME = "No store found with name '{}'!"
MSG_STORE_WITH_NAME_EXISTS = "The store with name '{}' already exists!"
MSG_STORE_DELETED = "The store with name '{}' is deleted."


def message_object(message):
    return {"message": message}


class Stores(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.get_stores()

        return {"stores": list(map(lambda x: x.json(), stores))}, 200


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        return {"store": store.json()}, 200 if store else 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return message_object(MSG_STORE_WITH_NAME_EXISTS.format(name)), 400

        new_store = StoreModel(name)

        try:
            new_store.upsert()
        except:
            return {"message": "An error occurred while inserting an store!"}, 500

        return new_store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        try:
            store.delete()
        except:
            return {"message": "An error occurred while deleting an store!"}, 500

        return message_object(MSG_STORE_DELETED.format(name)), 200
