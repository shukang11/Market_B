from app.units.ext import INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from app import db
from app.units.constantFactory import getUnix_timeTuple, get_list_from_column

__all__ = ['ItemCommonAttributeKeyModel', 'ItemCommonAttributeValueModel', 'Brand', 'Cate', 'Item', 'Cart', 'OrderContainItem', 'Order','User', 'Activity']

# 对外展示的
tables = {}


def addModel(model):
    tables[model.__name__] = model
    return model


class BaseModel():
    """可以拓展功能"""
    pass


"""商品的一般属性键表"""


@addModel
class ItemCommonAttributeKeyModel(db.Model, BaseModel):
    """
    商品的一般属性，一般相同类目下的通用属性
    向上是叶子类目
    """
    __tablename__ = "bao_common_attribute_key"

    attr_id = Column(INTEGER, Sequence(start=1, increment=1, name="attr_id_sep"), primary_key=True,
                     autoincrement=True)  # 主键
    cate_id = Column(INTEGER, nullable=True, default=-1)  # 所属叶子分类
    attr_name = Column(String(64), nullable=True)  # 属性名称
    attr_index = Column(SMALLINT(1), nullable=True,
                        default=0)  # 属性是否可以检索;0不需要检索; 1关键字检索2范围检索,该属性应该是如果检索的话,可以通过该属性找到有该属性的商品
    attr_order = Column(SMALLINT, nullable=True, default=0)  # 属性显示的顺序,数字越大越靠前,如果数字一样则按id顺序
    is_linked = Column(SMALLINT(1), nullable=True, default=0)  # 是否关联,0 不关联 1关联; 如果关联, 那么用户在购买该商品时,具有有该属性相同的商品将被推荐给用户
    attr_input_type = Column(SMALLINT(1), nullable=True, default=1)  # 当添加商品时,该属性的添加类别; 0为手功输入;1为选择输入;2为多行文本输入
    attr_values = Column(TEXT, nullable=True)  # 即选择输入,则attr_name对应的值的取值就是该这字段值
    attr_group = Column(SMALLINT, nullable=True, default=0)  # 属性分组,相同的为一个属性组应该取自goods_type的attr_group的值的顺序.
    attr_can_muti = Column(SMALLINT(1), nullable=True, default=1)  # 属性是否多选; 0否; 1是 如果可以多选,则可以自定义属性,并且可以根据值的不同定不同的价
    attr_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    attr_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(),
                              onupdate=getUnix_timeTuple())  # 修改时间
    attr_is_delete = Column(SMALLINT(1), nullable=True, default=1)  # 是否已删除


"""商品的一般属性值表"""


@addModel
class ItemCommonAttributeValueModel(db.Model, BaseModel):
    """
        商品的一般属性值，一般相同类目下的通用属性值
        向上是叶子类目
        """
    __tablename__ = "bao_common_attribute_value"

    value_id = Column(INTEGER, Sequence(start=1, increment=1, name="value_id_sep"), primary_key=True,
                      autoincrement=True)  # 主键
    attr_key_id = Column(INTEGER, nullable=True)  # 对应的属性
    value = Column(String(255), nullable=True)  # 对应的值
    value_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    value_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 修改时间
    value_is_delete = Column(SMALLINT(1), nullable=True, default=1)  # 是否已删除


@addModel
class Brand(db.Model, BaseModel):
    """
    品牌的模型
    """
    __tablename__ = "bao_brand"

    brand_id = Column(INTEGER, Sequence(increment=1, start=1, name="brand_id_seq"), primary_key=True,
                      autoincrement=True)  # 品牌自增id
    brand_name = Column(String(22), nullable=True)  # 品牌名
    brand_pic_url = Column(String(255), nullable=True)  # 品牌的图片地址
    brand_cate_id = Column(String(255), nullable=True)  # 所属叶子分类, 是一个数组，一对多
    brand_note = Column(String(255), nullable=True)  # 品牌的简介
    brand_is_delete = Column(SMALLINT(1), nullable=True, default=1)  # 默认是删除的
    brand_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    brand_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(),
                               onupdate=getUnix_timeTuple())  # 修改时间


"""分类表，包含了分类和叶子分类"""


