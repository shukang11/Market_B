from app.api_1_0.units.ext import db, INTEGER, \
    TEXT, SMALLINT, Sequence, FLOAT, DATE, String, Column, \
    ForeignKey
import datetime

class ItemUniqueAttributeModel(db.Model):
    """
    商品的关键属性-唯一确定商品的属性
    向上是叶子类目
    """
    __tablename__ = "bao__unique_attribute"

    attr_id = Column(INTEGER, Sequence(start=1), primary_key=True, autoincrement=True)# 主键
    cate_id = Column(INTEGER, nullable=False, default=-1)# 所属叶子分类
    attr_name = Column(String(64), nullable=False)# 属性名称
    attr_index = Column(SMALLINT(1), nullable=False, default=0)# 属性是否可以检索;0不需要检索; 1关键字检索2范围检索,该属性应该是如果检索的话,可以通过该属性找到有该属性的商品
    attr_order = Column(SMALLINT(5), nullable=False, default=0)# 属性显示的顺序,数字越大越靠前,如果数字一样则按id顺序
    is_linked = Column(SMALLINT(1), nullable=False, default=0)# 是否关联,0 不关联 1关联; 如果关联, 那么用户在购买该商品时,具有有该属性相同的商品将被推荐给用户
    attr_input_type = Column(SMALLINT(1), nullable=False, default=1)# 当添加商品时,该属性的添加类别; 0为手功输入;1为选择输入;2为多行文本输入
    attr_values = Column(TEXT, nullable=False)# 即选择输入,则attr_name对应的值的取值就是该这字段值
    attr_group = Column(SMALLINT(1), nullable=False, default=0)# 属性分组,相同的为一个属性组应该取自goods_type的attr_group的值的顺序.
    attr_can_muti = Column(SMALLINT(1), nullable=False, default=1)# 属性是否多选; 0否; 1是 如果可以多选,则可以自定义属性,并且可以根据值的不同定不同的价

    def __init__(self, cate_id, attr_name, attr_index, attr_order,
                 is_linked, attr_input_type, attr_values, attr_group,
                 attr_can_muti):
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
        """