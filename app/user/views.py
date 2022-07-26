from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.user.daos import user_dao
from app.user.schemas import (
    UserSchema,
    UpdateUserSchema,
    AuthResponseSchema,
    AuthCredentialSchema,
)


user_bp = Blueprint("user", __name__)

user_schema = UserSchema()
auth_creds_schema = AuthCredentialSchema()
auth_response_schema = AuthResponseSchema()
update_user_schema = UpdateUserSchema()
user_schema = UserSchema()


@user_bp.route("", methods=["POST"])
def create_user():
    user_json = request.get_json()
    user = user_schema.load(user_json)

    created_user = user_dao.create_user(user)
    return user_schema.dump(created_user), 201


@user_bp.route("", methods=["PUT"])
@jwt_required()
def update_user():
    data = request.get_json()
    user_id = get_jwt_identity()
    user_dao.update_user(user_id, data)
    return {}, 200


@user_bp.route("/authorize", methods=["POST"])
def authenticate():
    auth_creds_json = request.get_json()
    auth_creds = auth_creds_schema.load(auth_creds_json)

    user, access_token = user_dao.authenticate(auth_creds)
    return auth_response_schema.dump({"access_token": access_token, "user": user}), 200
