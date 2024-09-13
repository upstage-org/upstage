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


class AssignMediaInput(BaseModel):
    id: int = Field(..., description="ID of the stage")
    mediaIds: Optional[list[int]] = Field([], description="List of media IDs")


class UploadMediaInput(BaseModel):
    name: str = Field(..., description="Name of the media")
    base64: str = Field(..., description="Base64 encoded media")
    mediaType: str = Field(..., description="Type of the media")
    filename: str = Field(..., description="Name of the file")


class UpdateMediaInput(BaseModel):
    id: int = Field(..., description="ID of the media")
    name: str = Field(..., description="Name of the media")
    mediaType: Optional[str] = Field(None, description="Type of the media")
    description: Optional[str] = Field(None, description="Description of the media")
    fileLocation: Optional[str] = Field(None, description="Location of the file")
    base64: Optional[str] = Field(None, description="Base64 encoded media")
    copyrightLevel: Optional[int] = Field(None, description="Copyright level")
    playerAccess: Optional[str] = Field(None, description="Player access information")
    uploadedFrames: Optional[list[str]] = Field(
        [], description="List of uploaded frames"
    )


class AssignStagesInput(BaseModel):
    id: int = Field(..., description="ID of the stage")
    stageIds: Optional[list[int]] = Field([], description="List of stage IDs")
