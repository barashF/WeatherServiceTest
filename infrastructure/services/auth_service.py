from dal.models.user import User
from infrastructure.database.entities.user import User as UserDto
from infrastructure.repositories.auth_repository import AuthRepository
from configuration.config import Config

from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository
        self.config = Config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    async def authenticate_user(self, username: str, password: str):
        user = await self.auth_repository.get_user_by_username(username)
        if not user or self.verify_password(password, user.password):
            False
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, self.config.ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await self.auth_repository.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    
    async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
        if current_user["disabled"]:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    async def register_user(self, username, password):
        hashed_password = self.get_password_hash(password)
        return await self.auth_repository.add_user(UserDto(username=username, password=hashed_password))
