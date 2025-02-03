from dal.interfaces.services.weather import IWeatherService
from dal.interfaces.services.city import ICityService
from dal.interfaces.repositories.city import ICityRepository
from infrastructure.services.open_meteo_service import OpenMeteoWheatherService
from infrastructure.services.city_service import CityService
from infrastructure.repositories.city import CityRepository
from infrastructure.database.db import get_db
from configuration.logger import setup_logger

from logging import Logger

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_weather_service() -> IWeatherService:
    return OpenMeteoWheatherService()

def get_city_repository(session: AsyncSession = Depends(get_db)) -> ICityRepository:
    return CityRepository(session)

def get_city_service(session: AsyncSession = Depends(get_db)) -> ICityService:
    city_repository = CityRepository(session)
    return CityService(city_repository)
