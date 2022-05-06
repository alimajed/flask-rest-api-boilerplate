import pytest

from app import db, init_app


@pytest.fixture(scope="module")
def app_inst():
    app = init_app()
    app.app_context().push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
