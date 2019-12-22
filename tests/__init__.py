import pytest, json,logging
from app import app
from flask import Flask,request
from app import cache
from blueprints import app



@pytest.fixture
def client(request):
    return app.test_client()


