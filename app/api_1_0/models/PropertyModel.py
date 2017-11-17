from app.api_1_0.units.ext import db, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, String, Column, \
    ForeignKey
from app.api_1_0.models import BaseModel
from app.api_1_0.units.constantFactory import getUnix_timeTuple

class ItemCommonAttributeKeyModel(db.Model, BaseModel):
    """
    商品的一般属性，一般相同类目下的通用属性
    向上是叶子类目
    """
    __tablename__ = "bao_common_attribute_key"

    attr_id = Column(INTEGER, Sequence(start=1, increment=1, name="attr_id_sep"), primary_key=True, autoincrement=True)# 主键
    cate_id = Column(INTEGER, nullable=False, default=-1)# 所属叶子分类
    attr_name = Column(String(64), nullable=False)# 属性名称
    attr_index = Column(SMALLINT(1), nullable=False, default=0)# 属性是否可以检索;0不需要检索; 1关键字检索2范围检索,该属性应该是如果检索的话,可以通过该属性找到有该属性的商品
    attr_order = Column(SMALLINT, nullable=False, default=0)# 属性显示的顺序,数字越大越靠前,如果数字一样则按id顺序
    is_linked = Column(SMALLINT(1), nullable=False, default=0)# 是否关联,0 不关联 1关联; 如果关联, 那么用户在购买该商品时,具有有该属性相同的商品将被推荐给用户
    attr_input_type = Column(SMALLINT(1), nullable=False, default=1)# 当添加商品时,该属性的添加类别; 0为手功输入;1为选择输入;2为多行文本输入
    attr_values = Column(TEXT, nullable=False)# 即选择输入,则attr_name对应的值的取值就是该这字段值
    attr_group = Column(SMALLINT, nullable=False, default=0)# 属性分组,相同的为一个属性组应该取自goods_type的attr_group的值的顺序.
    attr_can_muti = Column(SMALLINT(1), nullable=False, default=1)# 属性是否多选; 0否; 1是 如果可以多选,则可以自定义属性,并且可以根据值的不同定不同的价
    attr_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 创建时间
    attr_update_time = Column(String(11), nullable=True, default=getUnix_timeTuple(), onupdate=getUnix_timeTuple())  # 修改时间
    attr_is_delete = Column(SMALLINT(1), nullable=False, default=1)# 是否已删除

    def __init__(self, cate_id, attr_name, attr_index, attr_order,
                 is_linked, attr_input_type, attr_values, attr_group,
                 attr_can_muti, create_time, update_time, is_delete):
        """
        初始化一个商品分类属性
        :param cate_id: 属性所属叶子分类id
        :param attr_name: 属性名
        :param attr_index: 属性是否可检索
        :param attr_order: 属性的排序优先级
        :param is_linked: 属性是否关联
        :param attr_input_type: 属性的输入类型，如果是手动输入就以attr_values为准
        :param attr_values: 输入的属性值
        :param attr_group: 属性的分组
        :param attr_can_muti: 属性是否支持多选
        :param create_time:  创建时间
        :param update_time:  最近的更新时间
        :param is_delete:  是否删除状态
        """
        self.cate_id = cate_id
        self.attr_name = attr_name
        self.attr_index = attr_index
        self.attr_order = attr_order
        self.is_linked = is_linked
        self.attr_input_type = attr_input_type
        self.attr_values = attr_values
        self.attr_group = attr_group
        self.attr_can_muti = attr_can_muti
        self.attr_create_time = create_time
        self.attr_update_time = update_time
        self.attr_is_delete = is_delete


    def simpleInfo(self) -> dict:
        return {
            "cate_id": self.cate_id,
            "attr_name": self.attr_name,
            "attr_index": self.attr_index,
            "attr_order": self.attr_order,
            "is_linked": self.is_linked,
            "attr_input_type": self.attr_input_type,
            "attr_values": self.attr_values,
            "attr_group": self.attr_group,
            "attr_can_muti": self.self.attr_can_muti,
            "create_time": self.attr_create_time,
            "update_time": self.attr_update_time,
            "is_delete": self.attr_is_delete,
        }

    def getAllInfo(self):
        o = {
            "attr_id": self.attr_id,
            "cate_id": self.cate_id,
            "attr_name": self.attr_name,
            "attr_index": self.attr_index,
            "attr_order": self.attr_order,
            "is_linked": self.is_linked,
            "attr_input_type": self.attr_input_type,
            "attr_values": self.attr_values,
            "attr_group": self.attr_group,
            "attr_can_muti": self.self.attr_can_muti,
            "create_time": self.attr_create_time,
            "update_time": self.attr_update_time,
            "is_delete": self.attr_is_delete,
        }
        return o


class ItemCommonAttributeValueModel(db.Model, BaseModel):
    """
        商品的一般属性值，一般相同类目下的通用属性值
        向上是叶子类目
        """
    __tablename__ = "bao_common_attribute_value"

    value_id = Column(INTEGER, Sequence(start=1, increment=1, name="value_id_sep"), primary_key=True, autoincrement=True)  # 主键
    attr_key_id = Column(INTEGER, nullable=False)# 对应的属性
    value = Column(String(255), nullable=False)# 对应的值
    value_create_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 创建时间
    value_update_time = Column(String(11), nullable=False, default=getUnix_timeTuple())  # 修改时间
    value_is_delete = Column(SMALLINT(1), nullable=False, default=1)  # 是否已删除

    def __init__(self, key_id, value, create_time,
                 update_time, is_delete):
        """
        商品的一般属性值
        :param key_id: 对应的属性
        :param value: 属性值
        :param create_time: 创建时间
        :param update_time: 最近的更新时间
        :param is_delete: 是否已删除状态
        """
        self.attr_key_id = key_id
        self.value = value
        self.value_create_time = create_time
        self.value_update_time = update_time
        self.value_is_delete = is_delete

    def simpleInfo(self):
        o = {
            "attr_key_id": self.key_id,
            "value": self.value,
            "value_create_time": self.create_time,
            "value_update_time": self.update_time,
            "value_is_delete": self.is_delete,
        }
        return o

    def getAllInfo(self):
        o = {
            "attr_key_id": self.key_id,
            "value": self.value,
            "value_create_time": self.create_time,
            "value_update_time": self.update_time,
            "value_is_delete": self.is_delete,
        }
        return o
