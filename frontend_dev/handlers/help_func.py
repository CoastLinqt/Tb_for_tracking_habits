import prettytable as pt
from typing import List


def create_table(data: List[dict]):
    table = pt.PrettyTable(["num", "name", "description", "goal"])
    table.align["num"] = "l"
    table.align["Name"] = "r"
    table.align["Discr"] = "r"
    table.align["Goal"] = "r"

    table._max_width = {"name": 9, "description": 9, "goal": 5}

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
