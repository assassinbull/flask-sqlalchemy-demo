from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

MSG_NO_ITEM_FOUND_WITH_NAME = "No item found with name '{}'!"
MSG_ITEM_WITH_NAME_EXISTS = "The item with name '{}' already exists!"
MSG_ITEM_DELETED = "The item with name '{}' is deleted."


def message_object(message):
    return {"message": message}


class Items(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.get_items()

        # return {"items": [x.json() for x in items]}, 200
        return {"items": list(map(lambda x: x.json(), items))}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field is required.")
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return {"item": item.json()}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return message_object(MSG_ITEM_WITH_NAME_EXISTS.format(name)), 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)

        try:
            new_item.upsert()
        except:
            return {"message": "An error occurred while inserting an item!"}, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        try:
            item.delete()
        except:
            return {"message": "An error occurred while deleting an item!"}, 500

        return message_object(MSG_ITEM_DELETED.format(name)), 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        try:
            item.upsert()
        except:
            return {"message": "An error occurred while updating an item!"}, 500

        return item.json(), 200
