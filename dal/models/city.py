from pydantic import BaseModel, field_validator


class City(BaseModel):
    name: str
    latitude: float
    longitude: float

    @field_validator("latitude")
    def validate_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError("Широта должна быть между -90 и 90 градусами.")
        return value
    
    @field_validator("longitude")
    def validate_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError("Долгота должна быть между -180 и 180 градусами.")
        return value
