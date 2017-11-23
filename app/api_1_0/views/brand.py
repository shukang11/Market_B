from flask import request
from ..auth import api
from ..models.brand import Brand
from ..errors.ApiError import CommonError, CateBluePrintError
from ..units.common import responseErrorHandler, responseSuccessHandler
from ..errors.DAOError import NoResultFound
from app.units.ext import session

@api.route("/brand", methods=['GET'])
def get_brands():
    page = request.args.get('page', type=int)
    brands = session.query(Brand).all()
    body = list()
    for brand in brands:
        body.append({
            "brand_id": brand.brand_id,
            "brand_name": brand.brand_name,
            "brand_pic_url": brand.brand_pic_url,
            "brand_cate_id": brand.brand_cate_id,
            "brand_note": brand.brand_note,
            "brand_is_delete": brand.brand_is_delete,
            "brand_create_time": brand.brand_create_time,
            "brand_update_time": brand.brand_update_time,
        })
    return responseSuccessHandler(body=body)

@api.route("/brand", methods=['POST'])
def insert_a_brand():
    brand_name = request.args.get("brand_name")
    brand_pic_url = request.args.get("brand_pic_url")
    brand_cate_id = request.args.get("brand_cate_id")
    brand_note = request.args.get("brand_note")
    if brand_name is None:
        return CommonError.args_miss(msg='brand_name_required')
    if brand_pic_url is None:
        return CommonError.args_miss(msg='brand_pic_url_require')
    if brand_cate_id is None:
        return CommonError.args_miss(msg='brand_cate_id_required')
    if brand_note is None:
        return CommonError.args_miss(msg='brand_note_required')
    brand = Brand()
    brand.brand_name = brand_name
    brand.brand_pic_url = brand_pic_url
    brand.brand_cate_id = brand_cate_id
    brand.brand_note = brand_note
    session.add(brand)
    session.commit()
    return responseSuccessHandler()

@api.route("/brand/<int:brand_id>", methods=['PUT'])
def update_brand_info(brand_id):
    if brand_id is None:
        return CommonError.args_miss(msg='brand_id_required')
    brand_name = request.args.get("brand_name")
    brand_pic_url = request.args.get("brand_pic_url")
    brand_cate_id = request.args.get("brand_cate_id")
    brand_note = request.args.get("brand_note")
    try:
        brand = session.query(Brand).filter_by(brand_id=brand_id).one()
        if brand_name:
            brand.brand_name = brand_name
        if brand_note:
            brand.brand_note = brand_note
        if brand_cate_id:
            brand.brand_cate_id = brand_cate_id
        if brand_pic_url:
            brand.brand_pic_url = brand_pic_url
        session.add(brand)
        body = dict({
            "brand_id": brand.brand_id,
            "brand_name": brand.brand_name,
            "brand_pic_url": brand.brand_pic_url,
            "brand_cate_id": brand.brand_cate_id,
            "brand_note": brand.brand_note,
            "brand_is_delete": brand.brand_is_delete,
            "brand_create_time": brand.brand_create_time,
        })
        return responseSuccessHandler(body=body)
    except NoResultFound:
        return CommonError.getError(errorCode=1006)