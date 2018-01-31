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

@api.route("/payment", methods=['POST', ])
@login_required
def payment():
    """
    支付接口
    :return:
    """
    params = request.values or request.get_json()
    print(params)
    requires = ["order_sn", "pay_platform", "pay_machine_code",
                "pay_system_version", "pay_app_version", "pay_type"]
    for r in requires:
        if params.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))
    order_sn = params.get('order_sn')
    pay_machine = params.get('pay_platform')  # ios/Andriod...
    pay_machine_code = params.get('pay_machine_code')  # iPhone 7,2...
    pay_system_version = params.get('pay_system_version')  # ios 10.0...
    pay_app_version = params.get('pay_app_version')  # 1.5.4...
    pay_type = params.get('pay_type')  # 0/1/2...
    remark = params.get('remark')  # 留言
    order: Order = db.session.query(Order).filter_by(order_sn=order_sn).first()
    if order:
        try:
            order.pay_platform = pay_machine
            order.pay_machine_code = pay_machine_code
            order.pay_system_version = pay_system_version
            order.pay_app_version = pay_app_version
            order.pay_type = pay_type
            order.totol_price = Decimal(order.sum_price)
            order.remark = remark
            order.is_payed = 1
            order.pay_time = getUnix_timeTuple()

            # 找到商品们，更新销量
            items = db.session.query(OrderContainItem).filter_by(order_sn=order_sn).all() or list()
            for item_by_order_sn in items:
                item_by_order_sn: OrderContainItem
                item = db.session.query(Item).filter_by(item_sn=item_by_order_sn.item_sku_id).first()
                if item:
                    item.item_sale_num += item_by_order_sn.item_sku_num
                else:
                    return CommonError.args_miss("no item find by sn:{}".format(item_by_order_sn.item_sku_id))
                pass
            db.session.commit()
            return responseSuccessHandler()
        except:
            db.session.rollback()
            return CommonError.getError(errorCode=999)
    else:
        return CommonError.args_miss("can't find order info, please check your order_sn")