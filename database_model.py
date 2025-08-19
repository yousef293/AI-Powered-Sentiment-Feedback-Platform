from pydantic import BaseModel,constr,validator
from datetime import datetime
from typing import Literal
from fastapi import FastAPI
app=FastAPI()

class Feedback_schema(BaseModel):
    text:constr(max_length=200) # type: ignore
    createdAt: datetime=datetime.utcnow()


class Client_data(BaseModel):
    user_name:constr(min_length=3,max_length=15) # type: ignore
    user_id:int
    password:constr(min_length=8, max_length=20) # type: ignore
    @validator("user_name")
    def validate_user_name(cls, v):
        if len(v) > 15:
            raise ValueError("Username must be 15 characters or less.")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return v
    @validator("password")
    def validate_password(cls, v):
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters.")
            if len(v) > 20:
                raise ValueError("Password must not exceed 20 characters.")
            return v


