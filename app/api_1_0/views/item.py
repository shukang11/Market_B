from flask import request
from ..auth import api
from ..models.item import Item
from ..errors.ApiError import CommonError, CateBluePrintError
from ..units.common import responseErrorHandler, responseSuccessHandler
from ..errors.DAOError import NoResultFound
from ..units.constantFactory import get_list_from_column
from app.units.ext import session

@api.route("/item/<int:item_id>", methods=['GET', ])
def get_a_item(item_id):
    try:
        item = session.query(Item).filter_by(item_id=item_id).first()
        body = dict()
        body["item_id"] = item.item_id
        body["item_cate_name"] = item.item_cate_name
        body["item_cid"] = item.item_cid
        body["item_name"] = item.item_name
        body["item_price"] = str(item.item_price)
        body["item_desc"] = item.item_desc
        body["item_brand_id"] = item.item_brand_id
        body["item_sn"] = item.item_sn
        body["item_sn_type"] = item.item_sn_type
        body["item_pic_url"] = item.item_pic_url
        body["item_vertical_market"] = item.item_vertical_market
        body["item_stock_inventory"] = item.item_stock_inventory
        body["item_shop_price"] = str(item.item_shop_price)
        body["item_sell_pt"] = get_list_from_column(item.item_sell_pt)
        body["item_template_id"] = item.item_template_id
        body["item_remark"] = item.item_remark
        body["item_on_sale_state"] = item.item_on_sale_state
        body["item_binds"] = get_list_from_column(item.item_binds)
        body["item_sale_props"] = get_list_from_column(item.item_sale_props)
        body["item_custom_props"] = get_list_from_column(item.item_custom_props)
        body["item_create_time"] = item.item_create_time
        body["item_update_time"] = item.item_update_time
        body["item_standard_price"] = str(item.item_standard_price)
        body["item_level"] = item.item_level
        body["item_rate_num"] = item.item_rate_num
        body["item_sale_num"] = item.item_sale_num
        body["item_status"] = item.item_status
        return responseSuccessHandler(body=body)
    except NoResultFound:
        return CommonError.getError(errorCode=1006)

@api.route("/item", methods=['POST', ])
def insert_a_item():
    # 商品分类信息(用于定位)
    item_cate_name = request.args.get("item_cate_name")  # 产品类目名称, 优先替换掉类目id对应名称
    item_cid = request.args.get("item_cid")  # 商品类目id, 必须是提供的叶子类目
    # 商品的基本信息
    item_name = request.args.get("item_name")  # 产品名称
    item_price = request.args.get("item_price")  # 产品的市场价格
    item_desc = request.args.get("item_desc")  # 产品描述
    item_brand_id = request.args.get("item_brand_id")  # 商品所属的品牌
    item_sn = request.args.get("item_sn")  # 商品的货号
    item_sn_type = request.args.get("item_sn_type")  # 商品标号的类型
    # 商品的店家设置
    item_pic_url = request.args.get("item_pic_url")  # 产品的主图地址
    item_vertical_market = request.args.get("item_vertical_market")  # 垂直市场,暂时只有一个

    item_stock_inventory = request.args.get("item_stock_inventory")  # 商品库存量
    item_shop_price = request.args.get("item_shop_price")  # 商品的店内价格，商家填写
    item_sell_pt = request.args.get("item_sell_pt")  # 产品卖点
    item_template_id = request.args.get("item_template_id")  # 模板id
    item_remark = request.args.get("item_remark")  # 商家备注
    item_on_sale_state = request.args.get("item_on_sale_state")  # 0 下架 1 只读不可下单(活动预告) 2 正常上架
    # 产品属性相关
    item_binds = request.args.get("item_binds")  # 产品的非关键属性， 格式pid:vid;
    item_sale_props = request.args.get("item_sale_props")  # 商品的销售属性列表.格式:pid:vid;pid:vid
    item_custom_props = request.args.get("item_custom_props")  # 用户自定义的属性 pid1:value1;pid2:value2 例如：“20000:优衣库”，表示“品牌:优衣库”
    requireds = [ "item_cid", "item_name", "item_price", "item_desc",
                  "item_brand_id", "item_sn", "item_sn_type", "item_pic_url",
                  "item_vertical_market", "item_stock_inventory",
                  "item_shop_price", "item_sell_pt", "item_template_id",
                  "item_remark", "item_on_sale_state", "item_binds",
                  "item_sale_props",]
    for r in requireds:
        if request.args.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))
    item = Item()
    item.item_cate_name = item_cate_name
    item.item_cid = item_cid
    item.item_name = item_name
    item.item_price = item_price
    item.item_desc = item_desc
    item.item_brand_id = item_brand_id
    item.item_sn = item_sn
    item.item_sn_type = item_sn_type
    item.item_pic_url = item_pic_url
    item.item_vertical_market = item_vertical_market
    item.item_stock_inventory = item_stock_inventory
    item.item_shop_price = item_shop_price
    item.item_sell_pt = item_sell_pt
    item.item_template_id = item_template_id
    item.item_remark = item_remark
    item.item_on_sale_state = item_on_sale_state
    item.item_binds = item_binds
    item.item_sale_props = item_sale_props
    item.item_custom_props = item_custom_props
    try:
        session.add(item)
        session.commit()
        return responseSuccessHandler()
    except:
        return CommonError.getError(errorCode=999)

@api.route("/item", methods=['DELETE', ])
def delete_items():
    tmp = request.args.get('item_ids')
    item_ids = list(tmp)
    if isinstance(tmp, str):
        i = int(tmp)
        item_ids.append(i)
    elif isinstance(tmp, int):
        item_ids.append(tmp)
    elif isinstance(tmp, list):
        item_ids = tmp
    else:
        return CateBluePrintError.getError(errorCode=3002)
    if len(item_ids) == 0:
        return CommonError.args_miss(msg='cate_ids_required')
    tmp = session.query(Item).filter(Item.item_id.in_(item_ids)).all()
    if len(tmp) == 0:
        return CommonError.getError(errorCode=1006)
    for item in tmp:
        item.item_is_delete = 1
    session.commit()
    return responseSuccessHandler()
