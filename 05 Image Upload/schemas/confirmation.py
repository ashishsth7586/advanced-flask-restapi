from ma import ma
from models.confirmation import ConfirmationModel
from marshmallow_sqlalchemy import ModelSchema


class ConfirmationSchema(ModelSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expire_at", "confirmed")
        include_fk = True
