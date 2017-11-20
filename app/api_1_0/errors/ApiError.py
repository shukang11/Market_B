from ..units.common import responseErrorHandler

class ApiError(object):

    @classmethod
    def getError(self, errorCode):
        pass

class CommonError(ApiError):
    @classmethod
    def getError(self, errorCode):
        switcher = {
            # 未知错误
            999: responseErrorHandler(errorCode=999, msg="unknow_v1_error", httpCode=400),
            # 需要权限
            1000: responseErrorHandler(errorCode=1000, msg="need_permission", httpCode=403),
            # 资源不存在
            1001: responseErrorHandler(errorCode=1001, msg="url_not_found", httpCode=404),
            # 参数不全
            1002: responseErrorHandler(errorCode=1002, msg="missing_args", httpCode=400),
            # 上传的图片太大
            1003: responseErrorHandler(errorCode=1003, msg="image_too_large", httpCode=400),
            # 输入有违禁词
            1004: responseErrorHandler(errorCode=1004, msg="has_ban_word", httpCode=400),
            # 输入为空，或者输入字数不够
            1005: responseErrorHandler(errorCode=1005, msg="input_too_short", httpCode=400),
            # 相关的对象不存在，比如回复帖子时，发现小组被删掉了
            1006: responseErrorHandler(errorCode=1006, msg="target_not_fount", httpCode=400),
            # 需要验证码，验证码有误
            1007: responseErrorHandler(errorCode=1007, msg="need_captcha", httpCode=403),
            # 不支持的图片格式
            1008: responseErrorHandler(errorCode=1008, msg="image_unknow", httpCode=400),
            # 照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)
            1009: responseErrorHandler(errorCode=1009, msg="image_wrong_format", httpCode=400),
            # 访问私有图片ck验证错误
            1010: responseErrorHandler(errorCode=1010, msg="image_wrong_ck", httpCode=403),
            # 访问私有图片ck过期
            1011: responseErrorHandler(errorCode=1011, msg="image_ck_expired", httpCode=403),
            # 题目为空
            1012: responseErrorHandler(errorCode=1012, msg="title_missing", httpCode=400),
            # 描述为空
            1013: responseErrorHandler(errorCode=1013, msg="desc_missing", httpCode=400),
            # 数据库查找错误， 只需要一个结果找到了多个
            1200: responseErrorHandler(errorCode=1200, msg="multiple_results_found", httpCode=400),
            # 数据库查找错误， 一个都没找到
            1201: responseErrorHandler(errorCode=1201, msg="no_result_found", httpCode=400),

        }
        return switcher.get(errorCode or 999, {"error": None})

    @classmethod
    def args_miss(self, msg):
        return responseErrorHandler(errorCode=1002,
                                    msg=msg or "missing_args",
                                    httpCode=400)

class userBluePrintError(CommonError):
    @classmethod
    def getError(self, errorCode):
        switcher = {
            # 用户名丢失
            2000: responseErrorHandler(errorCode=2000, msg="username_missing", httpCode=400),
            # 密码错误
            2001: responseErrorHandler(errorCode=2001, msg="password_wrong", httpCode=400),
            # 手机号为空
            2002: responseErrorHandler(errorCode=2002, msg="phone_number_missing", httpCode=400),
            # 无此账号，无法找出用户
            2003: responseErrorHandler(errorCode=2003, msg="no_account", httpCode=400),
            # 登录错误，查表错误，重新登录
            2004: responseErrorHandler(errorCode=2004, msg="login_failure", httpCode=500),

        }
        return switcher.get(errorCode) or super(userBluePrintError, self).getError(errorCode=errorCode)


class CateBluePrintError(CommonError):

    @classmethod
    def getError(self, errorCode):

        switcher = {
            # 分类已存在，重复插入了
            3000: responseErrorHandler(errorCode=3000, msg="cate_already_exists", httpCode=400),
            3001: responseErrorHandler(errorCode=3001, msg="super_cate_id_cant_none_when_is_parent_is_no", httpCode=400),
            3002: responseErrorHandler(errorCode=3002, msg="cate_ids_must_be_list", httpCode=400),
        }
        return switcher.get(errorCode) or super(CateBluePrintError, self).getError(errorCode=errorCode,)

    @classmethod
    def args_miss(self, msg):
        return super(CateBluePrintError, self).args_miss(msg=msg)

class ItemBluePrintError(CommonError):

    @classmethod
    def getError(self, errorCode):
        switcher = {
            # 分类已存在，重复插入了
            4000: responseErrorHandler(errorCode=4000, msg="item_already_exists", httpCode=400),

        }
        return switcher.get(errorCode) or super(ItemBluePrintError, self).getError(errorCode=errorCode)

    @classmethod
    def args_miss(self, msg):
        return super(ItemBluePrintError, self).args_miss(msg=msg)