import json
import requests

from frontend_dev.config_info.config import BACK_URL


def check_user_db(telegram_id):
    data = {"telegram_id": telegram_id}

    check_user = requests.post(
        url=f"{BACK_URL}/check_user/",
        data=json.dumps(data),
    )

    return check_user


def add_habit_db(data: dict):

    requests.post(url=f'{BACK_URL}/user/me/add_habit/', data=json.dumps(data))

