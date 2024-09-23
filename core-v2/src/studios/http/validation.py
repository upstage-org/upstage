from pydantic import BaseModel, EmailStr, Field, constr


class BatchUserInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=10)
    password: str = Field(..., min_length=8, max_length=256)
    email: EmailStr


class UpdateUserInput(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=10)
    password: str = Field(..., min_length=8, max_length=256)
    email: EmailStr
    binName: str = Field(..., min_length=1)
    role: int
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    displayName: str = Field(..., min_length=1)
    active: bool
    firebasePushnotId: str
    uploadLimit: int
    intro: str = Field(..., max_length=500)


class ChangePasswordInput(BaseModel):
    oldPassword: str = Field(..., min_length=8, max_length=256)
    newPassword: str = Field(..., min_length=8, max_length=256)
    id: int
