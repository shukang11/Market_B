from functools import wraps
from flask import request
from app.units.common import responseErrorHandler
from app.models import User
from app.units.Constant import IDENTIFY

def login_required(func):
    """检测登录权限"""
    @wraps(func)
    def decorator_view(*args, **kwargs):
        token = request.values.get('token', type=str) or request.get_json().get('token')
        if not token:
            return responseErrorHandler(errorCode=1000 ,msg='需要登录权限', httpCode=400)
        user = User.get_user_by_token(token)
        if user is None:
            return responseErrorHandler(errorCode=1000, msg='您的登录信息已过期，请重新登录', httpCode=400)
        return func(*args, **kwargs)
    return decorator_view

def permission_required(identify=IDENTIFY.ANONYMOUS):
    """权限限制"""
    def decorator(func):
        @wraps(func)
        def decorator_view(*args, **kwargs):
            token = request.args.get('token', type=str) or request.get_json().get('token')
            user: User = User.get_user_by_token(token)
            if user is None:
                return responseErrorHandler(errorCode=1000, msg='您的登录信息已过期，请重新登录', httpCode=400)
            if user.user_permition < identify:
                return responseErrorHandler(errorCode=1000, msg='您的操作权限不足， 请联系管理员', httpCode=400)
            return func(*args, **kwargs)
        return decorator_view
    return decorator
