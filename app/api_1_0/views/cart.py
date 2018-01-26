from flask import request
from ..auth import api
from app.models import Cart, User
from app.models import Item
from ..errors.ApiError import CommonError, OrderBluePrintError, ItemBluePrintError
from app.units.common import responseErrorHandler, responseSuccessHandler
from ..errors.DAOError import NoResultFound, MultipleResultsFound
from app.units.constantFactory import get_list_from_column
from app.units.verfy import login_required

from app import db


@api.route("/cart/add", methods=['POST', ])
@login_required
def cart_add():
    """
    添加到购物车
    :return:
    """
    params = request.values or request.get_json()
    user = User.get_user_by_token(params.get('token'))
    cart_item_id = params.get("cart_item_id")
    cart_sku_id = params.get("cart_sku_id")
    cart_add_from = params.get("cart_add_from")
    cart_sku_num = params.get("cart_sku_num")
    requires = ["cart_item_id", "cart_sku_id", "cart_sku_num", ]
    for r in requires:
        if params.get(r) is None:
            return CommonError.args_miss(msg='{}_required'.format(r))
    cart_item: Cart
    try:
        cart_item = db.session.query(Cart).filter_by(cart_item_id=cart_item_id,
                                                     cart_sku_id=cart_sku_id,
                                                     is_delete=0).one()
        if cart_item is not None:
            cart_item = cart_item
            cart_item.cart_sku_num += int(cart_sku_num)
            db.session.add(cart_item)
            db.session.commit()
    except NoResultFound:
        cart_item = Cart()
        cart_item.cart_item_id = cart_item_id
        cart_item.cart_sku_id = cart_sku_id
        cart_item.cart_add_from = int(cart_add_from) or 1
        cart_item.cart_sku_num = cart_sku_num
        cart_item.cart_item_belong = user.user_id
        cart_item.is_delete = 0
        db.session.add(cart_item)
        db.session.commit()
    except:
        return CommonError.getError(errorCode=999)
    return responseSuccessHandler()


@api.route('/cart/synchro', methods=['GET', ])
@login_required
def cart_synchro():
    """
    同步终端的购物车到终端
    :return:
    """
    user = User.get_user_by_token(request.values.get('token'))
    query = db.session.query(Cart).filter_by(cart_item_belong=user.user_id, is_delete=0).all()
    carts = list()
    if query:
        for q in query:
            cart_item: Cart = q
            carts.append({
                "id": cart_item.cart_id,
                "item_id": cart_item.cart_item_id,
                "sn": cart_item.cart_sku_id,
                "num": cart_item.cart_sku_num
            })
    return responseSuccessHandler(body=carts)


@api.route('/cart/update', methods=['POST', ])
@login_required
def cart_update_server():
    """
    更新终端中的购物车到服务器
    :return:
    """
    user: User = User.get_user_by_token(request.get_json().get('token'))
    items = request.get_json().get('items')
    items = list(items)
    try:
        sql = "DELETE FROM bao_cart WHERE cart_item_belong='{}';".format(user.user_id)
        result = db.session.execute(sql)
        for item in items:
            o = Cart()
            o.cart_id = item.get('id', 0)
            o.cart_item_id = item.get('item_id', 0)
            o.cart_sku_id = item.get('sn', 0)
            o.cart_sku_num = item.get('num', 0)
            o.cart_item_belong = user.user_id or 0
            db.session.add(o)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return CommonError.getError(errorCode=999)
    return responseSuccessHandler()
