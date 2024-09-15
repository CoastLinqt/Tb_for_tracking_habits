from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func, ARRAY
from sqlalchemy.orm import DeclarativeBase, relationship

from database import engine  # type: ignore


class Model(DeclarativeBase):
    pass


class Users(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=True)
    telegram_id = Column(Integer)

    token = Column(String(), nullable=None)

    def __repr__(self):
        return f"id={self.id}," f" name={self.name}"


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)