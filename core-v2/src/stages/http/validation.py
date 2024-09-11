from typing import Optional
from pydantic import BaseModel, Field


class StageInput(BaseModel):
    id: Optional[int] = Field(None, description="ID of the stage")
    fileLocation: str = Field(..., description="Location of the file")
    status: str = Field(..., description="Status of the stage")
    visibility: bool = Field(..., description="Visibility of the stage")
    cover: str = Field(..., description="Cover image URL")
    name: str = Field(..., description="Name of the stage")
    description: str = Field(..., description="Description of the stage")
    playerAccess: str = Field(..., description="Player access information")
    config: Optional[str] = Field(None, description="Configuration of the stage")


class DuplicateStageInput(BaseModel):
    id: int = Field(..., description="ID of the stage")
    name: str = Field(..., description="Name of the stage")
