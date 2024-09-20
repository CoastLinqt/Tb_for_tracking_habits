from typing import List
from datetime import datetime

from fastapi import Depends, HTTPException, UploadFile, status, Form
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, desc, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from asyncpg.exceptions import UniqueViolationError

from database import get_async_session
from models import Users, Habits, HabitTracking
from utils import validate_password, decode_jwt
from schemas import UserSchema, TokenInfo, AddHabits



oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)


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
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account isn't active"
        )

    if not validate_password(password=password, hashed_password=user.token):
        return unauth_exc

    return user


def get_current_token_payload(token: str = Depends(oauth_scheme)) -> UserSchema:

    try:
        payload = decode_jwt(
            token=token,
        )

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error"
        )

    return payload


async def get_current_active_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> Users:
    telegram_id: int | None = payload.get("telegram_id")
    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == int(telegram_id))
    )
    user = find_user_db.scalar()

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Users has not been found"
    )


async def add_habit(data: AddHabits, session: AsyncSession = Depends(get_async_session)):

    find_user_db = await session.execute(
        select(Users.id).where(Users.telegram_id == int(data.telegram_id))
    )
    result_user = find_user_db.scalar()
    # check_in_db_habit = select(Users.id).where(Users.telegram_id == int(data.telegram_id)).options(selectinload(Users.habits))
    #
    # find_habit_name_db = await session.execute(select(Habits).where((Habits.name_habit.lower())_in))

    try:

        process_add_habit = Habits(
            name_habit=data.add_habit.capitalize(),
            description=data.habit_description,
            habit_goal=data.message_habit_goal,
            user_id=result_user,
        )
        session.add(process_add_habit)
        await session.commit()

        find_habit = HabitTracking(
            habit_id=process_add_habit.id,
        )
        session.add(find_habit)
        await session.commit()

        return True

    except IntegrityError as e:
        await session.rollback()
        print("habit's already been added.")


