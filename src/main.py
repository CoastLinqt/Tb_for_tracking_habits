from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import create_tables
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    print("Database created")


app = FastAPI(title="traing_habits", lifespan=lifespan)

app.include_router(router=router)
