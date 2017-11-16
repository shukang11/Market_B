from flask import request
from app.api_1_0 import api
from app.api_1_0.units.ext import db
from app.api_1_0.models.ItemModel import ItemModel
from app.api_1_0.units.common import responseSuccessHandler, responseErrorHandler
from app.api_1_0.errors.ApiError import CommonError, ItemBluePrintError
from app.api_1_0.errors.DAOError import NoResultFound, MultipleResultsFound


@api.route('/item/<item_id>', methods=['GET', ])
def get_item_info(item_id):
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    item: ItemModel
    try:
        item = db.session.query(ItemModel).filter_by(item_id=item_id).one()
        body = item.simpleInfo or dict()
        return responseSuccessHandler(body=body)
    except NoResultFound:
        return CommonError.getError(errorCode=1201)


@api.route('/item', methods=['POST', ])
def insert_a_item():
    """
    添加一个商品
    :return:
    """
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    item: ItemModel
    """check params"""
    check = ("item_name", "item_price", "item_desc",
             "item_pic_url", "item_shop_price",
             "item_standard_price",
             "item_cid", "item_sell_pt",
             "item_commodity_id", "item_props", "item_binds",
             "item_sale_props")
    for c in check:
        print('{0} --> {1}'.format(c, request.args.get(c)))
        if request.args.get(c) is None:
            return responseErrorHandler(errorCode=1002, msg="{} is required".format(c), httpCode=401,request=path)

    item_name = request.args.get("item_name", type=str)
    item_price = request.args.get("item_price", type=str)
    item_desc = request.args.get("item_desc", type=str)
    item_pic_url = request.args.get("item_pic_url", type=str)
    item_modified = request.args.get("item_modified")
    item_status = request.args.get("item_status", type=int, default=3)
    item_level = request.args.get("item_level") or 1
    item_rate_num = request.args.get("item_rate_num")
    item_sale_num = request.args.get("item_sale_num")
    item_shop_price = request.args.get("item_shop_price")
    item_standard_price = request.args.get("item_standard_price")
    item_vertical_market = request.args.get("item_vertical_market") or 0
    item_custom_props = request.args.get("item_custom_props")
    item_create_time = request.args.get("item_create_time")
    item_cate_name = request.args.get("item_cate_name")
    item_cid = request.args.get("item_cid")
    item_sell_pt = request.args.get("item_sell_pt")
    item_template_id = request.args.get("item_template_id")
    item_commodity_id = request.args.get("item_commodity_id") or 0
    item_props = request.args.get("item_props") or ''
    item_binds = request.args.get("item_binds") or ''
    item_sale_props = request.args.get("item_sale_props") or ''
    try:
        has_ = db.session.query(ItemModel).filter_by(item_name=item_name, item_cid=item_cid).first()
        if has_:
            return ItemBluePrintError.getError(errorCode=4000, request=path)
        item = ItemModel(item_name=item_name,
                         item_price=item_price,
                         item_desc=item_desc,
                         item_pic_url=item_pic_url,
                         item_status=item_status,
                         item_level=item_level,
                         item_rate_num=item_rate_num,
                         item_sale_num=item_sale_num,
                         item_shop_price=item_shop_price,
                         item_standard_price=item_standard_price,
                         item_vertical_market=item_vertical_market,
                         item_create_time=item_create_time,
                         item_cate_name=item_cate_name,
                         item_sell_pt=item_sell_pt,
                         item_template_id=item_template_id,
                         item_props=item_props,
                         item_binds=item_binds,
                         item_sale_props=item_sale_props,
                         item_cid=item_cid,
                         item_commodity_id=item_commodity_id)
        if item_modified:
            item.item_modified = item_modified
        if item_custom_props:
            item.item_custom_props = item_custom_props
        db.session.add(item)
        db.session.commit()
        return responseSuccessHandler()
    except Exception as e:
        print(e)
        return CommonError.getError(errorCode=999, request=path)

