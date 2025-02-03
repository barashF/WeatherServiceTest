from application.di import get_city_repository, get_city_service
from dal.models.city import City
from dal.models.weather import Forecast
from dal.interfaces.repositories.city import ICityRepository
from dal.interfaces.services.weather import IWeatherService
from dal.interfaces.services.city import ICityService
from infrastructure.database.entities.city import City as CityModel
from application.di import get_weather_service

from typing import List

from fastapi import (
    APIRouter, Depends, HTTPException, Query, status
)


router = APIRouter(
    prefix='/city',
    tags=['City']
)


@router.post('/add', summary="Добавить город")
async def add_new_city(city: City, city_repository: ICityRepository = Depends(get_city_repository),
                       weather_serv: IWeatherService = Depends(get_weather_service)) -> None:
    forecast = await weather_serv.get_current_weather(city.latitude, city.longitude, 
                                            ["temperature_2m", "windspeed_10m", "relativehumidity_2m", "precipitation"])
    await city_repository.add(city, forecast)

@router.get('/get_all', summary="Получить список доступных городов")
async def get_all_cities(city_repository: ICityRepository = Depends(get_city_repository)) -> List[str]:
    return await city_repository.get_all()

@router.get('/get_weather_by_city', summary="Получить погоду в городе")
async def get_all_cities(name: str, temperature: bool, windspeed: bool, 
                         relativehumidity: bool, precipitation: bool,
                         city_service: ICityService = Depends(get_city_service)):
    return await city_service.get_forecast_by_city(name, Forecast(
                                                            temperature=temperature,
                                                            windspeed=windspeed,
                                                            relativehumidity=relativehumidity,
                                                            precipitation=precipitation))
