from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from schemas import UserSchema

router = APIRouter(prefix="/api")


@router.post("/sign_up")
async def sign_up(user: UserSchema = Depends(), AsyncSession = Depends(get_async_session)):
    pass

