from app.units.ext import db, session, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from ..models import BaseModel
from ..units.constantFactory import getUnix_timeTuple

class Brand(db.Model, BaseModel):
    """
    品牌的模型
    """
    __tablename__ = "bao_brand"

    brand_id = Column(INTEGER, Sequence(increment=1, start=1, name="brand_id_seq"), primary_key=True, autoincrement=True)# 品牌自增id
    brand_name = Column(String(22), nullable=False)# 品牌名
    brand_pic_url = Column(String(255), nullable=False)# 品牌的图片地址
    brand_cate_id = Column(String(255), nullable=False)# 所属叶子分类, 是一个数组，一对多
    brand_note = Column(String(255), nullable=False)# 品牌的简介
    brand_is_delete = Column(SMALLINT(1), nullable=False, default=1)# 默认是删除的
    brand_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 创建时间
    brand_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(), onupdate=getUnix_timeTuple())  # 修改时间