@addModel
class Cate(db.Model, BaseModel):
    """分类表"""
    __tablename__ = 'bao_cate'

    cate_id = Column(INTEGER, Sequence(increment=1, start=1, name='item_spu_id_seq'), primary_key=True)
    cate_supercate_id = Column(INTEGER, nullable=True, default=0)  # 类目的上级类目,为0 代表1级目录
    cate_is_parent = Column(SMALLINT(1), nullable=True, default=0)  # 是否是一级类目,默认不是
    cate_name = Column(String(20), nullable=True)  # 类目名称
    cate_is_delete = Column(SMALLINT(1), nullable=True, default=0)  # 是否被删除
    cate_common_props = Column(String(255), nullable=True)  # 如果是叶子类目，需要有一些属性值
    cate_sort_num = Column(INTEGER, nullable=True, default=0)  # 类目的排列序号
    cate_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    cate_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(),
                              onupdate=getUnix_timeTuple())  # 修改时间

    @classmethod
    def insert_a_cate(cls, cate_name=None,
                      super_cate_id=None, sort_num=0):
        cate = Cate()
        cate.cate_name = cate_name
        cate.cate_supercate_id = super_cate_id
        cate.cate_sort_num = sort_num
        db.session.add(cate)
        db.session.commit()
        return cate.cate_id

    @classmethod
    def get_children_cate(cls, cate_id):
        return db.session.query(Cate).filter_by(cate_supercate_id=cate_id).all()

    @classmethod
    def get_a_cate(cls, cate_id=None, cate_name=None):
        if cate_id is None and cate_name is None:
            raise ValueError('cate_id or cate_name cant be None')
        if cate_id:
            return db.session.query(Cate).filter_by(cate_id=cate_id).first()
        elif cate_name:
            return db.session.query(Cate).filter_by(cate_name=cate_name).first()
        return None

    @classmethod
    def delete_cates(cls, cate_ids=list()) -> bool:
        # db.session.query(Cate).filter(Cate.cate_id.in_(cate_ids)).delete(synchronize_db.session='fetch')
        tmp = db.session.query(Cate).filter(Cate.cate_id.in_(cate_ids)).all()
        cates = list()
        for cate in tmp:
            cate.cate_is_delete = 1
        db.session.commit()
        return True


"""商品表"""


