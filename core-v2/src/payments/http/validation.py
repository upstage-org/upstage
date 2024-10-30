from pydantic import BaseModel, Field


class OneTimePurchaseInput(BaseModel):
    cardNumber: str = Field(...)
    expYear: str = Field(...)
    expMonth: str = Field(...)
    cvc: str = Field(...)
    amount: float = Field(...)


class CreateSubscriptionInput(BaseModel):
    cardNumber: str = Field(...)
    expYear: str = Field(...)
    expMonth: str = Field(...)
    cvc: str = Field(...)
    amount: float = Field(...)
    currency: str = Field(...)
    email: str = Field(...)
    type: str = Field(...)
