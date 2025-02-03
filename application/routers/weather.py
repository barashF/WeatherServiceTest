from application.di import get_weather_service
from dal.interfaces.services.weather import IWeatherService
from dal.models.weather import Weather

from fastapi import (
    APIRouter, Depends, HTTPException, Query, status
)


router = APIRouter(
    prefix='/weather',
    tags=['Weather']
)


@router.get(
    '/get_current_weather',
    summary="Получить текущую погоду")
async def get_weather(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    weather_serv: IWeatherService = Depends(get_weather_service)) -> Weather:
    
    weather = await weather_serv.get_current_weather(latitude, longitude, 
                                                     ["temperature_2m", "windspeed_10m", "pressure_msl"])
    return weather