@addModel
class Item(db.Model, BaseModel):
    """商品信息表"""
    __tablename__ = "bao_item"
    item_id = Column(INTEGER, Sequence(increment=1, start=1, name="item_id_sep"), primary_key=True,
                     autoincrement=True)  # id
    # 商品分类信息(用于定位)
    item_cate_name = Column(String(20), nullable=True)  # 产品类目名称, 优先替换掉类目id对应名称
    item_cid = Column(INTEGER, nullable=True)  # 商品类目id, 必须是提供的叶子类目
    # 商品的基本信息
    item_name = Column(String(64), nullable=True)  # 产品名称
    item_price = Column(DECIMAL(10, 2), nullable=True)  # 产品的市场价格
    item_desc = Column(TEXT, nullable=True)  # 产品描述
    item_brand_id = Column(INTEGER, nullable=True)  # 商品所属的品牌
    item_sn = Column(String(64), nullable=True)  # 商品的货号
    item_sn_type = Column(SMALLINT(1), nullable=True, default=1)  # 商品标号的类型
    # 商品的店家设置
    item_pic_url = Column(String(255), nullable=True)  # 产品的主图地址
    item_vertical_market = Column(SMALLINT(1), nullable=True, default=0)  # 垂直市场,暂时只有一个

    item_stock_inventory = Column(INTEGER, nullable=True, default=0)  # 商品库存量
    item_shop_price = Column(DECIMAL(10, 2), nullable=True)  # 商品的店内价格，商家填写
    item_sell_pt = Column(String(20), nullable=True)  # 产品卖点
    item_template_id = Column(SMALLINT(2), nullable=True, default=1)  # 模板id
    item_remark = Column(String(255), nullable=True)  # 商家备注
    item_on_sale_state = Column(SMALLINT(1), nullable=True, default=0)  # 0 下架 1 只读不可下单(活动预告) 2 正常上架
    # 产品属性相关
    item_binds = Column(String(255), nullable=True)  # 产品的非关键属性， 格式pid:vid;
    item_sale_props = Column(String(255), nullable=True)  # 商品的销售属性列表.格式:pid:vid;pid:vid
    item_custom_props = Column(String(255), nullable=True)  # 用户自定义的属性 pid1:value1;pid2:value2 例如：“20000:优衣库”，表示“品牌:优衣库”

    # 不提供给商家修改
    item_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    item_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(),
                              onupdate=getUnix_timeTuple())  # 修改时间
    item_standard_price = Column(DECIMAL(10, 2), nullable=True)  # 商品的标准价格
    item_level = Column(SMALLINT(1), nullable=True, default=1)  # 产品级别
    item_rate_num = Column(SMALLINT, nullable=True, default='0')  # 产品评分
    item_sale_num = Column(INTEGER, nullable=True, default=0)  # 产品销量
    item_belong_shop_id = Column(INTEGER, nullable=True)  # 商品属于的店家
    item_status = Column(SMALLINT(1), nullable=True, default=1)  # 状态(0 审核未通过 1 等待审核 2 审核通过)
    item_is_delete = Column(SMALLINT(1), nullable=True, default=1)  # 商品是否被删除

    def item_dict(self, needall=False):
        """
        获得item的结构化信息
        :param needall: 是否需要全量信息
        :return: dict()
        """
        query = db.session.query(Cate).filter_by(cate_id=self.item_cid).one()
        body = dict()
        body["item_id"] = self.item_id
        body["item_cate_name"] = self.item_cate_name or query.cate_name
        body["item_cid"] = self.item_cid
        body["item_name"] = self.item_name
        body["item_price"] = str(self.item_price)
        body["item_desc"] = self.item_desc
        body["item_brand_id"] = self.item_brand_id
        body["item_sn"] = self.item_sn
        body["item_sn_type"] = self.item_sn_type
        body["item_pic_url"] = self.item_pic_url
        body["item_vertical_market"] = self.item_vertical_market
        body["item_stock_inventory"] = self.item_stock_inventory
        body["item_shop_price"] = str(self.item_shop_price)
        body["item_sell_pt"] = get_list_from_column(self.item_sell_pt)
        body["item_template_id"] = self.item_template_id
        body["item_remark"] = self.item_remark
        body["item_on_sale_state"] = self.item_on_sale_state
        body["item_binds"] = get_list_from_column(self.item_binds)
        body["item_sale_props"] = get_list_from_column(self.item_sale_props)
        body["item_custom_props"] = get_list_from_column(self.item_custom_props) or []
        body["item_create_time"] = self.item_create_time
        body["item_update_time"] = self.item_update_time
        body["item_standard_price"] = str(self.item_standard_price)
        body["item_level"] = self.item_level
        body["item_rate_num"] = self.item_rate_num
        body["item_sale_num"] = self.item_sale_num
        body["item_status"] = self.item_status
        if needall:
            body["item_belong_shop_id"] = self.item_belong_shop_id
            body["item_is_delete"] = self.item_is_delete
        return body


"""购物车"""


@addModel
class Cart(db.Model):
    __tablename__ = "bao_cart"

    cart_id = Column(INTEGER, Sequence(increment=1, start=1, name='cart_id_seq'), primary_key=True)
    cart_item_id = Column(INTEGER, nullable=True)  # 商品的id
    cart_sku_id = Column(INTEGER, default='0')  # 商品规格销售属性
    cart_add_from = Column(SMALLINT(2), nullable=True)  # 从哪里加入到购物车的
    cart_item_belong = Column(INTEGER, nullable=True, default='0')  # 购买人
    cart_sku_num = Column(INTEGER, default='0')  # 改属性购买的数量
    is_delete = Column(SMALLINT(1), default='0')  # 是否被删除


"""订单关联商品"""
@addModel
class OrderContainItem(db.Model):
    __tablename__ = "bao_rsp_order_item"

    rsp_id = Column(INTEGER, Sequence(increment=1, start=1, name='rsp_id_seq'), primary_key=True)
    order_sn = Column(String(64), nullable=False)# 订单id
    item_sku_id = Column(INTEGER, default='0')
    item_sku_num = Column(INTEGER, default='0')


"""订单"""

