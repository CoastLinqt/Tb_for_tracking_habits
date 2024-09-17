from typing import List, Optional
#
from pydantic import BaseModel, Field, constr, parse_obj_as, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    telegram_id: int
    password: str
    is_active: bool


class Chat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str


class FromF(BaseModel):

    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


class Message(BaseModel):
    message_id: int
    from_f: FromF = Field(alias='from')
    chat: Chat
    date: int
    text: str


class Answer(BaseModel):
    update_id: int
    message: Message


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


