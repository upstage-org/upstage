from pydantic import BaseModel, Field


class LoginInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=256)
