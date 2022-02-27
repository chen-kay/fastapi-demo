"""自定义异常
"""
from fastapi import status


class APIException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"
    default_code = "error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = detail
        self.code = code

    def __str__(self):
        return str(self.detail)


class TokenAuthFaild(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "无法验证凭证."


class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "认证已过期."


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "您无权执行此操作."


class NotFoundError(APIException):
    default_detail = "您所操作的对象已不存在."


class ExistsError(APIException):
    default_detail = ""
