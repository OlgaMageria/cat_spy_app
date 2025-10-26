from uuid import UUID
from src.domain.repositories.mission_repository import MissionRepository

class MissionDomainService:
    """Service for mission-related domain operations"""
    
    def __init__(self, mission_repository: MissionRepository):
        self.mission_repository = mission_repository
    
    def can_assign_cat_to_mission(self, mission_id: UUID, cat_id: UUID) -> bool:
        """Check if a cat can be assigned to a mission"""
        mission = self.mission_repository.find_by_id(mission_id)
        if not mission:
            return False
        
        if not mission.can_be_assigned():
            return False
        
        return cat_id not in mission.assigned_cat_uuids