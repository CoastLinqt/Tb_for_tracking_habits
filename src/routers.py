from fastapi import Depends, HTTPException,  APIRouter, Request, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import Users
from schemas import UserSchema, TokenInfo, TelegramId, AddHabits
from utils import hash_password, encode_jwt
from methods import authenticate_user, get_current_active_auth_user, add_habit
# from main import app
# from frontend_dev.config_info.config import WEBHOOK_URL, WEBHOOK_PATH
# from frontend_dev.loader import bot


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)


router = APIRouter()


@router.post("/token/")
async def auth_register_user(
    user: UserSchema, session: AsyncSession = Depends(get_async_session)
):

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

    if isinstance(user, HTTPException):
        return user.detail

    jwt_payload = {
        "sub": user.name,
        "username": user.name,
        "telegram_id": user.telegram_id,
    }
    token = encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")


@router.post('/check_user/')
async def user_check_db(telegram_id: TelegramId, session: AsyncSession = Depends(get_async_session)):

    find_user_db = await session.execute(
        select(Users).where(Users.telegram_id == telegram_id.telegram_id)
    )
    result = find_user_db.scalar()

    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    raise HTTPException(status_code=status.HTTP_200_OK,)


@router.get("/user/me/")
async def auth_user_check_self_info(
                              user: UserSchema = Depends(get_current_active_auth_user),
                             ):

    return {"username": user.name, "telegram_id": user.telegram_id}


@router.post("/user/me/add_habit/")
async def add_habit(habit: AddHabits = Depends(add_habit)):

    if habit:
        raise HTTPException(status_code=status.HTTP_200_OK,)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, )
