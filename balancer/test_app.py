from sanic_testing.testing import SanicTestClient

from app import app

test_client = SanicTestClient(app)


def test__handler():
    ...


def test__config__create():
    ...


def test__config__update():
    ...


def test__config__delete():
    ...
