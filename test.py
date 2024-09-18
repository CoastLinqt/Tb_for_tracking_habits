import json
import datetime
from collections import OrderedDict

data_new = {"add_habit": "dsa", "habit_description": "das", "message_habit_goal": 12, "telegram_id": 138217207, "habit_date": "18-09-2024"}

print(json.dumps(data_new))

dsa = '26-09-2024'

formatter_string = "%d-%m-%Y"
datetime_object = datetime.datetime.strptime(dsa, formatter_string)
date_object = datetime_object.date()
print(date_object)