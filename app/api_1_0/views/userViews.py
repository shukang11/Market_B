from app.api_1_0 import api
from flask import request, url_for
from app.api_1_0.units.ext import db, NoResultFound
from app.api_1_0.models.UserModel import UserModel
from app.api_1_0.units.constantFactory import getUnix_timeTuple, getMD5
from app.api_1_0.units.common import responseSuccessHandler
from app.api_1_0.errors.ApiError import userBluePrintError
from app.api_1_0.errors.DAOError import NoResultFound, MultipleResultsFound

def get_a_user_with_token(token):
    """通过用户验证获得一个用户"""
    if token is None or len((token)) == 0:
        return None
    try:
        user = db.session.query(UserModel).filter_by(user_verfy_code=token).one()
        if user:
            return user
        return None
    except NoResultFound:
        return None

@api.route("/user/login", methods=['POST'])
def login():
    """
    用户登录
    :return:
    """
    path = request.path # 请求的路径
    if path:
        path = "POST {}".format(path)
    phone = request.args.get('phone')
    password = request.args.get('password')
    if phone is None:
        return userBluePrintError.getError(errorCode=2002, request=path)
    elif password is None:
        return userBluePrintError.getError(errorCode=2001, request=path)
    phone_exist = db.session.query(UserModel).filter_by(user_mobile=phone).all()
    if len(phone_exist) == 0:
        return userBluePrintError.getError(errorCode=2002, request=path)
    sec_password = getMD5(password)
    print(sec_password)
    try:
        usr = db.session.query(UserModel) \
            .filter_by(user_mobile=phone, user_password=sec_password) \
            .first()
        # 更新登录信息
        unix_time = getUnix_timeTuple()
        # 更新加密验证信息
        verfy_code = getMD5("{0}{1}".format(usr.user_mobile, unix_time))
        # 更新登录IP
        remote_addr = request.remote_addr
        usr.user_verfy_code = verfy_code
        usr.user_current_login_time = unix_time
        usr.user_ip = remote_addr
        db.session.add(usr)
        db.session.commit()
        return responseSuccessHandler(statusCode=200)
    except Exception as e:
        print(e)
        db.session.rollback()
        return userBluePrintError.getError(errorCode=2003, request=path)

@api.route("/user/register", methods=['POST'])
def register():
    pass

@api.route("/user/<string:user_id>/logout", methods=['POST'])
def logout(user_id=""):
    """
    用户登出
    :return:
    """
    print(user_id)
    return responseSuccessHandler(body=user_id)


@api.route("/user/<string:user_token>", methods=['GET'])
def getuserInfo(user_token=""):
    """
    获得用户的信息
    :param user_id: 用户的唯一标识符
    :return:
    """
    path = request.path  # 请求的路径
    method = request.method
    if path:
        path = "{0} {1}".format(method, path)
    usr = get_a_user_with_token(token=user_token)
    if usr:
        body = usr.info
        return responseSuccessHandler(body=body)
    else:
        return userBluePrintError.getError(errorCode=1004,request=path)
