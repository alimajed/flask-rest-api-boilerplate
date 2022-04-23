from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.database import Session


class BaseModelSchema(SQLAlchemyAutoSchema):

    class Meta:
        sqla_session = Session
        load_instance = True


class BaseCustomSchema(Schema):

    class Meta:
        pass