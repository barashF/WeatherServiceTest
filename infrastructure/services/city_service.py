from dal.interfaces.services.city import ICityService
from dal.models.weather import Forecast
from infrastructure.repositories.city import CityRepository
from infrastructure.database.entities.city import City

class CityService(ICityService):
    def __init__(self, repository: CityRepository):
        self.repository = repository

    async def get_forecast_by_city(self, name: str, data: Forecast):
        city = await self.repository.get_cities_by_name(name)
        if not city:
            raise Exception("City not found")
        
        responce = {}
        if data.temperature:
            responce["temperature"] = city.forecast["temperature_2m"]
        if data.windspeed:
            responce["windspeed"] = city.forecast["windspeed_10m"]
        if data.relativehumidity:
            responce["relativehumidity"] = city.forecast["relativehumidity_2m"]
        if data.precipitation:
            responce["precipitation"] = city.forecast["precipitation"]
        
        return responce