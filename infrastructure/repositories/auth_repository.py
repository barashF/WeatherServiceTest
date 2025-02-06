from dal.models.user import User as UserDto
from dal.interfaces.repositories.auth_repository import IAuthRepository
from infrastructure.database.entities.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional


class AuthRepository(IAuthRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context
    
    async def get_user_by_username(self, username) -> Optional[User]:
        result = await self.db_context.execute(
            select(User).where(
                User.username == username))
        user = result.scalar_one_or_none()
        return user
    
    async def add_user(self, user: User) -> None:
        if await self.get_user_by_username(user.username):
            raise Exception("Пользователь с таким ником уже существует")
            
        self.db_context.add(user)
        await self.db_context.commit()
        await self.db_context.refresh(user)
        return user


