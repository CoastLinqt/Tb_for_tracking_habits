import prettytable as pt
from typing import List


def create_table(data: List[dict]):
    table = pt.PrettyTable(
        [
            "№",
            "Name",
            "Description",
            "Goal",
        ]
    )
    table.align["num"] = "r"
    table.align["Name"] = "m"
    table.align["Discr"] = "m"
    table.align["Goal"] = "m"

    table._max_width = {
        "Name": 9,
        "Description": 10,
        "Goal": 7,
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
            "№",
            "Name",
            "Result",
        ]
    )
    table.align["num"] = "r"
    table.align["Name"] = "m"
    table.align["Result"] = "m"

    table._max_width = {
        "Name": 10,
        "Result": 3,
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
