from marshmallow_sqlalchemy import ModelSchema
from models.user import UserModel


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
