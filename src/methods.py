from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Users
from fastapi import Depends, HTTPException, UploadFile, status, Form
from sqlalchemy import delete, desc, func, select
from typing import List
from utils import validate_password


async def authenticate_user(
    telegram_id: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session),
):

    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == int(telegram_id))
    )

    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )

    result = find_user_db.first()
    if result is None:
        return unauth_exc

    data_info: List[dict] = [i.__dict__ for i in result]

    if not validate_password(password=password, hashed_password=data_info[0]["token"]):
        return unauth_exc

    return data_info

