from flask import request
from ..auth import api
from ..models.cate import Cate
from ..errors.ApiError import CommonError, CateBluePrintError
from ..units.common import responseErrorHandler, responseSuccessHandler
from app.units.ext import session

@api.route("/cate", methods=['POST', ])
def insert_a_cate():
    cate_name = request.args.get('cate_name')
    super_id = request.args.get('super_id')
    sort_num = request.args.get('sort_num')
    if cate_name is None:
        return CommonError.args_miss(msg='cate_name_required')
    if super_id is None:
        return CommonError.args_miss(msg='super_id_required')
    if Cate.get_a_cate(cate_name=cate_name):
        return CateBluePrintError.getError(errorCode=3000)
    try:
        cate_id = Cate.insert_a_cate(cate_name, super_id,sort_num)
        return responseSuccessHandler(body={'cate_id':cate_id})
    except:
        return CommonError.getError(errorCode=999)

@api.route("/cate", methods=['DELETE'])
def delete():
    tmp = request.args.get('cate_ids')
    cate_ids = list(tmp)
    if isinstance(tmp, str):
        i = int(tmp)
        cate_ids.append(i)
    elif isinstance(tmp, int):
        cate_ids.append(tmp)
    elif isinstance(tmp, list):
        cate_ids = tmp
    else:
        return CateBluePrintError.getError(errorCode=3002)
    if len(cate_ids) == 0:
        return CommonError.args_miss(msg='cate_ids_required')
    if Cate.delete_cates(cate_ids=tmp):
        return responseSuccessHandler()

@api.route("/cate/root", methods=['GET'])
def get_cates():
    result = session.query(Cate).filter_by(cate_supercate_id=0).all()
    body = list()
    for r in result:
        body.append({
            "cate_id": r.cate_id,
            "cate_supercate_id": r.cate_supercate_id,
            "cate_is_parent": r.cate_is_parent,
            "cate_name": r.cate_name,
            "cate_is_delete": r.cate_is_delete,
            "cate_common_props": r.cate_common_props,
            "cate_sort_num": r.cate_sort_num,
            "cate_create_time": r.cate_create_time,
            "cate_update_time": r.cate_update_time,
        })
    return responseSuccessHandler(body=body)

@api.route("/cate/<int:cate_id>", methods=['GET', ])
def get_a_cates(cate_id):
    t_cate:Cate = Cate.query.get_or_404(cate_id)
    if cate_id is None:
        return CommonError.args_miss(msg='cate_id_required')
    try:
        r = Cate.get_a_cate(rcate_id=cate_id)
        if isinstance(r, Cate):
            body = dict({
            "cate_id": r.cate_id,
            "cate_supercate_id": r.cate_supercate_id,
            "cate_is_parent": r.cate_is_parent,
            "cate_name": r.cate_name,
            "cate_is_delete": r.cate_is_delete,
            "cate_common_props": r.cate_common_props,
            "cate_sort_num": r.cate_sort_num,
            "cate_create_time": r.cate_create_time,
            "cate_update_time": r.cate_update_time,
            })
            return responseSuccessHandler(body=body)
        return CommonError.getError(errorCode=1006)
    except:
        return CommonError.getError(errorCode=999)

@api.route("/cate/super", methods=['GET', ])
def get_super_cate_info():
    """
    获得一个分类的父节点
    :return:
    """
    cate_id = request.args.get('cate_id')
    if cate_id is None:
        return  CommonError.args_miss(msg='cate_id_required')
    cate: Cate = Cate.get_a_cate(cate_id=cate_id)
    if cate is None:
        return CommonError.getError(errorCode=1006)
    su = Cate.get_a_cate(cate_id=cate.cate_supercate_id)
    if su:
        body = dict({
            "cate_id": su.cate_id,
            "cate_supercate_id": su.cate_supercate_id,
            "cate_is_parent": su.cate_is_parent,
            "cate_name": su.cate_name,
            "cate_is_delete": su.cate_is_delete,
            "cate_common_props": su.cate_common_props,
            "cate_sort_num": su.cate_sort_num,
            "cate_create_time": su.cate_create_time,
            "cate_update_time": su.cate_update_time,
        })
        return responseSuccessHandler(body=body)
    return responseSuccessHandler(body={})
