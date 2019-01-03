import traceback
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemResource(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument(
        "price",
        type=float,
        required=True,
        help="this field is required")
    req_parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_by(name)
        if item:
            return item.to_dict(), 200
        else:
            return {}, 404

    @jwt_required()
    def post(self, name):
        data = ItemResource.req_parser.parse_args()
        try:
            if ItemModel.get_by(name):
                return {"message": "An item with name '{0}' already exist".format(name)}, 400
            ItemModel(name, **data).save()
            return {"message": "item created successfully"}, 201
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": "some error occurred | {0} | {1}".format(str(err), stack_trace)}, 500

    @jwt_required()
    def delete(self, name):
        try:
            item = ItemModel.get_by(name)
            if item is None:
                raise Exception("item does not exist")
            item.delete()
            return {"messages": "item deleted"}, 200
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": "some error occurred | {0} | {1}".format(str(err), stack_trace)}, 500

    @jwt_required()
    def put(self, name):
        data = ItemResource.req_parser.parse_args()
        try:
            item = ItemModel.get_by(name)
            if item is None:
                item = ItemModel(name, **data)
            else:
                item.name = name
                item.price = data["price"]
                item.store_id = data["store_id"]
            item.save()
            return {"message": "item updated successfully"}, 201
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": "some error occurred | {0} | {1}".format(str(err), stack_trace)}, 500


class ItemListResource(Resource):
    @staticmethod
    def get():
        items = ItemModel.query.all()
        if len(items) > 0:
            return {"items": [i.to_dict() for i in items]}, 200
        else:
            return {"items": []}, 404
