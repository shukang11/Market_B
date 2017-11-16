from flask import Blueprint

api = Blueprint('api1_0', __name__)

from app.api_1_0.views import indexViews
from app.api_1_0.views import userViews
from app.api_1_0.views import cateViews
from app.api_1_0.views import itemViews
"""
GET（SELECT）：从服务器取出资源（一项或多项）。
POST（CREATE）：在服务器新建一个资源。
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
DELETE（DELETE）：从服务器删除资源。
"""