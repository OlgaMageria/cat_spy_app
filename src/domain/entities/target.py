# domain/entities/target.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from typing import List
from enum import Enum
from uuid import UUID, uuid4

class TargetStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

@dataclass
class Target:
    """Target aggregate root"""
    uuid: UUID
    cat_uuid: UUID
    mission_uuid: UUID
    description: str
    status: TargetStatus
    notes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    @classmethod
    def create(cls, cat_uuid: UUID, mission_uuid: UUID, description: str) -> 'Target':
        """Factory method to create a new Target"""
        return cls(
            uuid=uuid4(),
            cat_uuid=cat_uuid,
            mission_uuid=mission_uuid,
            description=description,
            status=TargetStatus.PENDING
        )

    def assign_cat(self, cat_uuid: UUID) -> None:
        """Assign a cat to the target"""
        self.cat_uuid = cat_uuid
        self.status = TargetStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
    
    def add_note(self, note: str) -> None:
        """Add a note to the target"""
        self.notes.append(note)
        self.updated_at = datetime.now(timezone.utc)
    
    def complete(self) -> None:
        """Mark target as completed"""
        self.status = TargetStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
