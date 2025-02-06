from infrastructure.repositories.city import CityRepository
from infrastructure.services.open_meteo_service import OpenMeteoWheatherService


class UpdateForecastService:
    def __init__(self, city_repository: CityRepository, open_meteo_service: OpenMeteoWheatherService):
        self.city_repository = city_repository
        self.open_meteo_service = open_meteo_service

    async def update_forecast(self):
        cities = await self.city_repository.get_all()
        for city in cities:
            try:
                forecast = await self.open_meteo_service.get_current_weather(city.latitude, 
                                                                             city.longitude,
                                                                             ["temperature_2m", 
                                                                              "windspeed_10m", 
                                                                              "relativehumidity_2m", 
                                                                              "precipitation"])
                await self.city_repository.update_forecast_city(city, forecast)

            except:
                raise Exception(f"Error update forecast for {city.name}")