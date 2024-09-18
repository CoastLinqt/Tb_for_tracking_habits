from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    set_pass = State()
    add_habit = State()
    habit_description = State()
    habit_goal = State()
    habit_date = State()
