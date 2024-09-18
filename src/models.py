from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.types import LargeBinary
from database import engine  # type: ignore


class Model(DeclarativeBase):
    pass


class Users(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=True)
    telegram_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    token = Column(LargeBinary, nullable=False)

    def __repr__(self):
        return f"id={self.id}," f" name={self.name}, t_id={self.telegram_id}, is_active={self.is_active}"


class Habits(Model):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)

    name_habit = Column(String(30),)
    description = Column(String(50),)

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), unique=False)

    def __repr__(self):
        return f"id={self.id}," f" name_habit={self.name_habit}, description={self.description}"


class HabitTracking(Model):
    __tablename__ = 'habittrackings'

    id = Column(Integer, primary_key=True)

    alert_time = Column(DateTime, server_default=func.now())
    count = Column(Integer,)

    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), unique=False)

    def __repr__(self):
        return f"id={self.id}," f" alert_time={self.alert_time}, count={self.count}"


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
