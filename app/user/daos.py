from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import abort

from app.common.daos import BaseDAO
from app.user.models import UserModel
from app.common.localization import gettext


class UserDAO(BaseDAO):
    def __init__(self, model):
        super().__init__(model)

    def authenticate(self, creds):
        user = self._find_by_email(creds["email"])
        if user and user.is_correct_password(creds["password"]):
            access_token = create_access_token(identity=user.email)
            return user, access_token
        abort(401, {"message": gettext("wrong_credentials")})

    def create_user(self, user):
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, user_id, data):
        user = self._find_by_email(user_id)
        if data.get("first_name"):
            user.first_name = data.get("first_name")
        if data.get("last_name"):
            user.last_name = data.get("last_name")
        if data.get("sex"):
            user.sex = data.get("sex")
        if data.get("date_of_birth"):
            user.date_of_birth = data.get("date_of_birth")
        if data.get("password"):
            user.password = generate_password_hash(data.get("password"))
        user.updated_at = datetime.utcnow()
        self.session.commit()

    def _find_by_email(self, _email):
        return self.session.query(self.model).filter_by(email=_email).first()


user_dao = UserDAO(UserModel)
