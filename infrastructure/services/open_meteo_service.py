from configuration.config import Config
from dal.interfaces.services.weather import IWeatherService
from dal.models.weather import Weather
from typing import Optional
import httpx


class OpenMeteoWheatherService(IWeatherService):  
    def __init__(self):
        super().__init__()
        self.open_meteo_api_uri = Config.OPEN_METEO_API_URI
        self.client = httpx.AsyncClient()
        
    async def get_current_weather(self, latitude: float, longitude: float, data_params: list[str]) -> Optional[Weather]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": data_params
        }
        
        try:
            response = await self.client.get(self.open_meteo_api_uri, params=params)
            if response.status_code == 200:
                data = response.json()
                return data["current"]
            else:
                raise Exception(f"Error: Received status code {response.status_code} from Open-Meteo API")
        except httpx.RequestError as e:
            raise Exception(f"Request to OpenMeteo error: {e}")
            
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()
