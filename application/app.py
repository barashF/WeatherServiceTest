from application.middlewares.exception_middleware import ExceptionMiddleware
from application.routers import weather, city, user
from application.di import get_update_forecast_service

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler


def _init_routers(app: FastAPI):
    app.include_router(weather.router)
    app.include_router(city.router)
    app.include_router(user.router)

def create_app():
    app = FastAPI(
        title='Weather Service',
        docs_url='/api/swagger'
    )
    
    app.add_middleware(ExceptionMiddleware)
    _init_routers(app)

    scheduler = BackgroundScheduler()
    scheduler.add_job(get_update_forecast_service().update_forecast, "interval", minutes=2)
    
    return app
