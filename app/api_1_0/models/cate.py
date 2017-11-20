from app.units.ext import db, session, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey, DECIMAL
from ..models import BaseModel
from ..units.constantFactory import getUnix_timeTuple

"""分类表，包含了分类和叶子分类"""
class Cate(db.Model, BaseModel):
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


    @classmethod
    def insert_a_cate(cls, cate_name=None,
                      super_cate_id=None, sort_num=0):
        cate = Cate()
        cate.cate_name = cate_name
        cate.cate_supercate_id = super_cate_id
        cate.cate_sort_num = sort_num
        session.add(cate)
        session.commit()
        return cate.cate_id

    @classmethod
    def get_a_cate(cls, cate_id=None, cate_name=None):
        if cate_id is None and cate_name is None:
            raise ValueError('cate_id or cate_name cant be None')
        if cate_id:
            return session.query(Cate).filter_by(cate_id=cate_id).first()
        elif cate_name:
            return session.query(Cate).filter_by(cate_name=cate_name).first()
        return None

    @classmethod
    def delete_cates(cls, cate_ids=list())->bool:
        session.query(Cate).filter(Cate.cate_id.in_(cate_ids)).delete(synchronize_session=False)
        session.commit()
        return True
