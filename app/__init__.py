from app.units.ext import Flask, request
from config import config, Config, root_dir
import os
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

__all__ = ['db', 'create_app']
route_list = []

mail = Mail()
db = SQLAlchemy()

def fetchRoute(blueprint, prefix=None):
    tempList = [blueprint, prefix]
    route_list.append(tempList)



def create_app(config_name) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    createTables(config_name, app)
    config[config_name].init_app(app)
    # 注册插件
    mail.init_app(app)
    app_dir = os.path.join(root_dir, 'app')
    for routes in os.listdir(app_dir):
        rou_path = os.path.join(app_dir, routes)
        if (not os.path.isfile(rou_path)) and routes != 'static' and routes != 'templates':
            if (os.path.exists(os.path.join(rou_path, "auth"))):
                __import__('app.' + routes + ".auth")
                # 从route_list 引入蓝图
    for blueprints in route_list:
        if blueprints[1] is not None:
            app.register_blueprint(blueprints[0], url_prefix=blueprints[1])
        else:
            app.register_blueprint(blueprints[0])
    return app

# 注册蓝图
def register(app):
    pass
    # from app.api_1_0.auth import api as api_1_0
    # app.register_blueprint(api_1_0, url_prefix='/api/v1000')
    #
    # from app.api_test import api as api_test
    # app.register_blueprint(api_test, url_prefix='api/test')

def createTables(config_name, app):
    if config_name is not 'production':
        from app.models import __all__
        with app.test_request_context():
            db.create_all()