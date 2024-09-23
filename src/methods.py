from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from sqlalchemy.exc import IntegrityError

from database.database import get_async_session
from models import Users, Habits, HabitTracking
from utils import validate_password, decode_jwt
from schemas import UserSchema, AddHabits, EditTrackHabit


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


async def add_habit(
    data: AddHabits, session: AsyncSession = Depends(get_async_session)
):
    find_user_db = await session.execute(
        select(Users.id).where(Users.telegram_id == int(data.telegram_id))
    )
    result_user = find_user_db.scalar()

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
        print(find_habit.id)
        session.add(find_habit)
        await session.commit()

        return True

    except IntegrityError as e:
        await session.rollback()
        print("habit's already been added.")


async def function_update_track_habit(
    data: EditTrackHabit, session: AsyncSession = Depends(get_async_session)
):
    select_find_id_user = (
        select(Users.id).filter(Users.telegram_id == data.telegram_id).subquery()
    )

    select_find_habit = (
        select(Habits.id)
        .filter(
            and_(
                Habits.name_habit == data.name_habit,
                Habits.user_id == select_find_id_user.c.id,
            )
        )
        .subquery()
    )

    await session.execute(
        update(HabitTracking)
        .values(count=HabitTracking.count + 1)
        .filter(HabitTracking.habit_id == select_find_habit.c.id)
    )

    await session.commit()

    return True
