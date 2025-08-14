from auth_sdk.auth_middleware import AuthenticationMiddleware

from ctx.app_context import AppContext
from api.routers.testing_page_router import mount_resources_for_testing_page
from utils.logger import LogRequestMiddleware
from api.routers import examples_router, health_check
from starlette.middleware import Middleware
from fastapi import FastAPI
from utils.RequestBodyMiddleware import CacheRequestBodyMiddleware


def create_app(ctx: AppContext = AppContext(), lifespan_main=None) -> FastAPI:

    oauth_client = ctx.get("oauth_client")
    logger = ctx.get("logger")

    middlewares = [
        Middleware(CacheRequestBodyMiddleware, logger=logger),
        Middleware(LogRequestMiddleware, logger=logger),
    ]

    app = FastAPI(title="AuguryGenAIAPI", lifespan=lifespan_main, middleware=middlewares)
    app.include_router(health_check.router)
    app.include_router(examples_router.router)

    app.state.context = ctx
    logger.info("context is available in app.state.context")

    mount_resources_for_testing_page(app, logger)

    return app
