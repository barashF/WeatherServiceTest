from infrastructure.database.entities.base import Base
from sqlalchemy import Column, Float, String, JSON


class City(Base):
    __tablename__ = 'Cities'
    
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    forecast = Column(JSON, nullable=False)