@addModel
class Order(db.Model):
    __tablename__ = "bao_order"

    # 订单的基本信息
    order_id = Column(INTEGER, Sequence(increment=1, start=1, name='order_id_seq'), primary_key=True)
    order_sn = Column(String(64), nullable=True)  # 订单流水号
    user_id = Column(INTEGER, nullable=True)  # 用户的id
    # 订单的价格状态
    sum_price = Column(DECIMAL(10, 2), default="0.00")  # 订单的总价格
    totol_price = Column(DECIMAL(10, 2), default='0.00')  # 除掉优惠后的价格
    pay_price = Column(DECIMAL(10, 2), default='0.00')  # 实际需要支付的价格

    # 订单的状态信息
    create_ip = Column(String(15), default='0.0.0.0')  # 创建的ip
    create_time = Column(String(11), default=getUnix_timeTuple())  # 订单的创建时间
    pay_time = Column(String(11), default='0')  # 支付时间
    receive_time = Column(String(11), default="0")  # 收货时间
    order_is_delete = Column(SMALLINT(1), default=1)  # 订单是否被删除
    order_status = Column(SMALLINT, default='0')  # 订单的状态
    rec_addr_id = Column(INTEGER, nullable=True)  # 收货地址id

    # 订单的支付信息
    pay_platform = Column(SMALLINT, default=0)  # 支付平台 ios/win..
    pay_machine_code = Column(String(64), default="unknown")  # 支付设备
    pay_system_version = Column(String(32), nullable=True)  # 支付的系统版本
    pay_app_version = Column(String(32), nullable=True)  # 支付app的版本
    pay_type = Column(SMALLINT, default=0)  # 支付方式
    is_payed = Column(SMALLINT(1), default=0)  # 是否已支付

    # 订单的拓展信息
    remark = Column(String(255), nullable=True)  # 留言
    comment_id = Column(INTEGER, nullable=True)  # 评价， 不确定有没有追加评价，单独开一张表


"""前台用户表"""


@addModel
class User(db.Model):
    """前台用户表"""
    __tablename__ = "bao_user"
    user_id = Column(INTEGER, Sequence(increment=1, start=1, name='user_id_seq'), primary_key=True)  # id
    user_nickname = Column(String(32), nullable=True)  # 昵称
    user_name = Column(String(20), nullable=True)  # 用户名
    user_verfy_code = Column(String(32), nullable=True)  # 用户验证
    user_password = Column(String(32), nullable=True)  # 加密密码
    user_mobile = Column(String(11), nullable=True)  # 手机号
    user_email = Column(String(32), nullable=True)  # 邮箱
    user_ip = Column(String(20), nullable=True)  # ip
    user_is_man = Column(SMALLINT(1), nullable=True)  # 性别
    user_id_card = Column(String(32), nullable=True)  # 身份证号码
    user_last_ip = Column(String(20), nullable=True)  # 最后登录的ip
    user_status = Column(SMALLINT, nullable=False, default=1)  # 状态 0 不可用 1 可用
    user_current_login_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 最近登录的时间
    user_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    user_logo = Column(String(255), nullable=True)  # 用户头像
    user_permition = Column(SMALLINT, nullable=True, default=0)  # 权限管理 0 不可用状态 1 只读状态 2 可写状态 4 可执行

    @classmethod
    def get_user_by_token(self, token):
        try:
            return db.session.query(User).filter_by(user_verfy_code=token).first()
        except:
            return None

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            return db.session.query(User).filter_by(user_id=user_id).first()
        except:
            return None


@addModel
class Activity(db.Model):
    """活动表"""
    __tablename__ = "bao_activity"

    activity_id = Column(INTEGER, Sequence(increment=1, start=1, name='Activity_id_seq'), primary_key=True)  # id
    activity_title = Column(String(32), nullable=True)  # 标题
    activity_url = Column(String(255), nullable=True)
    activity_create_time = Column(String(11), nullable=True, default=getUnix_timeTuple())  # 创建时间
    activity_link = Column(String(255), nullable=True)  # 活动链接
    activity_type = Column(SMALLINT, nullable=True, default=0)  # 活动类型 10 首推Banner
    activity_recommand = Column(SMALLINT, nullable=True, default=0)  # 是否推荐
    activity_is_delete = Column(SMALLINT, nullable=True, default=1)  # 是否被删除

    @classmethod
    def insertActivity(cls, title, url, link, type, is_recommand):
        activate = Activity()
        activate.activity_url = url
        activate.activity_title = title
        activate.activity_link = link
        activate.activity_type = type
        activate.activity_recommand = is_recommand
        db.session.add(activate)
        db.session.commit()
        return activate.activity_id

    @classmethod
    def deleteActivity(cls, id):
        activity = db.session.query(Activity).filter_by(activity_id=id).one()
        if activity:
            activity.activity_is_delete = 1
        else:
            return False
        db.session.commit()
        return True
