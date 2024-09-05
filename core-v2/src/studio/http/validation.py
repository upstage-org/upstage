from pydantic import BaseModel, EmailStr, Field, constr


class BatchUserInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=10)
    password: str = Field(..., min_length=8, max_length=256)
    email: EmailStr
