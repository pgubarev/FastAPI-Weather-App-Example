__all__ = ('setup_api', )

from fastapi import FastAPI

from conf.api_config import API_PREFIX

from .auth.views import router as auth_router
from .cities.views import router as cities_router
from .weather.views import router as weather_router

from .exception_handlers import EXCEPTION_HANDLERS_LIST


def setup_api(app: FastAPI) -> None:
    # setup routers
    app.include_router(auth_router, prefix=API_PREFIX)
    app.include_router(cities_router, prefix=API_PREFIX)
    app.include_router(weather_router, prefix=API_PREFIX)

    # setup error handlers
    for exception_class, handler in EXCEPTION_HANDLERS_LIST:
        app.add_exception_handler(exception_class, handler)
