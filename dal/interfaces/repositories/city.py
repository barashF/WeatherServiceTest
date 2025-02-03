from dal.models.city import City

from abc import ABC, abstractmethod
from typing import List, Optional

from uuid import UUID

class ICityRepository(ABC):
    @abstractmethod
    async def add(self, city: City) -> None:
        pass
    
    @abstractmethod
    async def get_cities_by_name(self, name: str) -> List[City]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[City]:
        pass
