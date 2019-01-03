import traceback
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class UserResource(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument(
        "username",
        type=str,
        required=True,
        help="this field required")
    req_parser.add_argument(
        "password",
        type=str,
        required=True,
        help="this field required")

    @jwt_required()
    def get(self):
        users = UserModel.query.all()
        return {"users": [u.to_dict() for u in users] if len(users) > 0 else None}

    def post(self):
        data = UserResource.req_parser.parse_args()
        try:
            username = data["username"]
            if UserModel.get_by(username=username):
                return {"message": "username '{0}' is already used".format(username)}, 400
            UserModel(**data).save()
            return {"message": "user created successfully"}, 201
        except Exception as err:
            stack_trace = traceback.format_tb(err.__traceback__)
            return {"message": "some error occurred | {0} | {1}".format(str(err), stack_trace)}, 500
