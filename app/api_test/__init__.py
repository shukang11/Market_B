from flask import Blueprint

api = Blueprint('api_test', __name__)

from app.api_test import views