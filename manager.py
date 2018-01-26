import os
from app import create_app, db
from flask_script import Manager, Shell# 项目对接命令行接口
from app.units.ext import migrate, MigrateCommand
from app.models import tables

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)
migrate.init_app(app, db=db)

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    """性能分析， 当页面请求时，可以获得分析结果"""
    from  werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=(length), profile_dir=profile_dir)
    app.run()

def make_shell_context():
    tables['app'] = app
    tables['db'] = db
    return tables
manager.add_command('shell', Shell(make_context=make_shell_context()))
manager.add_command('db', MigrateCommand)


@manager.command
def sharedData():
    """一般来说，静态文件都使用Nginx服务，但是在测试环境中，对资源响应的要求不高
    所以也会使用这个中间件"""
    from werkzeug.wsgi import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        'static': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run()

@manager.command
def debug():
    """使用wsgi的调试器启动"""
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    app.run()

@manager.command
def deploy():
    """启动应用，并打开调试模式"""
    app.run('0.0.0.0', port=5000, debug=True)



if __name__ == '__main__':
    manager.run(default_command=debug.__name__)
    # debug()