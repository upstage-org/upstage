from pydantic import BaseModel


class SignupDTO(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    intro: str
    token: str
