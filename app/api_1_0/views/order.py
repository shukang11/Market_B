from flask import request
from ..auth import api
from decimal import Decimal
from app.models import Cart
from app.models import Item, Order, OrderContainItem
from ..errors.ApiError import CommonError, OrderBluePrintError, ItemBluePrintError
from app.units.common import responseErrorHandler, responseSuccessHandler
from ..errors.DAOError import NoResultFound
from app.units.constantFactory import get_list_from_column, getMD5, get_random_num, getUnix_timeTuple, \
    getDateFromTimeTuple
from app import db
from app.models import User
from app.units.verfy import login_required


@api.route('/order/preview', methods=['POST', ])
@login_required
def order_preview():
    """
    订单预览(确认订单逻辑)
    :return:
    """
    params = request.values or request.get_json()
    items: list = params.get('goods_info')
    body = {}
    goods_list = []
    for item in items:
        # loop to check
        item: dict = item
        item_id = int(item.get('item_id', '0'))
        item_sn = str(item.get('sn', '0'))
        item_num = int(item.get('num', '0'))
        good: Item = db.session.query(Item).filter_by(item_id=item_id).first()
        if not good:  # 找不到忽略
            continue
        good_info = good.item_dict(needall=False)
        goods_list.append(good_info)

    body['goods_list'] = goods_list
    return responseSuccessHandler(body=body.copy())


@api.route('/order/add', methods=['POST', ])
@login_required
def order_add():
    """
    同时处理订单和订单关联的表
    ::: rec_address_id 收货地址id
    ::: goods_info 商品的结构化列表

    :return:
    """
    params = request.values or request.get_json()
    user: User = User.get_user_by_token(params.get('token'))
    create_ip = request.remote_addr
    rec_addr_id = params.get('rec_address_id')
    items: list = params.get('goods_info')
    requires = ["rec_address_id", "goods_info"]
    for r in requires:
        if params.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))

    # 检查收货地址

    # 检查商品列表的结构
    if not items: return CommonError.args_miss('商品信息错误!')
    append_items = []  # 商品检查成功后添加，完成后写表
    for item in items:
        item: dict = item
        item_id = int(item.get('item_id', '0'))
        item_sn = str(item.get('sn', '0'))
        item_num = int(item.get('num', 0))
        good: Item = db.session.query(Item).filter_by(item_id=item_id).first()
        good_num = good.item_stock_inventory or 0
        if good_num < item_num:
            return CommonError.args_miss('商品sn:{}库存数不足了！'.format(item_sn))
        # 检查商品通过
        good.item_stock_inventory -= item_num
        item['item_shop_price'] = good.item_shop_price
        append_items.append(item)

    try:
        # 总价
        sum_price = sum([Decimal(item['item_shop_price']) * Decimal(item['num']) for item in append_items])
        # 订单编号
        order_sn = str(getDateFromTimeTuple(formatter='%Y%m%d%H%M'))
        order_sn += get_random_num(digit=10)
        for item in append_items:
            # 添加到关系表中
            relationship: OrderContainItem = OrderContainItem()
            relationship.order_sn = order_sn
            relationship.item_sku_id = item['sn']
            relationship.item_sku_num = item['num']
            db.session.add(relationship)
        # 写order表
        order: Order = Order()
        order.order_sn = order_sn
        order.create_ip = create_ip
        order.user_id = user.user_id
        order.rec_addr_id = rec_addr_id
        order.sum_price = sum_price
        order.order_is_delete = 0
        db.session.add(order)
        db.session.commit()
        return responseSuccessHandler(body={'order_sn': order_sn})
    except Exception as e:
        print(e)
        db.session.rollback()
        return CommonError.getError(errorCode=999)


@api.route('/order/detail/<string:order_sn>', methods=['GET', ])
def order_detail(order_sn: str):
    """
    查看订单详情
    :param order_sn: 订单编号
    :return:
    """
    order_sn = order_sn or ''
    order: Order = db.session.query(Order).filter_by(order_sn=order_sn).first()
    body = {}
    if order:
        goods_info = []
        sum_price = str(order.sum_price)
        # 检索订单关联商品
        sql = "SELECT * FROM bao_rsp_order_item WHERE order_sn='{}'".format(order_sn)
        result = db.session.execute(sql)
        for r in result:
            item: Item = db.session.query(Item).filter_by(
                item_sn=r.item_sku_id
            ).first()
            if item:
                goods_info.append({
                    'good_title': item.item_name,
                    'good_price': str(item.item_shop_price),
                    'good_inventory': item.item_stock_inventory
                })
        body['sum_price'] = str(order.sum_price)
        body['order_sn'] = order_sn
        body['totol_price'] = sum_price
        body['sum_price'] = str(order.sum_price)
        body['goods_list'] = goods_info
        return responseSuccessHandler(body=body)
    else:
        return CommonError.args_miss('order_sn错误，找不到订单')

@api.route("/order/cancel", methods=['POST', ])
@login_required
def order_cancel():
    """
    取消订单流程
    :return:
    """
    params = request.values or request.get_json()
    requires = ["order_sn"]
    for r in requires:
        if params.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))
    order_sn = params.get('order_sn') or ''
    order: Order = db.session.query(Order).filter_by(order_sn=order_sn).first()
    if order:
        if order.is_payed :
            return CommonError.args_miss("You have payed this order! please request for refund!")
        try:
            order.order_is_delete = 1
            sql = "SELECT * FROM bao_rsp_order_item WHERE order_sn='{}'".format(order_sn)
            result = db.session.execute(sql)
            for r in result:
                # 归还库存
                item: Item = db.session.query(Item).filter_by(
                    item_sn=r.item_sku_id
                ).first()
                if item:
                    item.item_stock_inventory += r.item_sku_num
                else:
                    return CommonError.args_miss("cant find item by sn:{}".format(r.item_sku_id))
            db.session.commit()
            return responseSuccessHandler()
        except:
            db.session.rollback()
            return CommonError.getError(errorCode=999)
    else:
        return CommonError.args_miss("cant't find order")
