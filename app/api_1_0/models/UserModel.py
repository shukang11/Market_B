from app.api_1_0.units.ext import db, INTEGER, \
    String, TEXT, SMALLINT, Sequence
from app.api_1_0.units.constantFactory import getUnix_timeTuple

class UserModel(db.Model):
    """前台用户表"""
    __tablename__ = "bao_user"
    user_id = db.Column(INTEGER, Sequence(increment=1, start=1, name='user_id_seq'), primary_key=True)  # id
    user_nickname = db.Column(String(32), nullable=True)  # 昵称
    user_name = db.Column(String(20), nullable=True)  # 用户名
    user_verfy_code = db.Column(String(32), nullable=False)  # 用户验证
    user_password = db.Column(String(32), nullable=False)  # 加密密码
    user_mobile = db.Column(String(11), nullable=True)  # 手机号
    user_email = db.Column(String(32), nullable=True)  # 邮箱
    user_ip = db.Column(TEXT, nullable=True)  # ip
    user_is_man = db.Column(SMALLINT, nullable=False)  # 性别
    user_id_card = db.Column(String(32), nullable=True)  # 身份证号码
    user_last_ip = db.Column(String(20), nullable=True)  # 最后登录的ip
    user_status = db.Column(SMALLINT, nullable=False, default=1)  # 状态 0 不可用 1 可用
    user_current_login_time = db.Column(String(32), nullable=True)  # 最近登录的时间
    user_logo = db.Column(TEXT, nullable=True)  # 用户头像


    def __init__(self, nickname=None, name=None, ip=None, is_man=None,
                 id_card=None, mobile=None, password=None, last_ip=None,
                 status=None, verfy_code=None, email=None, user_logo=None):
        self.user_name = name
        self.user_nickname = nickname
        self.user_ip = ip
        self.user_password = password
        self.user_is_man = is_man
        self.user_id_card = id_card
        self.user_mobile = mobile
        self.user_email = email
        self.user_last_ip = last_ip
        self.user_status = status
        self.user_verfy_code = verfy_code
        self.user_logo = user_logo

    @property
    def info(self):
        return {
            "user_name": self.user_name,
            "user_nickname": self.user_nickname,
            "user_ip": self.user_ip,
            "user_is_man": self.user_is_man,
            "user_mobile": self.user_mobile,
            "user_email": self.user_email,
            "user_last_ip": self.user_last_ip,
            "user_status": self.user_status,
            "user_verfy_code": self.user_verfy_code,
            "user_logo": self.user_logo,
        }


class BackStageUserModel(db.Model):
    __tablename__ = "bao_backstage_user"
    user_id = db.Column(INTEGER, Sequence(increment=1, start=1, name='user_id_seq'), primary_key=True)  # id
    user_name = db.Column(String(20), nullable=False)  # 用户名
    user_verfy_code = db.Column(String(32), nullable=False)  # 用户验证
    user_password = db.Column(String(32), nullable=False)  # 加密密码
    user_mobile = db.Column(String(11), nullable=True)  # 手机号
    user_email = db.Column(String(32), nullable=True)  # 邮箱
    user_ip = db.Column(TEXT, nullable=True)  # ip
    user_is_man = db.Column(SMALLINT, nullable=False, default=1)  # 性别
    user_id_card = db.Column(String(32), nullable=True)  # 身份证号码
    user_last_ip = db.Column(String(20), nullable=True)  # 最后登录的ip
    user_status = db.Column(SMALLINT, nullable=False, default=1)  # 状态
    user_current_login_time = db.Column(String(32), nullable=True, default=getUnix_timeTuple())  # 最近登录的时间
    user_logo = db.Column(TEXT, nullable=True)  # 用户头像
    user_permition = db.Column(SMALLINT, nullable=False, default=0) # 权限管理 0 不可用状态 1 只读状态 2 可写状态 4 可执行


    def __init__(self, name=None, ip=None, is_man=None,
                 id_card=None, mobile=None, password=None, last_ip=None,
                 status=None, verfy_code=None, email=None, user_logo=None):
        self.user_name = name
        self.user_ip = ip
        self.user_password = password
        self.user_is_man = is_man
        self.user_id_card = id_card
        self.user_mobile = mobile
        self.user_email = email
        self.user_last_ip = last_ip
        self.user_status = status
        self.user_verfy_code = verfy_code
        self.user_logo = user_logo

    @property
    def info(self):
        return {
            "user_name": self.user_name,
            "user_ip": self.user_ip,
            "user_is_man": self.user_is_man,
            "user_mobile": self.user_mobile,
            "user_email": self.user_email,
            "user_last_ip": self.user_last_ip,
            "user_status": self.user_status,
            "user_verfy_code": self.user_verfy_code,
            "user_logo": self.user_logo,
        }