@api.route('/item/<int:item_id>', methods=['PUT', ])
def edit_a_item(item_id):
    """
    修改一个商品的信息
    :return:
    """
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    try:
        item: ItemModel
        item = db.session.query(ItemModel).filter_by(item_id=item_id).one()
        """check params"""
        check = ("item_name", "item_price", "item_desc",
                 "item_pic_url", "item_shop_price",
                 "item_standard_price",
                 "item_cid", "item_sell_pt",
                 "item_commodity_id", "item_props", "item_binds",
                 "item_sale_props")
        for c in check:
            print('{0} --> {1}'.format(c, request.args.get(c)))
            if request.args.get(c) is None:
                return responseErrorHandler(errorCode=1002, msg="{} is required".format(c), httpCode=401, request=path)

        item_name = request.args.get("item_name", type=str)
        item_price = request.args.get("item_price", type=str)
        item_desc = request.args.get("item_desc", type=str)
        item_pic_url = request.args.get("item_pic_url", type=str)
        item_modified = request.args.get("item_modified")
        item_status = request.args.get("item_status", type=int)
        item_level = request.args.get("item_level") or 1
        item_rate_num = request.args.get("item_rate_num")
        item_sale_num = request.args.get("item_sale_num")
        item_shop_price = request.args.get("item_shop_price")
        item_standard_price = request.args.get("item_standard_price")
        item_vertical_market = request.args.get("item_vertical_market")
        item_custom_props = request.args.get("item_custom_props")
        item_create_time = request.args.get("item_create_time")
        item_cate_name = request.args.get("item_cate_name")
        item_cid = request.args.get("item_cid")
        item_sell_pt = request.args.get("item_sell_pt")
        item_template_id = request.args.get("item_template_id")
        item_commodity_id = request.args.get("item_commodity_id")
        item_props = request.args.get("item_props")
        item_binds = request.args.get("item_binds")
        item_sale_props = request.args.get("item_sale_props")
        try:
            if item_name:
                item.item_name = item_name
            if item_price:
                item.item_price = item_price
            if item_desc:
                item.item_desc = item_desc
            if item_pic_url:
                item.item_pic_url = item_pic_url
            if item_modified:
                item.item_modified = item_modified
            if item_status:
                item.item_status = item_status
            if item_level:
                item.item_level = item_level
            if item_rate_num:
                item.item_rate_num = item_rate_num
            if item_sale_num:
                item.item_sale_num = item_sale_num
            if item_shop_price:
                item.item_shop_price = item_shop_price
            if item_standard_price:
                item.item_standard_price = item_standard_price
            if item_vertical_market:
                item.item_vertical_market = item_vertical_market
            if item_custom_props:
                item.item_custom_props = item_custom_props
            if item_create_time:
                item.item_create_time = item_create_time
            if item_cate_name:
                item.item_cate_name = item_cate_name
            if item_cid:
                item.item_cid = item_cid
            if item_sell_pt:
                item.item_sell_pt = item_sell_pt
            if item_template_id:
                item.item_template_id = item_template_id
            if item_commodity_id:
                item.item_commodity_id = item_commodity_id
            if item_props:
                item.item_props = item_props
            if item_binds:
                item.item_binds = item_binds
            if item_sale_props:
                item.item_sale_props = item_sale_props
            db.session.commit()
            return responseSuccessHandler()
        except Exception as e:
            print(e)
            return CommonError.getError(errorCode=999, request=path)
    except NoResultFound:
        return CommonError.getError(errorCode=1201, request=path)
    except MultipleResultsFound:
        return CommonError.getError(errorCode=1200, request=path)

@api.route('/item', methods=['DELETE', ])
def delete_a_item():
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    item: ItemModel
    item_ids: list = request.args.get('item_ids')
    if item_ids is None:
        return CommonError.getError(errorCode=1002, request=path)
    try:
        db.session.query(ItemModel).filter(ItemModel.item_id.in_(item_ids)).delete(synchronize_session=False)
        db.session.commit()  # or session.expire_all()
        return responseSuccessHandler()
    except Exception as e:
        print(e)
        return CommonError.getError(errorCode=999, request=path)
