import prettytable as pt
from typing import List


def create_table(data: List[dict]):
    table = pt.PrettyTable(["num", "Название", "Описание", "Цель", 'Р'])
    table.align["num"] = "R"
    table.align["Name"] = "r"
    table.align["Discr"] = "r"
    table.align["Goal"] = "r"
    table.align["Res"] = "r"

    table._max_width = {"Название": 6, "Описание": 7, "Цель": 5, "Р": 1}

    for num, result in enumerate(data):
        table.add_row(
            [
                num + 1,
                f'{result["name_habit"]}',
                f'{result["description"]}',
                f'{result["habit_goal"]}',
                f'{result["result"]}',
            ],
            divider=True,
        )
    return table
