import prettytable as pt
from typing import List


def create_table(data: List[dict]):
    table = pt.PrettyTable(
        [
            "num",
            "Название",
            "Описание",
            "Цель",
        ]
    )
    table.align["num"] = "R"
    table.align["Name"] = "r"
    table.align["Discr"] = "r"
    table.align["Goal"] = "r"

    table._max_width = {
        "Название": 6,
        "Описание": 10,
        "Цель": 7,
    }

    for num, result in enumerate(data):
        table.add_row(
            [
                num + 1,
                f'{result["name_habit"]}',
                f'{result["description"]}',
                f'{result["habit_goal"]}',
            ],
            divider=True,
        )
    return table


def track_stats(data: List[dict]):
    table = pt.PrettyTable(
        [
            "num",
            "Название",
            "Результат",
        ]
    )
    table.align["num"] = "R"
    table.align["Name"] = "r"
    table.align["Result"] = "r"

    table._max_width = {
        "Название": 10,
        "Результат": 3,
    }

    for num, result in enumerate(data):
        table.add_row(
            [
                num + 1,
                f'{result["name_habit"]}',
                f'{result["count"]}/21',
            ],
            divider=True,
        )
    return table
