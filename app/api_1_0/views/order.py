from flask import request
from ..auth import api
from app.models import Cart
from app.models import Item
from ..errors.ApiError import CommonError, OrderBluePrintError, ItemBluePrintError
from app.units.common import responseErrorHandler, responseSuccessHandler
from ..errors.DAOError import NoResultFound
from app.units.constantFactory import get_list_from_column
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
        if not good:# 找不到忽略
            continue
        good_info = good.item_dict(needall=False)
        goods_list.append(good_info)
    body['goods_list'] = goods_list
    return responseSuccessHandler(body=body.copy())

@api.route('/order/add', methods=['POST', ])
def order_add():
    """
    同时处理订单和订单关联的表
    ::: rec_address_id 收货地址id
    ::: goods_info 商品的结构化列表

    :return:
    """
    params = request.values or request.get_json()
    user = User.get_user_by_token(params.get('token'))
    create_ip = request.remote_addr
    rec_addr_id = params.get('rec_address_id')
    items: list = params.get('goods_info')
    requires = ["rec_address_id", "goods_info"]
    for r in requires:
        if params.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))

    # 检查商品列表的结构
    if not items: return CommonError.args_miss('商品信息错误!')
    for item in items:
        print(item)
    return responseSuccessHandler()
