from fastapi import APIRouter, Request
import httpx



router = APIRouter()

@router.get("/")
def sign_up():

    return {"Hello": "world"}



