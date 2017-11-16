from app.api_1_0 import api
from app.api_1_0.units.common import responseSuccessHandler, responseErrorHandler
from app.api_1_0.models.ClassifyModel import CateModel
from app.units.ext import db
from flask import request
from app.api_1_0.errors.ApiError import CommonError, CateBluePrintError
from app.api_1_0.errors.DAOError import NoResultFound, MultipleResultsFound


@api.route('/cate/all', methods=['GET'])
def get_all_cates():
    """
    获得所有的分类
    :return:
    """
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    try:
        results = db.session.query(CateModel).all()
        body = list()
        for result in results:
            body.append(result.getAllInfo())
        return responseSuccessHandler(body=body)
    except:
        return CommonError.getError(errorCode=999, request=path)

@api.route('/cate/<int:cate_id>', methods=['GET'])
def get_a_cate(cate_id):
    """
    获得一个分类的信息
    :param cate_id: 分类的id
    :return:
    """
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    try:
        result: CateModel
        result = db.session.query(CateModel).filter_by(cate_id=cate_id).one()
        return responseSuccessHandler(body=result.getAllInfo())
    except MultipleResultsFound:
        return CommonError.getError(errorCode=1200, request=path)

@api.route('/cate/delete', methods=['POST'])
def delete_a_cate():
    """
    删除一个分类
    :return:
    """
    path = "{0} {1}".format(request.method, request.path)  # 请求的路径
    cate_ids:list = request.args.get('cate_ids')
    if cate_ids is None:
        return CommonError.getError(errorCode=1002, request=path)
    try:
        db.session.query(CateModel).filter(CateModel.cate_id.in_(cate_ids)).delete(synchronize_session=False)
        db.session.commit()  # or session.expire_all()
        return responseSuccessHandler()
    except Exception as e:
        db.session.rollback()
        return CommonError.getError(errorCode=999)

@api.route('/cate', methods=['POST'])
def insert_cate():
    """
    插入一个分类
    :return:
    """
    path =  "{0} {1}".format(request.method, request.path) # 请求的路径
    cate_name = request.args.get('cate_name')
    super_cate_id = request.args.get('super_cate_id')
    is_parent = request.args.get('is_parent') or 0
    common_props = request.args.get('common_props')
    if super_cate_id:
        is_parent = 0
    sort_num = request.args.get('sort_num')
    if cate_name is None:
        return CommonError.getError(errorCode=1002, request=path)
    has_already = db.session.query(CateModel).filter_by(cate_name=cate_name).first()
    if has_already:
        return CateBluePrintError.getError(errorCode=3000, request=path)
    cate = CateModel(cate_name=cate_name, supercate_id=super_cate_id,
                     is_parent=is_parent, common_props=common_props, sort_num=sort_num)
    try:
        db.session.add(cate)
        db.session.commit()
        return responseSuccessHandler(body=cate.simpleInfo)
    except Exception as e:
        print(e)
        return CommonError.getError(errorCode=999, request=path)

@api.route('/cate/<int:cate_id>/edit', methods=['POST'])
def edit_cate(cate_id):
    """
        修改一个分类
        :return:
        """
    path =  "{0} {1}".format(request.method, request.path) # 请求的路径
    cate_name = request.args.get('cate_name')
    super_cate_id = request.args.get('super_cate_id')
    is_parent = request.args.get('is_parent')
    common_props = request.args.get('common_props')
    if super_cate_id:
        is_parent = 0
    sort_num = request.args.get('sort_num')
    try:
        cate: CateModel
        cate = db.session.query(CateModel).filter_by(cate_id=cate_id).one()
        if cate_name:
            cate.cate_name = cate_name
        if is_parent:
            cate.cate_is_parent = is_parent
        if common_props:
            cate.cate_common_props = common_props
        if super_cate_id:
            cate.cate_supercate_id = super_cate_id
        if sort_num:
            cate.cate_sort_num = sort_num
        db.session.commit()
        body = cate.getAllInfo()
        return responseSuccessHandler(body=body)
    except NoResultFound:
        return CommonError.getError(errorCode=999, request=path)

