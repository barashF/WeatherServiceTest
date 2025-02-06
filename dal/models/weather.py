from pydantic import BaseModel
from typing import Optional


class Weather(BaseModel):
    temperature_2m: float
    windspeed_10m: float
    pressure_msl: float

class Forecast(BaseModel):
    temperature: bool
    windspeed: bool
    relativehumidity: bool
    precipitation: bool

class WeatherResponse(BaseModel):
    temperature: Optional[float] = None
    windspeed: Optional[float] = None
    relativehumidity: Optional[float] = None
    precipitation: Optional[float] = None

    def to_response(self):
        return self.dict(exclude_none=True)