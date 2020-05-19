from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    fresh_jwt_required
)
from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank."
ITEM_NOT_FOUND = 'Item not found'
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred inserting the item!."
ITEM_DELETED = "Item deleted."


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help=BLANK_ERROR.format('price')
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help=BLANK_ERROR.format('store_id')
                        )

    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):

        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        data = cls.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item.json(), 201    

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        # claims = get_jwt_claims() # get the data from request, interpret it and extract claims
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required!'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED }
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def put(cls, name: str):
        data = cls.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': [item.json() for item in ItemModel.find_all()]}, 200


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
