from application.di import get_auth_service
from dal.models.user import User
from infrastructure.database.entities.user import User as UserDto
from infrastructure.services.auth_service import AuthService
from configuration.config import Config

from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/register', summary="регистрация")
async def register(user: User, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.register_user(user.username, user.password)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/items/")
async def read_items(current_user: UserDto = Depends(get_auth_service().get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]