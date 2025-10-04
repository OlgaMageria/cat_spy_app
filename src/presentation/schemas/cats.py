from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

from datetime import datetime

class CatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int

class CatModel(BaseModel):
    name: str = Field(..., max_length=50)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8)

    @field_validator('breed')
    @classmethod
    def normalize_breed(cls, v: str) -> str:
        return v.lower().strip()

class CatCreate(CatBase):
    password: str

class CatResponse(BaseModel):
    id: int
    name: str
    years_of_experience: int
    breed: str
    salary: int
    is_staff: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CatProfile(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: Optional[int] = None
    created_at: datetime

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordResetRequest(BaseModel):
    name: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

