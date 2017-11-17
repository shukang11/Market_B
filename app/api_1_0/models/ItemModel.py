from app.api_1_0.units.ext import db, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from app.api_1_0.models import BaseModel
from app.api_1_0.units.constantFactory import getUnix_timeTuple
from app.api_1_0.models import BaseModel
from app.api_1_0.units.constantFactory import getUnix_timeTuple


class ItemModel(db.Model, BaseModel):
    """商品信息表"""
    __tablename__ = "bao_item"
    item_id = Column(INTEGER, Sequence(increment=1, start=1, name="item_id_sep"), primary_key=True, autoincrement=True)  # id
    # 商品分类信息(用于定位)
    item_cate_name = Column(String(20), nullable=True)  # 产品类目名称, 优先替换掉类目id对应名称
    item_cid = Column(INTEGER, nullable=False)  # 商品类目id, 必须是提供的叶子类目
    # 商品的基本信息
    item_name = Column(String(64), nullable=False)  # 产品名称
    item_price = Column(DECIMAL(10, 2), nullable=False)  # 产品的市场价格
    item_desc = Column(TEXT, nullable=False)  # 产品描述
    item_brand_id = Column(INTEGER, nullable=False)# 商品所属的品牌
    item_sn = Column(String(64), nullable=False)# 商品的货号
    item_sn_type = Column(SMALLINT(1), nullable=False, default=1)# 商品标号的类型
    # 商品的店家设置
    item_pic_url = Column(String(255), nullable=False)  # 产品的主图地址
    item_vertical_market = Column(SMALLINT(1), nullable=False, default=0) # 垂直市场,暂时只有一个

    item_stock_inventory = Column(INTEGER, nullable=False, default=0)# 商品库存量
    item_shop_price = Column(DECIMAL(10, 2), nullable=False)  # 商品的店内价格，商家填写
    item_sell_pt = Column(String(20), nullable=True)  # 产品卖点
    item_template_id = Column(SMALLINT(2), nullable=False, default=1)  # 模板id
    item_remark = Column(String(255), nullable=True)# 商家备注
    item_on_sale_state = Column(SMALLINT(1), nullable=False, default=0)# 0 下架 1 只读不可下单(活动预告) 2 正常上架
    # 产品属性相关
    item_binds = Column(String(255), nullable=False)  # 产品的非关键属性， 格式pid:vid;
    item_sale_props = Column(String(255), nullable=False)  # 商品的销售属性列表.格式:pid:vid;pid:vid
    item_custom_props = Column(String(255), nullable=True)  # 用户自定义的属性 pid1:value1;pid2:value2 例如：“20000:优衣库”，表示“品牌:优衣库”

    # 不提供给商家修改
    item_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 创建时间
    item_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(), onupdate=getUnix_timeTuple())  # 修改时间
    item_standard_price = Column(DECIMAL(10, 2), nullable=False, default=item_price)  # 商品的标准价格
    item_level = Column(SMALLINT(1), nullable=False, default=1)  # 产品级别
    item_rate_num = Column(SMALLINT, nullable=False, default='0')  # 产品评分
    item_sale_num = Column(INTEGER, nullable=False, default=0)  # 产品销量
    item_status = Column(SMALLINT(1), nullable=False, default=1)  # 状态(0 审核未通过 1 等待审核 2 审核通过)

    def __init__(self, item_name, item_price, item_desc, item_pic_url, item_status, item_level,
                 item_rate_num, item_sale_num, item_shop_price, item_standard_price, item_vertical_market,
                 item_create_time, item_cate_name, item_cid, item_sell_pt, item_template_id, item_commodity_id,
                 item_props, item_binds, item_sale_props, ):
        """
        初始化一个商品的基本模型
        :param item_name: 商品的名称
        :param item_price: 商品的市场价格
        :param item_desc: 商品的描述
        :param item_pic_url: 商品的主图图片地址
        :param item_status: 状态(0 商家确认 1 屏蔽 2 后台确认 3 未确认 -1 删除)
        :param item_level: 产品级别
        :param item_rate_num: 产品评分
        :param item_sale_num: 商品的销量
        :param item_shop_price: 商品的店内价格
        :param item_standard_price: 商品的标准价格
        :param item_vertical_market: 商品的市场，暂时只有一个
        :param item_create_time: 商品的创建时间
        :param item_cate_name: 商品所在的类目名称
        :param item_cid: 商品的类目id，必须不是一级类目
        :param item_sell_pt: 商品的卖点
        :param item_template_id: 商品使用的模板
        :param item_commodity_id: 商品的类目
        :param item_props: 商品的关键属性
        :param item_binds: 商品的非关键属性
        :param item_sale_props: 销售属性
        """
        self.item_name = item_name
        self.item_price = item_price
        self.item_desc = item_desc
        self.item_pic_url = item_pic_url
        self.item_status = item_status
        self.item_level = item_level
        self.item_rate_num = item_rate_num
        self.item_sale_num = item_sale_num
        self.item_shop_price = item_shop_price
        self.item_standard_price = item_standard_price
        self.item_vertical_market = item_vertical_market
        self.item_create_time = item_create_time
        self.item_cate_name = item_cate_name
        self.item_cid = item_cid
        self.item_sell_pt = item_sell_pt
        self.item_template_id = item_template_id
        self.item_commodity_id = item_commodity_id
        self.item_props = item_props
        self.item_binds = item_binds
        self.item_sale_props = item_sale_props

    @property
    def simpleInfo(self):
        o = dict( {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_price": self.item_price,
            "item_desc": self.item_desc,
            "item_pic_url": self.item_pic_url,
            "item_modified": self.item_modified,
            "item_status": self.item_status,
            "item_level": self.item_level,
            "item_rate_num": self.item_rate_num,
            "item_sale_num": self.item_sale_num,
            "item_shop_price": self.item_shop_price,
            "item_standard_price": self.item_standard_price,
            "item_vertical_market": self.item_vertical_market,
            "item_custom_props": self.item_custom_props,
            "item_create_time": self.item_create_time,
            "item_cate_name": self.item_cate_name,
            "item_cid": self.item_cid,
            "item_sell_pt": self.item_sell_pt,
            "item_template_id": self.item_template_id,
            "item_commodity_id": self.item_commodity_id,
            "item_props": self.item_props,
            "item_binds": self.item_binds,
            "item_sale_props": self.item_sale_props,
        } )
        return o

    def getAllInfo(self):
        o = dict({
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_price": self.item_price,
            "item_desc": self.item_desc,
            "item_pic_url": self.item_pic_url,
            "item_modified": self.item_modified,
            "item_status": self.item_status,
            "item_level": self.item_level,
            "item_rate_num": self.item_rate_num,
            "item_sale_num": self.item_sale_num,
            "item_shop_price": self.item_shop_price,
            "item_standard_price": self.item_standard_price,
            "item_vertical_market": self.item_vertical_market,
            "item_custom_props": self.item_custom_props,
            "item_create_time": self.item_create_time,
            "item_cate_name": self.item_cate_name,
            "item_cid": self.item_cid,
            "item_sell_pt": self.item_sell_pt,
            "item_template_id": self.item_template_id,
            "item_commodity_id": self.item_commodity_id,
            "item_props": self.item_props,
            "item_binds": self.item_binds,
            "item_sale_props": self.item_sale_props,
        })
        return o


# class ItemAttributeModel(db.Model, BaseModel):
#     __tablename__ = "bao_item_attr"
#
#     def simpleInfo(self):
#         pass
#
#     def getAllInfo(self):
#         pass


