from typing import List, Optional

from pydantic import BaseModel, Field, constr

class UserSchema(BaseModel):
    password: constr(min_length=8, max_length=20)