import os

import pytest

from db import DB
from client import ClientFactory
from data import *


SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_URL = f"{SERVER_HOST}:{SERVER_PORT}/api/"

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


_db = DB(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
_db.connect()


_client_factory = ClientFactory(SERVER_URL)


@pytest.fixture(autouse=True)
def db():
    _db.clear_db()
    return _db


@pytest.fixture()
def client():
    return _client_factory.create_client()


@pytest.fixture()
def client_factory():
    return _client_factory


@pytest.fixture()
def superuser_client():
    _db.create_superuser(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)
    return _client_factory.create_client()


@pytest.fixture()
def user_client():
    _db.create_user(email=USER_EMAIL, password=USER_PASSWORD)
    return _client_factory.create_client()
