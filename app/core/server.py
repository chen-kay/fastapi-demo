"""FastAPI Application"""
from app.core.config import settings
from app.core.registers import event, exception, hook, router
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        redoc_url=settings.REDOC_URL,
    )

    # 注册路由
    router.register_router(app)
    # 注册捕获全局异常
    exception.register_exception(app)
    # 注册请求拦截
    hook.register_hook(app)
    # 注册事件
    event.register_event(app)

    return app
