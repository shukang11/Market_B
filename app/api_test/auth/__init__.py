from flask import Blueprint
import app

api = Blueprint('api_test', __name__)
app.fetchRoute(api, "/api_test")


from app.api_test import views
