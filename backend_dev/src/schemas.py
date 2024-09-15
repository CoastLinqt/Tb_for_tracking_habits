from typing import List, Optional

from pydantic import BaseModel, Field, constr

class UserSchema(BaseModel):
    name: str = Field(max_length=20)
    password: constr(min_length=8, max_length=20)