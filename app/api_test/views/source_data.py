from flask import request
from ..auth import api
from app.models import Item, Brand
from app.units.constantFactory import get_random_num
from app.units.verfy import login_required
from app.units.common import responseErrorHandler, responseSuccessHandler
import pandas
import os
from app import db

@api.route('/fill_data', methods=['POST', ])
@login_required
def fill_data():
    try:
        path = os.path.dirname(__file__)
        data: pandas.DataFrame = pandas.read_csv(os.path.join(path, 'jd_book.csv'))
        for index in data.index:
            line = data.loc[index]
            item = Item()
            item.item_cid = 3
            item.item_name = line.title
            item.item_price = line.standard_price
            item.item_standard_price = line.standard_price
            item.item_shop_price = line.shop_price
            item.item_desc = '我是商品： {}'.format(item.item_name)
            item.item_brand_id = 1
            item.item_sn = get_random_num(digit=10)
            item.item_sn_type = 1
            item.item_pic_url = line.pic_src
            item.item_vertical_market = 1
            item.item_stock_inventory = 1000
            item.item_sell_pt = '是我啊！;{}'.format(line.title)
            item.item_template_id = 1
            item.item_level = 1
            item.item_rate_num = 0
            item.item_sale_num = 0
            item.item_status = 1
            item.item_is_delete = 0
            db.session.add(item)
        db.session.commit()
        return responseSuccessHandler(body={"res": "suc"})
    except:
        return responseSuccessHandler(body={'err': 'err'})
