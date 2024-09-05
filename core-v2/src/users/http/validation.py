from pydantic import BaseModel, Field, EmailStr


class CreateUserInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=10)
    password: str = Field(..., min_length=8, max_length=256)
    email: EmailStr
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    intro: str = Field(..., max_length=500)
    token: str
