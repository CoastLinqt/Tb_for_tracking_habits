from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def pick_edit(data):
    buttons = InlineKeyboardMarkup()
    for i in data:

        buttons.add((InlineKeyboardButton(text=i['name_habit'].capitalize(), callback_data="+" + i['name_habit'].capitalize())))
    return buttons


def delete_or_edit_habit():
    buttons = InlineKeyboardMarkup()

    item = InlineKeyboardButton("Редактировать", callback_data="Редактировать")
    item2 = InlineKeyboardButton("Удалить", callback_data="Удалить")
    buttons.add(item, item2)

    return buttons


def choice_edit_habit():

    buttons = InlineKeyboardMarkup()
    item = InlineKeyboardButton("Описание", callback_data="description")
    item2 = InlineKeyboardButton("Цель", callback_data="goal")
    item3 = InlineKeyboardButton("Все вместе", callback_data="all")
    buttons.add(item, item2, item3)

    return buttons
