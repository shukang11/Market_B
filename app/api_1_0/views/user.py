from flask import request, current_app
from ..auth import api
from app.models import User
from ..errors.ApiError import CommonError, CateBluePrintError
from app.units.common import responseSuccessHandler
from ..errors.DAOError import NoResultFound
from app import db
from app.units.constantFactory import getMD5, get_random_num
from app.units.verfy import login_required, permission_required
from app.units.Constant import IDENTIFY


@api.route("/user", methods=['POST', ])
def register_user():
    """注册用户"""
    user_name = request.args.get("user_name")
    user_password = request.args.get("user_password")
    password_repeat = request.args.get("password_repeat")
    user_mobile = request.args.get("user_mobile")
    user_email = request.args.get("user_email")
    user_is_man = request.args.get("user_is_man")
    requires = ["user_name", "user_password", "password_repeat",
                "user_email", "user_is_man", ]
    for r in requires:
        if request.args.get(r) is None:
            return CommonError.args_miss('{}_required'.format(r))
    if password_repeat != user_password:
        return CommonError.args_miss(msg="两次密码不匹配")
    verfy_ = current_app.config['SERVICE_TOKEN_SUFFIX'] or 'token'
    user_verfy_code = getMD5("{0}{1}".format(get_random_num(), verfy_))
    user_ip = request.args.get("user_ip") or request.remote_addr
    user_id_card = request.args.get("user_id_card")
    user_last_ip = user_ip
    user_logo = request.args.get("user_logo")
    user_status = request.args.get("user_status") or 1
    if db.session.query(User).filter_by(user_email=user_email).first():
        return CommonError.args_miss("email_used")
    user = User()
    user.user_name = user_name
    user.user_verfy_code = user_verfy_code
    user.user_password = getMD5(user_password)
    user.user_mobile = user_mobile
    user.user_email = user_email
    user.user_ip = user_ip
    user.user_is_man = user_is_man
    user.user_id_card = user_id_card
    user.user_last_ip = user_last_ip
    user.user_logo = user_logo
    user.user_status = user_status
    db.session.add(user)
    db.session.commit()
    body = dict({
        "user_name": user.user_name,
        "user_verfy_code": user.user_verfy_code,
        "user_password": user.user_password,
        "user_mobile": user.user_mobile,
        "user_email": user.user_email,
        "user_ip": user.user_ip,
        "user_is_man": user.user_is_man,
        "user_id_card": user.user_id_card,
        "user_last_ip": user.user_last_ip,
        "user_status": user.user_status,
        "user_logo": user.user_logo,
    })
    return responseSuccessHandler(body=body)


@api.route('/user/self', methods=['GET', ])
@login_required
def get_self_info():
    """获得用户自己的信息"""
    token = request.args.get('token')
    user = User.get_user_by_token(token)
    body = dict({
        "user_name": user.user_name,
        "user_verfy_code": user.user_verfy_code,
        "user_password": user.user_password,
        "user_mobile": user.user_mobile,
        "user_email": user.user_email,
        "user_ip": user.user_ip,
        "user_is_man": user.user_is_man,
        "user_id_card": user.user_id_card,
        "user_last_ip": user.user_last_ip,
        "user_status": user.user_status,
        "user_logo": user.user_logo,
        "user_id": user.user_id,
    })
    return responseSuccessHandler(body=body)


@api.route("/user/login", methods=['POST'])
def user_login():
    """
    用户登录
    :return:
    """
    user_password = request.args.get("user_password")
    user_email = request.args.get("user_email")
    requires = ["user_password",
                "user_email", ]
    for r in requires:
        if request.args.get(r) is None:
            return CommonError.args_miss('{}_required'.format(r))
    try:
        user = db.session.query(User).filter_by(user_email=user_email).first()
        if user.user_password == user_password:
            verfy_ = current_app.config['SERVICE_TOKEN_SUFFIX'] or 'token'
            user_verfy_code = getMD5("{0}{1}".format(get_random_num(), verfy_))
            user.user_verfy_code = user_verfy_code
            db.session.add(user)
            db.session.commit()
            return responseSuccessHandler(body={"token": user_verfy_code})
        else:
            return CommonError.args_miss("password_or_email_worong")
    except NoResultFound:
        return CommonError.getError(errorCode=1201)


@api.route("/user/<int:user_id>", methods=['GET', ])
@login_required
def get_a_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return CommonError.getError(errorCode=1201)
    body = dict({
        "user_name": user.user_name,
        "user_mobile": user.user_mobile,
        "user_email": user.user_email,
        "user_is_man": user.user_is_man,
        "user_id_card": user.user_id_card,
        "user_logo": user.user_logo,
        "user_id": user.user_id,
    })
    return responseSuccessHandler(body=body)


@api.route("/user/audit", methods=['POST', ])
@permission_required(IDENTIFY.ADMINISTER)
def audit_user():
    """
    审核用户
    :return:
    """
    user_id = request.args.get('user_id') or 0
    if int(user_id) <= 0:
        return CommonError.getError(errorCode=1201)
    user: User = User.get_user_by_id(user_id)
    body = dict({
        "user_name": user.user_name,
        "user_verfy_code": user.user_verfy_code,
        "user_password": user.user_password,
        "user_mobile": user.user_mobile,
        "user_email": user.user_email,
        "user_ip": user.user_ip,
        "user_is_man": user.user_is_man,
        "user_id_card": user.user_id_card,
        "user_last_ip": user.user_last_ip,
        "user_status": user.user_status,
        "user_logo": user.user_logo,
        "user_id": user.user_id,
    })
    return responseSuccessHandler(body=body)
