from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    set_id = State()
    set_pass = State()
    add_habit = State()
    habit_description = State()
    habit_goal = State()
    habit_date = State()
    save_habit_name = State()
    set_goal = State()
    set_description = State()
    set_delete_habit = State()
    set_all_goal = State()
    set_all_description = State()

