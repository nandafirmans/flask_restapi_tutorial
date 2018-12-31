from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.get_by(username=username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.get_by(id=user_id)