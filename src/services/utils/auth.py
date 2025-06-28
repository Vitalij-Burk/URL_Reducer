from core.db.session import get_db
from core.settings import Config
from core.utils.password import Security
from db.models import User
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from repositories.DAL.postgres.userDAL import UserDAL
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with email <{email}> not found."
        )
    return user


async def authenticate_user(email: str, password: str, session: AsyncSession):
    user: User = await _get_user_by_email_for_auth(email, session)
    if not user:
        return
    if not Security.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    try:
        payload = jwt.decode(
            token,
            Config.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[Config.ACCESS_TOKEN_ALGORITHM],
        )
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email, session)
    if not user:
        raise credentials_exception
    return user
