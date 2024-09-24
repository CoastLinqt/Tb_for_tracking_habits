from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def pick_edit(data):
    buttons = InlineKeyboardMarkup()
    for i in data:
        buttons.add(
            (
                InlineKeyboardButton(
                    text=i["name_habit"].capitalize(),
                    callback_data="+" + i["name_habit"].capitalize(),
                )
            )
        )
    return buttons


def set_habit(data):
    buttons = InlineKeyboardMarkup()
    for i in data:
        buttons.add(
            (
                InlineKeyboardButton(
                    text=i["name_habit"].capitalize(),
                    callback_data="-" + i["name_habit"].capitalize(),
                )
            )
        )
    return buttons


def pick_track(data):
    print(data)
    buttons = InlineKeyboardMarkup()
    for i in data:
        buttons.add(
            (
                InlineKeyboardButton(
                    text=i["name_habit"].capitalize(),
                    callback_data="*" + i["name_habit"].capitalize(),
                )
            )
        )
    return buttons


def delete_or_edit_habit():
    buttons = InlineKeyboardMarkup()

    item = InlineKeyboardButton("Edit", callback_data="Edit")
    item2 = InlineKeyboardButton("Delete", callback_data="Delete")
    buttons.add(item, item2)

    return buttons


def choice_edit_habit():
    buttons = InlineKeyboardMarkup()
    item = InlineKeyboardButton("Description", callback_data="description")
    item2 = InlineKeyboardButton("Goal", callback_data="goal")
    item3 = InlineKeyboardButton("All together", callback_data="all")
    buttons.add(item, item2, item3)

    return buttons


def pick_time():
    keyboard = ReplyKeyboardMarkup(
        row_width=4, resize_keyboard=True, one_time_keyboard=True
    )

    item1 = KeyboardButton("00:00")
    item2 = KeyboardButton("01:00",)
    item3 = KeyboardButton("02:00",)
    item4 = KeyboardButton("03:00",)
    item5 = KeyboardButton("04:00",)
    item6 = KeyboardButton("05:00",)
    item7 = KeyboardButton("06:00",)
    item8 = KeyboardButton("07:00",)
    item9 = KeyboardButton("08:00",)
    item10 = KeyboardButton("09:00",)
    item11 = KeyboardButton("10:00",)
    item12 = KeyboardButton("11:00",)
    item13 = KeyboardButton("12:00",)
    item14 = KeyboardButton("13:00",)
    item15 = KeyboardButton("14:00",)
    item16 = KeyboardButton("15:00",)
    item17 = KeyboardButton("16:00",)
    item18 = KeyboardButton("17:00",)
    item19 = KeyboardButton("18:00",)
    item20 = KeyboardButton("19:00",)
    item21 = KeyboardButton("20:00",)
    item22 = KeyboardButton("21:00",)
    item23 = KeyboardButton("22:00",)
    item24 = KeyboardButton("23:00",)

    keyboard.add(item1, item2, item3, item4, item5, item6,
                 item7, item8, item9, item10, item11, item12,
                 item13, item14, item15, item16, item17, item18,
                 item19, item20, item21, item22, item23, item24,
                 )

    return keyboard
