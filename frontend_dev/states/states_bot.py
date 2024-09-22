from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    set_id = State()
    add_habit = State()
    save_habit_name = State()
    set_delete_habit = State()
    habit_description = State()
    habit_goal = State()
    habit_date = State()

