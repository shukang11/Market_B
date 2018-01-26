from flask import request
from ..auth import api
from app.models import Activity
from ..errors.ApiError import CommonError
from app.units.verfy import login_required, permission_required
from app.units.Constant import IDENTIFY
from app.units.common import responseErrorHandler, responseSuccessHandler
from app import db


@api.route('/activity', methods=['POST'])
@permission_required(identify=IDENTIFY.ADMINISTER)
def insert_activity():
    """增"""
    activity_title = request.args.get('activity_title')
    activity_type = request.args.get('activity_type')
    activity_link = request.args.get('activity_link')
    activity_recommand = request.args.get('activity_recommand') or 0
    activity_url = request.args.get('activity_url')
    if activity_title is None:
        return CommonError.args_miss(msg='activity_title_required')
    if activity_type is None:
        return CommonError.args_miss(msg='activity_type_required')
    if activity_link is None:
        return CommonError.args_miss(msg='activity_link_required')
    if activity_url is None:
        return CommonError.args_miss(msg='activity_url_required')
    try:
        cate_id = Activity.insertActivity(activity_title, activity_url, activity_link, activity_type,
                                          activity_recommand)
        return responseSuccessHandler(body={'cate_id': cate_id})
    except:
        return CommonError.getError(errorCode=999)


@api.route('/activity/<int:activity_id>', methods=['DELETE', ])
@permission_required(identify=IDENTIFY.ADMINISTER)
def delete_activity(activity_id):
    """删"""
    if activity_id <= 0:
        return CommonError.args_miss(msg='activity_id_required')
    result: bool = Activity.deleteActivity(activity_id)
    if result:
        return responseSuccessHandler(body='delete success')
    else:
        return CommonError.getError(errorCode=999)


@api.route('/activity/<int:activity_id>', methods=['GET', ])
def query_activity(activity_id):
    """查"""
    if activity_id <= 0:
        return CommonError.args_miss(msg='activity_id_required')
    query = db.session.query(Activity)
    query = query.filter_by(activity_id=activity_id)
    query = query.filter_by(activity_is_delete=0)
    query = query.first()
    if query == None:
        return CommonError.getError(errorCode=1006)
    body = dict({
        "activity_id": query.activity_id,
        "activity_title": query.activity_title,
        "activity_link": query.activity_link,
        "activity_url": query.activity_url,
        "activity_type": query.activity_type
    })
    return responseSuccessHandler(body=body)


@api.route('/activity/<int:activity_id>', methods=['PUT', ])
@permission_required(IDENTIFY.ADMINISTER)
def update_activity(activity_id):
    """改"""
    if activity_id <= 0:
        return CommonError.args_miss(msg='activity_id_required')
    activity_title = request.args.get('activity_title')
    activity_type = request.args.get('activity_type')
    activity_link = request.args.get('activity_link')
    activity_recommand = request.args.get('activity_recommand')
    activity_url = request.args.get('activity_url')
    activity = db.session.query(Activity).filter_by(activity_id=activity_id).one()
    if activity == None:
        return CommonError.getError(errorCode=1006)
    if activity_title:
        activity.activity_title = activity_title
    elif activity_type:
        activity.activity_type = activity_type
    elif activity_recommand:
        activity.activity_recommand = activity_recommand
    elif activity_url:
        activity.activity_url = activity_url
    elif activity_link:
        activity.activity_link = activity_link
    else:
        return CommonError.args_miss(msg="you need update something..")
    db.session.commit()
    return responseSuccessHandler(body='update success')
