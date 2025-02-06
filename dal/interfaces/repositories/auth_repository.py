from dal.models.user import User

from abc import ABC, abstractmethod
from typing import Optional


class IAuthRepository(ABC):
    @abstractmethod
    async def get_user_by_username(self, username) -> Optional[User]:
        pass