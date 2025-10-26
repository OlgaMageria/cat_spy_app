from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID

class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('name', 'country')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

class TargetResponse(BaseModel):
    uuid: UUID
    name: str
    country: str
    status: str
    mission_uuid: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True