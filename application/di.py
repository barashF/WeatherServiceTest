from dal.interfaces.services.weather import IWeatherService
from dal.interfaces.services.city import ICityService
from dal.interfaces.repositories.city import ICityRepository
from dal.interfaces.repositories.auth_repository import IAuthRepository
from infrastructure.services.open_meteo_service import OpenMeteoWheatherService
from infrastructure.services.auth_service import AuthService
from infrastructure.repositories.city import CityRepository
from infrastructure.repositories.auth_repository import AuthRepository
from infrastructure.database.db import get_db
from businesslogic.services.update_forecast_service import UpdateForecastService
from configuration.logger import setup_logger


from logging import Logger

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_weather_service() -> IWeatherService:
    return OpenMeteoWheatherService()

def get_city_repository(session: AsyncSession = Depends(get_db)) -> ICityRepository:
    return CityRepository(session)

def get_update_forecast_service(session: AsyncSession = Depends(get_db)):
    city_repository = CityRepository(session)
    open_meteo_service = OpenMeteoWheatherService()
    
    return UpdateForecastService(city_repository, open_meteo_service)

def get_auth_service(session: AsyncSession = Depends(get_db)):
    auth_repository = AuthRepository(session)
    return AuthService(auth_repository)