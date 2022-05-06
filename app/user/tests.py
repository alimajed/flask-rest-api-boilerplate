import json

from datetime import date

from app.user.daos import user_dao
from app.user.models import UserModel
from app.common.helpers import json_serial
from app.common.test_config import app_inst  # noqa


BASE_URL = "http://localhost:5000"


def test_create_user(app_inst):  # noqa
    with app_inst.test_client() as c:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        user_json = {
            "first_name": "ali",
            "last_name": "majed",
            "date_of_birth": date(1991, 3, 26),
            "email": "alimajed1991+3@gmail.com",
            "password": "password123",
        }
        req = c.post(
            f"{BASE_URL}/api/user/",
            data=json.dumps(user_json, default=json_serial),
            headers=headers,
        )
        assert req.status_code == 201


def test_user_sign_in(app_inst):  # noqa
    with app_inst.test_client() as c:
        user = UserModel(
            "ali", "majed", date(1991, 3, 26), "alimajed1991+4@gmail.com", "password123"
        )
        user_dao.create_user(user)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        creds = {"email": "alimajed1991+4@gmail.com", "password": "password123"}
        req = c.post(
            f"{BASE_URL}/api/user/authorize",
            data=json.dumps(creds, default=json_serial),
            headers=headers,
        )
        assert req.status_code == 200


def test_update_user(app_inst):  # noqa
    with app_inst.test_client() as c:
        user = UserModel(
            "ali", "majed", date(1991, 3, 26), "alimajed1991+5@gmail.com", "password123"
        )
        user_dao.create_user(user)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        creds = {"email": "alimajed1991+5@gmail.com", "password": "password123"}
        req = c.post(
            f"{BASE_URL}/api/user/authorize",
            data=json.dumps(creds, default=json_serial),
            headers=headers,
        )
        assert req.status_code == 200
        # test view protection
        user_json = {
            "first_name": "ali",
            "last_name": "majed",
            "date_of_birth": date(1991, 3, 27),
            "password": "password",
        }
        unauthorized_req = c.put(
            f"{BASE_URL}/api/user/",
            data=json.dumps(user_json, default=json_serial),
            headers=headers,
        )
        assert unauthorized_req.status_code == 401
        # update user info
        response = json.loads(req.data)
        access_token = response["access_token"]
        headers["Authorization"] = f"Bearer {access_token}"
        req = c.put(
            f"{BASE_URL}/api/user/",
            data=json.dumps(user_json, default=json_serial),
            headers=headers,
        )
        assert req.status_code == 200
        # make sure password updated
        headers.pop("Authorization")
        new_creds = {"email": "alimajed1991+5@gmail.com", "password": "password"}
        req = c.post(
            f"{BASE_URL}/api/user/authorize",
            data=json.dumps(new_creds, default=json_serial),
            headers=headers,
        )
        assert req.status_code == 200
