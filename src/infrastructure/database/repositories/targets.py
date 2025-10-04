from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Depends

from src.infrastructure.database.models.tables import Target, Mission, mission_cat, Cat

from src.infrastructure.database.session import get_db

class TargetRepository:
    """Repository for managing Target entities in the database."""
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def set_completed_target(self, target_id: int, current_cat: Cat) -> Target:
        target = await self.db.execute(
            select(Target).where(Target.id == target_id)
        )
        target = target.scalar_one_or_none()
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target not found"
            )
        # Check if mission of the target is assigned to current cat
        cat_mission_id = await self.db.execute(
            select(mission_cat.c.mission_id)
            .where(mission_cat.c.cat_id == current_cat.id)
        )
        cat_mission_ids = {mid for (mid,) in cat_mission_id.all()}  
        if target.mission_id not in cat_mission_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to complete this target"
            )
        target.is_completed = True

        # Close mission if all targets are completed
        all_targets = await self.db.execute(
            select(Target).where(Target.mission_id == target.mission_id)
        )
        all_targets = all_targets.scalars().all()
        if all(t.is_completed for t in all_targets):
            mission = await self.db.execute(
                select(Mission).where(Mission.id == target.mission_id)
            )
            mission = mission.scalar_one_or_none()
            if mission:
                mission.is_completed = True
        await self.db.commit()
        await self.db.refresh(target)
        return target

async def get_target_repository(db: AsyncSession = Depends(get_db)) -> TargetRepository:
    return TargetRepository(db)