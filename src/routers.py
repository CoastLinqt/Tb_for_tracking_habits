from fastapi import Depends, HTTPException, status, APIRouter, Form
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Users

from utils import encode_jwt
from schemas import UserSchema, TokenInfo
from utils import settings, hash_password
from methods import authenticate_user


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
        return {"details": "You've already been registered"}


@router.post(
    "/login/",
)
async def auth_user_issue_jwt(user: UserSchema = Depends(authenticate_user)):

    if isinstance(user, HTTPException):
        return user.detail

    jwt_payload = {"sub": user[0]["name"], "username": user[0]["name"]}
    token = encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")

# @router.get("/user/me/")
# def
