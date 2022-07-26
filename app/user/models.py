from sqlalchemy import Column
from sqlalchemy.types import Date, String
from werkzeug.security import check_password_hash, generate_password_hash

from app.common.models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    sex = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)

    def __init__(self, first_name, last_name, sex, date_of_birth, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    def is_correct_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)
