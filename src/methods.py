import datetime


from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database.database import get_async_session
from models import Users, Habits, HabitTracking
from utils import validate_password, decode_jwt
from schemas import UserSchema, AddHabits, EditTrackHabit, TelegramId, SetReminder


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


async def function_user_check_db(
    telegram_id: TelegramId, session: AsyncSession = Depends(get_async_session)
):
    print(telegram_id.telegram_id)
    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == telegram_id.telegram_id)
    )
    result = find_user_db.scalar()
    print(result)

    return result


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


async def function_edit_habit(
    data: EditTrackHabit, session: AsyncSession = Depends(get_async_session)
):
    try:
        find_id_user = (
            select(Users.id).filter(Users.telegram_id == data.telegram_id).subquery()
        )

        if data.habit_goal and data.description:
            await session.execute(
                update(Habits)
                .values(description=data.description, habit_goal=data.habit_goal)
                .filter(
                    and_(
                        Habits.name_habit == data.name_habit,
                        Habits.user_id == find_id_user.c.id,
                    )
                )
            )
        else:
            if data.habit_goal:
                await session.execute(
                    update(Habits)
                    .values(habit_goal=data.habit_goal)
                    .filter(
                        and_(
                            Habits.name_habit == data.name_habit,
                            Habits.user_id == find_id_user.c.id,
                        )
                    )
                )

            elif data.description:
                await session.execute(
                    update(Habits)
                    .values(description=data.description)
                    .filter(
                        and_(
                            Habits.name_habit == data.name_habit,
                            Habits.user_id == find_id_user.c.id,
                        )
                    )
                )

        await session.commit()

        return True
    except IntegrityError as e:
        await session.rollback()
        print("Error add.")


async def function_track_all(
    telegram_id: TelegramId, session: AsyncSession = Depends(get_async_session)
):
    find = await session.execute(
        select(Users)
        .where(Users.telegram_id == telegram_id.telegram_id)
        .options(selectinload(Users.habits))
    )
    find_scalar = find.scalars()
    print(find_scalar,'1')
    for items in find_scalar:
        result_items_id = [habit_info.id for habit_info in items.habits]
        print(result_items_id,'2')

        find_in = await session.execute(
            select(HabitTracking).where(
                and_(HabitTracking.habit_id.in_(result_items_id), HabitTracking.count < 21)
            )
        )
        find_in_scalar = find_in.scalars()

        result = [
            {
                "name_habit": f"{i.habits.name_habit}",
            }
            for i in find_in_scalar
        ]

        return result


async def function_process_habits(
    telegram_id: TelegramId, session: AsyncSession = Depends(get_async_session)
):
    try:
        find = await session.execute(
            select(Users)
            .where(Users.telegram_id == telegram_id.telegram_id)
            .options(selectinload(Users.habits))
        )
        result_db = find.scalars()

        if result_db:
            for i in result_db:
                result = [
                    {
                        "name_habit": f"{e.name_habit}",
                        "description": f"{e.description}",
                        "habit_goal": f"{e.habit_goal}",
                    }
                    for e in i.habits
                ]
                return result

    except IntegrityError as e:
        await session.rollback()
        print("Error find info habit.")


async def function_habit_stats(
    telegram_id: TelegramId, session: AsyncSession = Depends(get_async_session)
):
    find_user = (
        select(Users.id).where(Users.telegram_id == telegram_id.telegram_id)
    ).subquery()

    result = await session.execute(
        select(Habits.name_habit, HabitTracking.count).select_from(HabitTracking)
        .join(Habits)
        .where(Habits.user_id == find_user.c.id)
    )

    finish = result.all()

    result = [{"name_habit": i[0], "count": i[1]} for i in finish]

    return result


async def function_delete_habit(
    data_habit: EditTrackHabit, session: AsyncSession = Depends(get_async_session)
):
    try:
        find_id_user = (
            select(Users.id)
            .filter(Users.telegram_id == data_habit.telegram_id)
            .subquery()
        )

        await session.execute(
            delete(Habits).where(
                and_(
                    Habits.name_habit == data_habit.name_habit,
                    Habits.user_id == find_id_user.c.id,
                )
            )
        )
        await session.commit()
        return True

    except IntegrityError as e:
        await session.rollback()
        print("Error delete.")


async def function_update_track_habit(
    data: EditTrackHabit, session: AsyncSession = Depends(get_async_session)
):

    select_find_id_user = (
        select(Users).filter(Users.telegram_id == data.telegram_id).subquery()
    )

    select_find_habit = (
        select(Habits)
        .filter(
            and_(
                Habits.name_habit == data.name_habit,
                Habits.user_id == select_find_id_user.c.id,
            )
        )

    ).subquery()

    await session.execute(
        update(HabitTracking)
        .values(count=HabitTracking.count + 1)
        .filter(HabitTracking.habit_id == select_find_habit.c.id)
    )

    await session.commit()

    return True


async def function_set_reminder(data: SetReminder,
                                session: AsyncSession = Depends(get_async_session)):
    day = data.habit_date[0:2]
    month = data.habit_date[3:5]
    year = data.habit_date[-4:]
    hours = data.time[0:2]
    minutes = data.time[-2:]
    time_reminder = datetime.datetime.combine(datetime.date(int(year), int(month), int(day)),
                                              datetime.time(int(hours), int(minutes)))

    find_user = (
        select(Users).where(Users.telegram_id == data.telegram_id)
    ).subquery()

    find_habit = (
        select(Habits).where(and_(Habits.user_id == find_user.c.id, Habits.name_habit == data.name_habit))
    ).subquery()
    await session.execute(update(HabitTracking).values(alert_time=time_reminder).where(
        and_(HabitTracking.habit_id == find_habit.c.id, HabitTracking.count < 21)))
    await session.commit()

    return {"name_habit": data.name_habit, "habit_date": time_reminder}

