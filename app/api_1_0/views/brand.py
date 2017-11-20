from flask import request
from ..auth import api
from ..models.brand import Brand
from ..errors.ApiError import CommonError, CateBluePrintError
from ..units.common import responseErrorHandler, responseSuccessHandler
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
    pass