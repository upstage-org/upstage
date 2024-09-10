from pydantic import BaseModel, Field


class StageInput(BaseModel):
    fileLocation: str = Field(..., description="Location of the file")
    status: str = Field(..., description="Status of the stage")
    visibility: bool = Field(..., description="Visibility of the stage")
    cover: str = Field(..., description="Cover image URL")
    name: str = Field(..., description="Name of the stage")
    description: str = Field(..., description="Description of the stage")
    playerAccess: str = Field(..., description="Player access information")
