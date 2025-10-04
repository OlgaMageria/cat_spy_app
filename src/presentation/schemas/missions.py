from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

from src.presentation.schemas.targets import TargetCreate, TargetResponse

class MissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    targets: List[TargetCreate] = Field(..., min_items=1, max_items=3)
    cat_ids: Optional[List[int]] = Field(default=None)
    
    @field_validator('name', 'description')
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v
    
    @field_validator('targets')
    @classmethod
    def validate_targets_count(cls, v: List[TargetCreate]) -> List[TargetCreate]:
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Mission must have between 1 and 3 targets')
        return v

class MissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    targets: List[TargetResponse]
    cat_ids: List[int]
    
    class Config:
        from_attributes = True

    @classmethod
    def from_mission(cls, mission):
        return cls(
            id=mission.id,
            name=mission.name,
            description=mission.description,
            created_at=mission.created_at,
            updated_at=mission.updated_at,
            is_completed=mission.is_completed,
            targets=[
                {
                    "id": target.id,
                    "name": target.name,
                    "country": target.country,
                    "is_completed": target.is_completed,
                    "mission_id": target.mission_id,
                    "created_at": target.created_at
                }
                for target in mission.mission_target
            ],
            cat_ids=[cat.id for cat in mission.cat]
        )

class AssignCatsRequest(BaseModel):
    cat_ids: list[int] = Field(..., min_items=1)
    