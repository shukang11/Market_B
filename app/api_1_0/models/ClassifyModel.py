from app.api_1_0.units.ext import db, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, DATE, String, Column, \
    ForeignKey
from app.api_1_0.units.constantFactory import getMD5
class CateModel(db.Model):
    """分类表"""
    __tablename__ = 'bao_cate'

    cate_id = Column(INTEGER, Sequence(increment=1, start=1, name='item_spu_id_seq'), primary_key=True)
    cate_supercate_id = Column(INTEGER, nullable=False, default=0)# 类目的上级类目,为0 代表1级目录
    cate_is_parent = Column(SMALLINT, nullable=False, default=0)# 是否是一级类目,默认不是
    cate_name = Column(String(20), nullable=False)# 类目名称
    cate_is_delete = Column(SMALLINT, nullable=False, default=0)# 是否被删除
    cate_common_props = Column(String(255), nullable=True)# 如果是叶子类目，需要有一些属性值
    cate_sort_num = Column(INTEGER, nullable=False, default=0)# 类目的排列序号

    def __init__(self, cate_name=None, supercate_id=None, is_parent=None, common_props=None, sort_num=0):
        self.cate_supercate_id = supercate_id
        self.cate_is_parent = is_parent
        self.cate_common_props = common_props
        self.cate_sort_num = sort_num
        self.cate_name = cate_name

    @property
    def simpleInfo(self):
        return {
            "supercate_id": int(self.cate_supercate_id),
            "is_parent": bool(self.cate_is_parent),
            "common_props": str(self.cate_common_props or ''),
            "sort_num": int(self.cate_sort_num),
            "cate_name": str(self.cate_name),
        }

    def getAllInfo(self):
        o = {
            "supercate_id": int(self.cate_supercate_id),
            "is_parent": int(self.cate_is_parent),
            "common_props": str(self.cate_common_props or ''),
            "sort_num": int(self.cate_sort_num),
            "cate_name": str(self.cate_name),
            "cate_id": int(self.cate_id),
        }
        return o