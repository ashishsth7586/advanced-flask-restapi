from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required, 
    fresh_jwt_required
)
from schemas.item import ItemSchema
from models.item import ItemModel
from libs.strings import gettext


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': gettext("item_not_found")}, 404

    @classmethod
    @jwt_required
    def post(cls, name: str):

        if ItemModel.find_by_name(name):
            return {"message": gettext("item_name_exists").format(name)}, 400

        item_json = request.get_json()  # price and store id
        item_json["name"] = name
        item = item_schema.load(item_json)
        item_model = ItemModel(**item)
        try:
            item_model.save_to_db()
        except:
            return {"message": gettext("item_error_inserting")}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        # claims = get_jwt_claims() # get the data from request, interpret it and extract claims
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required!'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": gettext("item_deleted") }
        return {"message": gettext("item_not_found")}, 404

    @classmethod
    @jwt_required
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            item = item_schema.load(item_json)
        item.save_to_db()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200


# class ItemList(Resource):
#     @jwt_optional
#     def get(self):
#         """
#         Here we get the JWT identity, and then if the user is logged in
#         (we are able to get an identity) we return the entire item list.
#         Otherwise we just return item names.
#         This could be done with e.g. see orders that have been placed,
#         but not see details about the orders unless the user has logged in.
#         """
#         user_id = get_jwt_identity()
#         items = [item.json() for item in ItemModel.find_all()]
#         if user_id:
#             return {'items': items}, 200
#         return {
#             'items': [item['name'] for item in items],
#             'message': 'More data available if you log in'
#             }
