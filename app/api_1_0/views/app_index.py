from flask import request, current_app, render_template, g
from ..auth import api
from ..errors.ApiError import CommonError
from app.units.common import responseSuccessHandler
from ..errors.DAOError import NoResultFound
from app import db
from app.units.constantFactory import getMD5, getUnix_timeTuple, get_random_num
from app.models import Activity, Item


@api.route("/index/banner", methods=['GET', ])
def index_banner():
    """获得导航栏信息"""
    banners = list()
    query = db.session.query(Activity).filter_by(activity_type=10)
    query = query.filter_by(activity_is_delete=0)
    query = query.order_by(Activity.activity_recommand.desc())
    query = query.order_by(Activity.activity_create_time.desc())
    pics = query.limit(5).all()
    for pic in pics:
        banner = dict({
            "pic": pic.activity_url or '',
            "title": pic.activity_title or '',
            "is_recommend": pic.activity_recommand,
            "link": pic.activity_link or '',
            "id": pic.activity_id
        })
        banners.append(banner)
    return responseSuccessHandler(body=banners)


@api.route('/index/modules', methods=['GET', ])
def index_modules():
    """获得模块信息"""
    modules = ('今日推荐', '新闻', '测试', '测试01', '我是绯闻', '娱乐新闻', '今日特价', '秒杀抢购')
    body = list()
    for mo in modules:
        body.append(dict(
            icon_name=mo,
            icon_url='http://url_path/{}'.format(get_random_num()),
            icon_idf=get_random_num(digit=2))
        )
    return responseSuccessHandler(body=body)


@api.route('/index/recommand', methods=['GET', ])
def index_recommand_items():
    page = max(int(request.args.get('page', 1)), 0)
    page_limit = int(request.args.get('page_limit', current_app.config.get('PAGE_LIMIT'), 10))
    offset = page_limit * (page - 1)
    # 目前是销量和创建时间排序推荐
    query = db.session.query(Item).filter_by(item_is_delete=0)
    query = query.filter_by(item_vertical_market=1)
    query = query.order_by(Item.item_sale_num.desc())
    query = query.order_by(Item.item_create_time.desc())
    query = query.limit(page_limit).offset(offset)
    query = query.all()
    result = list()
    for q in query:
        result.append(q.item_dict())
    print("输出了{}个推荐商品".format(len(result)))
    return responseSuccessHandler(body=result)
