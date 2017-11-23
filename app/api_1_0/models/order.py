from app.units.ext import db, session, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from ..models import BaseModel
from ..units.constantFactory import getUnix_timeTuple

class Cart(db.Model):
    __tablename__ = "bao_cart"

    cart_id = Column(INTEGER, Sequence(increment=1, start=1, name='cart_id_seq'), primary_key=True)
    cart_item_id = Column(INTEGER, nullable=False)# 商品的id
    cart_item_num = Column(INTEGER, nullable=False, default=0)# 购买商品的数量
    cart_add_from = Column(SMALLINT(2), nullable=False)# 从哪里加入到购物车的
    cart_item_attr_keys = Column(String(128), nullable=True)# 商品的销售属性
    cart_item_attr_value = Column(String(128), nullable=True)# 商品的销售属性值

class Order(db.Model):
    __tablename__ = "bao_order"

    # 订单的基本信息
    order_id = Column(INTEGER, Sequence(increment=1, start=1, name='order_id_seq'), primary_key=True)
    order_sn = Column(String(64), nullable=False)# 订单流水号
    user_id = Column(INTEGER, nullable=True)# 用户的id
    # 订单的价格状态
    sum_price = Column(DECIMAL(10, 2), default="0.00")# 订单的总价格
    totol_price = Column(DECIMAL(10, 2), default='0.00')# 除掉优惠后的价格
    pay_price = Column(DECIMAL(10, 2), default='0.00')# 实际需要支付的价格

    # 订单的状态信息
    create_ip = Column(String(15), default='0.0.0.0')  # 创建的ip
    create_time = Column(String(11), default=getUnix_timeTuple())  # 订单的创建时间
    pay_time = Column(String(11), default='0')  # 支付时间
    receive_time = Column(String(11), default="0")# 收货时间
    order_is_delete = Column(SMALLINT(1), default=1)# 订单是否被删除
    order_status = Column(SMALLINT, default='0')  # 订单的状态
    rec_addr_id = Column(INTEGER, nullable=True)  # 收货地址id

    # 订单的支付信息
    pay_platform = Column(SMALLINT, default=0)# 支付平台 ios/win..
    pay_machine_code = Column(String(64), default="unknown")# 支付设备
    pay_system_version = Column(String(32), nullable=True)# 支付的系统版本
    pay_app_version = Column(String(32), nullable=True)# 支付app的版本
    pay_type = Column(SMALLINT, default=0)  # 支付方式
    is_payed = Column(SMALLINT(1), default=0)  # 是否已支付

    # 订单的拓展信息
    remark = Column(String(255), nullable=True)  # 留言
    comment_id = Column(INTEGER, nullable=True)# 评价， 不确定有没有追加评价，单独开一张表
