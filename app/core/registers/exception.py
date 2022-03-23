"""注册捕获全局异常"""
import traceback

from app.core import exceptions
from app.core.logger import logger
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse


def register_exception(app: FastAPI) -> None:
    # 自定义异常 捕获
    @app.exception_handler(exceptions.APIException)
    async def api_exception_handler(request: Request, exc: exceptions.APIException):
        logger.error(
            f"自定义异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        return JSONResponse(
            content=jsonable_encoder(
                dict(
                    code=exc.code,
                    message=exc.detail,
                )
            ),
            status_code=exc.status_code,
        )

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(
        request: Request, exc: ValidationError
    ):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        return JSONResponse(
            content=jsonable_encoder(
                dict(
                    code=5002,
                    message="Request Fail",
                    data=exc.errors(),
                )
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        # return response_code.resp_4001(message='; '.join([f"{e['loc'][1]}: {e['msg']}" for e in exc.errors()]))
        return JSONResponse(
            content=jsonable_encoder(
                dict(
                    code=4001,
                    message="Request Validation Error",
                    data=exc.errors(),
                )
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        )
        return JSONResponse(
            content=jsonable_encoder(
                dict(
                    code=500,
                    message="Internal Server Error",
                    data=None,
                )
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
