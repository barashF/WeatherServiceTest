from dal.models.weather import Weather

from abc import ABC, abstractmethod
from typing import Optional


class IWeatherService(ABC):
    @abstractmethod
    async def get_current_weather(self, latitude: float, longitude: float) -> Optional[Weather]:
        pass
