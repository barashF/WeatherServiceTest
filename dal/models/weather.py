from pydantic import BaseModel


class Weather(BaseModel):
    temperature_2m: float
    windspeed_10m: float
    pressure_msl: float


class Forecast(BaseModel):
    temperature: bool
    windspeed: bool
    relativehumidity: bool
    precipitation: bool
