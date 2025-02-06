class Config:
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    OPEN_METEO_API_URI: str = "https://api.open-meteo.com/v1/forecast"
    DB_URI = 'sqlite+aiosqlite:///./weather.db'
    SECRET_KEY = "123"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
