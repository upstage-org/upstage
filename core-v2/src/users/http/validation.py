from pydantic import BaseModel


class CreateUserInput(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    intro: str
    token: str
