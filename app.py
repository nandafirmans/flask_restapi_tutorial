from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserResource
from resources.item import ItemResource, ItemListResource
from resources.store import StoreResource, StoreListResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "nanda"
jwt = JWT(app, authenticate, identity)
api = Api(app)

api.add_resource(ItemResource, "/item/<string:name>")
api.add_resource(ItemListResource, "/items")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")
api.add_resource(UserResource, "/user")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
