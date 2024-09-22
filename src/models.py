from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, validates
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

    habits = relationship("Habits", backref='users', cascade="all, delete", lazy='selectin')

    def __repr__(self):
        return f"id={self.id}," f" name={self.name}, t_id={self.telegram_id}, is_active={self.is_active}"


class Habits(Model):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)

    name_habit = Column(String(20), unique=True)
    description = Column(String(50),)
    habit_goal = Column(String(20),)
    result = Column(String, default='-')

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=False)

    habittrackings = relationship("HabitTracking", backref='habits', cascade="all, delete", lazy='selectin')

    def __repr__(self):
        return f"id={self.id}," f" name_habit={self.name_habit}, description={self.description}"


class HabitTracking(Model):
    __tablename__ = 'habittrackings'

    id = Column(Integer, primary_key=True)

    alert_time = Column(DateTime, nullable=True)
    count = Column(Integer, CheckConstraint('count <= 20', postgresql_not_valid=True), default=0)

    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), unique=False)

    @validates('count')
    def validate_age(self, key, value):
        if not value <= 20:
            raise ValueError(f'Invalid age {value}')
        return value

    def __repr__(self):
        return f"id={self.id}," f" alert_time={self.alert_time}, count={self.count}"




async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
