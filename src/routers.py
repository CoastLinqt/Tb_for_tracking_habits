import datetime

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select, and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import get_async_session
from models import Users, Habits, HabitTracking
from schemas import (
    UserSchema,
    TokenInfo,
    TelegramId,
    AddHabits,
    EditTrackHabit,
    SetReminder,
)
from utils import hash_password, encode_jwt
from methods import (
    authenticate_user,
    get_current_active_auth_user,
    add_habit,
    function_update_track_habit,
    function_edit_habit,
    function_track_all,
    function_delete_habit,
    function_process_habits,
    function_habit_stats,
    function_user_check_db,
    function_set_reminder,
)


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)


router = APIRouter()


@router.post("/token/")
async def auth_register_user(
    user: UserSchema, session: AsyncSession = Depends(get_async_session)
):
    """The router hashes the user's password and enters it into the database """

    find_user_db = await session.execute(
        select(Users.telegram_id).filter(Users.telegram_id == int(user.telegram_id))
    )
    if find_user_db.scalar() is None:
        user.password = hash_password(user.password)
        new_user = Users(
            name=user.username, telegram_id=user.telegram_id, token=user.password
        )
        session.add(new_user)
        await session.commit()
        return {"details": f"{user.password}"}
    else:
        return {"details": "user has already been registered"}


@router.post(
    "/login/",
)
async def auth_user_issue_jwt(user: UserSchema = Depends(authenticate_user)):
    """The router formulates the access token """

    if isinstance(user, HTTPException):
        return user.detail

    jwt_payload = {
        "sub": user.name,
        "username": user.name,
        "telegram_id": user.telegram_id,
    }
    token = encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")


@router.post("/check_user/")
async def user_check_db(telegram_id: TelegramId = Depends(function_user_check_db)):
    """The router receives the necessary information from the telegram bot and,
     if there is one, checks whether the user is registered """

    if telegram_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    raise HTTPException(
        status_code=status.HTTP_200_OK,
    )


@router.get("/user/me/")
async def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
):
    """If correct password and username,
     the router gives user's information itself"""

    return {"username": user.name, "telegram_id": user.telegram_id}


@router.post("/user/me/add_habit/")
async def add_habit(habit: AddHabits = Depends(add_habit)):
    """The router receives the necessary information from the telegram bot and,
     if available, adds it to the Habit table"""

    if habit is True:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.post("/user/me/habits/")
async def process_habits(telegram_id: TelegramId = Depends(function_process_habits)):
    """The router receives the necessary information from the telegram bot and,
     if available, searches for all the habits associated with the user"""

    result = telegram_id

    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/habit/delete/")
async def delete_habit(data_habit: EditTrackHabit = Depends(function_delete_habit)):
    """The router receives the necessary information from the telegram bot and,
     if there is one, deletes it"""

    if data_habit:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.patch("/habit/edit/")
async def edit_habit(data_habit: EditTrackHabit = Depends(function_edit_habit)):
    """The router receives the necessary information from the telegram bot and,
     if there is one, edits it """

    if data_habit:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.post("/habit/count_track/")
async def track_habit(
    tracking_habit: EditTrackHabit = Depends(function_update_track_habit),
):
    """The router receives the necessary information from the telegram bot and,
     if there is one, keeps an account according to a given habit """

    if tracking_habit:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/habit/track_all/")
async def track_all(telegram_id: TelegramId = Depends(function_track_all)):
    """The router receives information from the telegram bot and processes it.
     It searches for the necessary information in the Habit and HabitTracking tables
      and outputs the result of all the excesses """

    result = telegram_id
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.post("/habit/habit_stats/")
async def habit_stats(telegram_id: TelegramId = Depends(function_habit_stats)):
    """The router receives information from the telegram bot and processes it.
     Searches for the necessary information in the Habit and HabitTracking tables """

    result = telegram_id
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.post("/habit/set_reminder/")
async def set_reminder(
    data: SetReminder = Depends(function_set_reminder),
):
    """The router that receives data from the telegram bot,
     processes it and enters it into the database to notify the client in the future"""

    if data:
        return data
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
