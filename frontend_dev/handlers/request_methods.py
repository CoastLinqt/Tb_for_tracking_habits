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
    re = requests.post(url=f'{BACK_URL}/user/me/add_habit/', data=json.dumps(data))

    if re.status_code == 500:
        return False
    return True


def habits_all(data: dict):
    response = requests.post(
        url=f"{BACK_URL}/user/me/habits/", data=json.dumps(data)
    )

    return response


def edit_habit_request(data: dict):
    requests.patch(f"{BACK_URL}/habit/edit/", data=json.dumps(data))



def delete_habit_request(data: dict):
    requests.delete(url=f"{BACK_URL}/habit/delete/", data=json.dumps(data))
