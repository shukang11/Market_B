from app.units.ext import db, session, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from ..models import BaseModel
from ..units.constantFactory import getUnix_timeTuple

"""商品表"""
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
