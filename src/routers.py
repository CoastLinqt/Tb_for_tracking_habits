from fastapi import APIRouter
import httpx


from backend_dev.src.frontend_dev.main import bot

router = APIRouter()
#
#
# @router.get("/sign_up")
# async def sign_up(user: UserSchema = Depends(),
#                   AsyncSession = Depends(get_async_session)
#                   ):
#
#     pass

TOKEN = "6944166033:AAHHKSdppLIMBrQWXHnaKoyLhyWsLaMoBc0"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
DOMAIN = 'http://127.0.0.1:8000/'
client = httpx.AsyncClient()

@router.get("/setwebhook")
async def set_webhook():
    s = bot.set_webhook(url=f"{DOMAIN}/telegram-update")
    if s:
        return {"dsa":"dsa"}
    else:
        return ("Error!")

