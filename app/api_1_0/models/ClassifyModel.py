from app.api_1_0.units.ext import db, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey
from app.api_1_0.models import BaseModel
from app.api_1_0.units.constantFactory import getUnix_timeTuple

class CateModel(db.Model, BaseModel):
    """分类表"""
    __tablename__ = 'bao_cate'

    cate_id = Column(INTEGER, Sequence(increment=1, start=1, name='item_spu_id_seq'), primary_key=True)
    cate_supercate_id = Column(INTEGER, nullable=False, default=0)# 类目的上级类目,为0 代表1级目录
    cate_is_parent = Column(SMALLINT(1), nullable=False, default=0)# 是否是一级类目,默认不是
    cate_name = Column(String(20), nullable=False)# 类目名称
    cate_is_delete = Column(SMALLINT(1), nullable=False, default=0)# 是否被删除
    cate_common_props = Column(String(255), nullable=True)# 如果是叶子类目，需要有一些属性值
    cate_sort_num = Column(INTEGER, nullable=False, default=0)# 类目的排列序号
    cate_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 创建时间
    cate_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(), onupdate=getUnix_timeTuple())  # 修改时间


    def __init__(self, cate_name=None, supercate_id=None,
                 is_parent=None, common_props=None,
                 create_time=None, update_time=None,
                 sort_num=0):
        self.cate_supercate_id = supercate_id
        self.cate_is_parent = is_parent
        self.cate_create_time = create_time
        self.cate_update_time = update_time
        self.cate_common_props = common_props
        self.cate_sort_num = sort_num
        self.cate_name = cate_name

    @property
    def simpleInfo(self):
        return {
            "supercate_id": int(self.cate_supercate_id),
            "is_parent": int(self.cate_is_parent),
            "common_props": str(self.cate_common_props or ''),
            "sort_num": int(self.cate_sort_num),
            "create_time": str(self.cate_create_time),
            "update_time": str(self.cate_update_time),
            "cate_name": str(self.cate_name),
        }

    def getAllInfo(self):
        o = {
            "supercate_id": int(self.cate_supercate_id),
            "is_parent": int(self.cate_is_parent),
            "common_props": str(self.cate_common_props or ''),
            "sort_num": int(self.cate_sort_num),
            "create_time": str(self.cate_create_time),
            "update_time": str(self.cate_update_time),
            "cate_name": str(self.cate_name),
            "cate_id": int(self.cate_id),
        }
        return o


class BrandModel(db.Model, BaseModel):
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

    def __init__(self, brand_name, brand_pic_url,
                 brand_cate_id, brand_note, is_delete,
                 create_time, update_time):
        self.brand_name = brand_name
        self.brand_pic_url = brand_pic_url
        self.brand_cate_id = brand_cate_id
        self.brand_note = brand_note
        self.brand_is_delete = is_delete
        self.brand_create_time = create_time
        self.brand_update_time = update_time

    def simpleInfo(self):
        return {
            "brand_name": self.brand_name,
            "brand_pic_url": self.brand_pic_url,
            "brand_cate_id": self.brand_cate_id,
            "brand_note": self.brand_note,
            "is_delete": self.brand_is_delete,
            "create_time": self.brand_create_time,
            "update_time": self.brand_update_time,
        }

    def getAllInfo(self):
        o = {
            "brand_name": self.brand_name,
            "brand_pic_url": self.brand_pic_url,
            "brand_cate_id": self.brand_cate_id,
            "brand_note": self.brand_note,
            "is_delete": self.brand_is_delete,
            "create_time": self.brand_create_time,
            "update_time": self.brand_update_time,
        }
        return o

