from flask import Blueprint, request, g, current_app
import app

api = Blueprint('api1_0', __name__)

from ..views import cate
from ..views import brand
from ..views import item
from ..views import user
from ..views import attribute
from ..views import order
from ..views import app_index
from ..views import activity
from ..views import cart
from ..views import payment

app.fetchRoute(api, "/api/v1000")


@api.before_request
def page_info_update():
    pass
    # c_page = max(int(request.args.get('page', 0)), 0)
    # c_page_limit = int(request.args.get('page_limit', current_app.config.get('PAGE_LIMIT'), 10))
    # if c_page > 0:
    #     g.page = c_page-1
    #     g.page_count = 0
    #     g.page_limit = c_page_limit


"""
GET（SELECT）：从服务器取出资源（一项或多项）。
POST（CREATE）：在服务器新建一个资源。
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
DELETE（DELETE）：从服务器删除资源。
"""



@api.route('/test', methods=['POST', 'GET', 'PATCH'])
def request_test():
    print('in test function')
    # form = TestFormer()
    # print(form['token'])
    # print(request.__dict__)
    logg = ""
    logg += "===============请求方法====================\n"
    logg += "{}\n".format(request.method)
    print(logg)
    logg = "=================header==================\n"
    logg += "{}\n".format(request.headers or 'No Header')
    print(logg)
    logg = "=================数据==================\n"
    logg += "{}\n".format(request.values.to_dict() or 'No 数据')
    print(logg)
    logg = "=================data==================\n"
    logg += "{}\n".format(request.get_json() or 'no Data')
    print(logg)
    logg = "==================================="
    print(logg)
    from app.units.common import responseSuccessHandler
    body = request.get_json() or request.values or {'msg': 'No Data'}
    return responseSuccessHandler(body=body)
