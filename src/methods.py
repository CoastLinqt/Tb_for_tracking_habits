from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Users
from fastapi import Depends, HTTPException, UploadFile, status, Form
from sqlalchemy import delete, desc, func, select
from typing import List
from utils import validate_password, decode_jwt
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from schemas import UserSchema, TokenInfo


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login/',)


async def authenticate_user(

    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session),
):
    telegram_id = username

    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == int(telegram_id))
    )

    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )

    user = find_user_db.scalar()
    if user is None:
        return unauth_exc

    if not user.is_active:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account isn't active")

    if not validate_password(password=password, hashed_password=user.token):
        return unauth_exc

    return user


def get_current_token_payload(token: str = Depends(oauth_scheme)) -> UserSchema:

    try:
        payload = decode_jwt(token=token,)

    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error")

    return payload


async def get_current_active_auth_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(get_async_session)
) -> Users:
    telegram_id: int | None = payload.get("telegram_id")
    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == int(telegram_id))
    )
    user = find_user_db.scalar()

    if user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Users has not been found')
