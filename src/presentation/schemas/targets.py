from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('name', 'country')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

class TargetResponse(BaseModel):
    id: int
    name: str
    country: str
    is_completed: bool
    mission_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True