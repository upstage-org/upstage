from pydantic import BaseModel


class LoginDTO(BaseModel):
    username: str
    password: str
