from app.units.ext import db, Flask, request
from config import config, Config

__all__ = ['db', 'create_app']
def create_app(config_name) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app=app)
    # from app.api_1_0.models.ItemModel import ItemModel
    # from app.api_1_0.models.ClassifyModel import CateModel
    # with app.test_request_context():
    #     db.create_all()
    register(app=app)
    return app

def register(app):
    from app.api_1_0 import api as api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/v1000')

    from app.api_test import api as api_test
    app.register_blueprint(api_test, url_prefix='api/test')