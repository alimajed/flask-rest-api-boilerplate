from marshmallow import fields

from app.user.models import UserModel
from app.common.schemas import BaseModelSchema, BaseCustomSchema


class UserSchema(BaseModelSchema):
    class Meta(BaseModelSchema.Meta):
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "created_at", "updated_at")


class UpdateUserSchema(BaseCustomSchema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    sex = fields.Str(required=False)
    date_of_birth = fields.Str(required=False)
    password = fields.Str(required=False)


class AuthCredentialSchema(BaseCustomSchema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthResponseSchema(BaseCustomSchema):
    access_token = fields.Str(required=True)
    user = fields.Nested(UserSchema)
