from app.units.ext import db, session, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from ..models import BaseModel
from ..units.constantFactory import getUnix_timeTuple

"""前台用户表"""
class UserModel(db.Model):
    """前台用户表"""
    __tablename__ = "bao_user"
    user_id = Column(INTEGER, Sequence(increment=1, start=1, name='user_id_seq'), primary_key=True)  # id
    user_nickname = Column(String(32), nullable=True)  # 昵称
    user_name = Column(String(20), nullable=True)  # 用户名
    user_verfy_code = Column(String(32), nullable=False)  # 用户验证
    user_password = Column(String(32), nullable=False)  # 加密密码
    user_mobile = Column(String(11), nullable=True)  # 手机号
    user_email = Column(String(32), nullable=True)  # 邮箱
    user_ip = Column(String(20), nullable=True)  # ip
    user_is_man = Column(SMALLINT(1), nullable=False)  # 性别
    user_id_card = Column(String(32), nullable=True)  # 身份证号码
    user_last_ip = Column(String(20), nullable=True)  # 最后登录的ip
    user_status = Column(SMALLINT, nullable=False, default=1)  # 状态 0 不可用 1 可用
    user_current_login_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 最近登录的时间
    user_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())# 创建时间
    user_logo = Column(String(255), nullable=True)  # 用户头像


"""后台用户表"""
class BackStageUserModel(db.Model):
    __tablename__ = "bao_backstage_user"

    user_id = Column(INTEGER, Sequence(increment=1, start=1, name='user_id_seq'), primary_key=True)  # id
    user_name = Column(String(20), nullable=False)  # 用户名
    user_verfy_code = Column(String(32), nullable=False)  # 用户验证
    user_password = Column(String(32), nullable=False)  # 加密密码
    user_mobile = Column(String(11), nullable=True)  # 手机号
    user_email = Column(String(32), nullable=True)  # 邮箱
    user_ip = Column(String(20), nullable=False, default='0.0.0.0')  # ip
    user_is_man = Column(SMALLINT(1), nullable=False, default=1)  # 性别
    user_id_card = Column(String(32), nullable=True)  # 身份证号码
    user_last_ip = Column(String(20), nullable=True)  # 最后登录的ip
    user_status = Column(SMALLINT(1), nullable=False, default=1)  # 状态
    user_current_login_time = Column(String(11), nullable=False, default=getUnix_timeTuple(),
                                     onupdate=getUnix_timeTuple())  # 最近登录的时间
    user_logo = Column(String(255), nullable=True)  # 用户头像
    user_permition = Column(SMALLINT, nullable=False, default=0)  # 权限管理 0 不可用状态 1 只读状态 2 可写状态 4 可执行
