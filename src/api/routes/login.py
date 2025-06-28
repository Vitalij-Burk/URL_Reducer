from datetime import timedelta

from core.db.session import get_db
from core.settings import Config
from core.utils.auth import AccessToken
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas.auth import Token
from services.utils.auth import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_by_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AccessToken.create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
