from app.units.ext import db, Flask, request
from config import config, Config, basedir
import os

__all__ = ['db', 'create_app']
route_list = []

def create_app(config_name) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app=app)
    # create_tables(app)
    register(app=app)
    app_dir = os.path.join(basedir, 'app')
    # for routes in os.listdir(app_dir):
    #     rou_path = os.path.join(app_dir, routes)
    #     if (not os.path.isfile(rou_path)) and routes != 'static' and routes != 'templates':
    #         __import__('app.' + routes)
    # for blueprints in route_list:
    #     if blueprints[1] is not None:
    #         app.register_blueprint(blueprints[0], url_prefix=blueprints[1])
    #     else:
    #         app.register_blueprint(blueprints[0])
    return app

def register(app):
    from app.api_1_0.auth import api as api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/v1000')

    from app.api_test import api as api_test
    app.register_blueprint(api_test, url_prefix='api/test')


def create_tables(app):

    with app.test_request_context():
        db.create_all()