from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    
    @field_validator('content')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

class NoteResponse(BaseModel):
    id: int
    content: str
    target_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True