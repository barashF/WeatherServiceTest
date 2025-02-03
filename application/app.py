from application.middlewares.exception_middleware import ExceptionMiddleware
from application.routers import weather, city

from fastapi import FastAPI


def _init_routers(app: FastAPI):
    app.include_router(weather.router)
    app.include_router(city.router)

def create_app():
    app = FastAPI(
        title='Weather Service',
        docs_url='/api/swagger'
    )
    
    app.add_middleware(ExceptionMiddleware)
    _init_routers(app)
    
    return app
