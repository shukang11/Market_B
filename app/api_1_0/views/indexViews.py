from app.api_1_0 import api
from app.api_1_0.units.common import responseSuccessHandler, responseErrorHandler

@api.route('/index/banner', methods=['GET'])
def get_index_banner():
    """
    获得app首页轮播图内容
    :return:
    """
    values = ["http://img.zcool.cn/community/010f87596f13e6a8012193a363df45.jpg@2o.jpg",
              "http://pic4.nipic.com/20091217/3885730_124701000519_2.jpg",
              "http://img3.redocn.com/tupian/20150425/suyahuawenbiankuangkapianbeijingsucai_3937892.jpg"]
    body = list()
    for value in values:
        body.append({
            "pic":value,
            "type": "1",
            "alt": "https://www.baidu.com"
        })
    return responseSuccessHandler(statusCode=202, body=body)

