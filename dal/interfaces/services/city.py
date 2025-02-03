from abc import ABC, abstractmethod
from dal.models.weather import Forecast

class ICityService(ABC):
    @abstractmethod
    async def get_forecast_by_city(self, name: str, data: Forecast):
        pass