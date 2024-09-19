from pydantic import BaseModel, Field


class LicenseInput(BaseModel):
    assetId: int = Field(
        ..., description="Asset ID must be between 1 and 50 characters"
    )
    level: int = Field(..., description="Level must be between 1 and 10")
    permissions: str = Field(
        ..., description="Permissions must be between 1 and 100 characters"
    )
