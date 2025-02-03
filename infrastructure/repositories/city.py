
from dal.interfaces.repositories.city import ICityRepository
from dal.models.city import City as CityDto
from infrastructure.database.entities.city import City

from typing import List, Optional

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound


class CityRepository(ICityRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context
    
    async def add(self, city: CityDto, forecast: dict) -> None:
        result = await self.db_context.execute(
            select(City).where(
                City.latitude == city.latitude and
                City.longitude == city.longitude))
        
        entity = result.scalar_one_or_none()
        if entity:
            raise Exception("Город с такими координатами уже существует")
        
        city_entity = self._dto_to_entity(city, forecast)
        self.db_context.add(city_entity)
        await self.db_context.commit()
        await self.db_context.refresh(city_entity)
        
    async def get_all(self) -> List[CityDto]:
        result = await self.db_context.execute(select(City))
        cities = result.scalars().all()
        
        return [city.name for city in cities]
    
    async def get_cities_by_name(self, name: str) -> City:
        result = await self.db_context.execute(
            select(City).where(
                City.name == name
            ))
        return result.scalar_one_or_none()
    
    def _dto_to_entity(self, dto: CityDto, forecast: dict) -> City:
        return City(
            name=dto.name,
            latitude=dto.latitude,
            longitude=dto.longitude,
            forecast=forecast
        )
