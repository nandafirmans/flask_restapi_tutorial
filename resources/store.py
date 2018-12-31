import traceback
from typing import List
from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class StoreResource(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.get_by(name)
        if store:
            return store.to_dict(), 200
        else:
            return {}, 404

    @jwt_required()
    def post(self, name):
        try:
            if StoreModel.get_by(name):
                return {"message": f"An store with name '{name}' already exist"}, 400
            StoreModel(name).save()
            return {"message": "store created successfully"}, 201
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": f"an error occurred | {str(err)} | {stack_trace}"}, 500

    @jwt_required()
    def delete(self, name):
        try:
            store = StoreModel.get_by(name)
            if store is None:
                raise Exception("store does not exist")
            store.delete()
            return {"messages": "store deleted"}, 200
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": f"an error occurred | {str(err)} | {stack_trace}"}, 500


class StoreListResource(Resource):
    @jwt_required()
    def get(self):
        stores: List["StoreModel"] = StoreModel.query.all()
        if len(stores) > 0:
            return {"stores": [s.to_dict() for s in stores]}, 200
        else:
            return {"stores": []}, 404
