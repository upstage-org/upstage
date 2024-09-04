from pydantic import BaseModel


class LoginInput(BaseModel):
    username: str
    password: str
