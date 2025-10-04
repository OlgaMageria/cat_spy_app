from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status, Depends

from src.infrastructure.database.models.tables import Mission, Target, Cat, mission_cat

from src.infrastructure.database.session import get_db
from src.presentation.schemas.missions import MissionCreate

class MissionRepository:
    """Repository for managing Mission entities in the database."""
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create(self, body: MissionCreate) -> Mission:
        """Create mission with targets and optional cat assignments"""
        existing_mission = await self.get_by_name(body.name)
        if existing_mission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mission with this name {body.name} already exists."
            )
       
        # Assign cats if provided
        if body.cat_ids:
            result = await self.db.execute(
                select(Cat).where(Cat.id.in_(body.cat_ids))
            )
            cats = result.scalars().all()
            
            if len(cats) != len(body.cat_ids):
                found_ids = {cat.id for cat in cats}
                missing_ids = set(body.cat_ids) - found_ids
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cats not found: {missing_ids}"
                )
            # Check if any cat is already assigned to a mission
            cats_with_missions = []
            for cat in cats:
                # Check if cat has any missions assigned
                mission_check = await self.db.execute(
                    select(mission_cat).where(mission_cat.c.cat_id == cat.id)
                )
                if mission_check.first():
                    cats_with_missions.append(cat.id)
            
            if cats_with_missions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cats with ID {cats_with_missions[0]} are already assigned to missions. Each cat can only have one mission."
                )
        # Create mission with targets relationship
        mission = Mission(
            name=body.name,
            description=body.description,
            mission_target=[
                Target(
                    name=target.name,
                    country=target.country
                )
                for target in body.targets
            ]
        )
        
        # Assign cats after validation
        if body.cat_ids:
            mission.cat.extend(cats)
        
        self.db.add(mission)
        await self.db.flush()
        mission_id = mission.id  # Access ID after flush
        await self.db.commit()

        result = await self.db.execute(
        select(Mission)
        .where(Mission.id == mission_id)
        .options(selectinload(Mission.mission_target))
        .options(selectinload(Mission.cat))
    )
        return result.scalar_one()

    async def get_by_id(self, mission_id: int) -> Optional[Mission]:
        """Get mission by id with all relationships loaded"""
        result = await self.db.execute(
            select(Mission)
            .where(Mission.id == mission_id)
            .options(selectinload(Mission.mission_target))
            .options(selectinload(Mission.cat))
        )
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Optional[Mission]:
        """Check if mission with this name already exists"""
        result = await self.db.execute(
            select(Mission).where(Mission.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all_missions(self) -> List[Mission]:
        """Get all missions with relationships loaded"""
        result = await self.db.execute(
            select(Mission)
            .options(selectinload(Mission.mission_target))
            .options(selectinload(Mission.cat))
        )
        return result.scalars().all()

    async def delete_mission_by_id(self, mission_id: int) -> None:
        mission = await self.get_by_id(mission_id)
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not found"
            )
        if mission.cat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete mission assigned to cats"
            )
        await self.db.delete(mission)
        await self.db.commit()

    async def set_completed_mission(self, mission_id: int) -> Mission:
        mission = await self.get_by_id(mission_id)
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not found"
            )
        mission.is_completed = True
        for target in mission.mission_target:
            target.is_completed = True
        await self.db.commit()
        await self.db.refresh(mission)
        return mission
    
    async def assigne_cats_to_mission(self, mission_id: int, cat_ids: List[int]) -> Mission:
        mission = await self.get_by_id(mission_id)
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not found"
            )
        
        result = await self.db.execute(
            select(Cat).where(Cat.id.in_(cat_ids))
        )
        cats = result.scalars().all()
        
        if len(cats) != len(cat_ids):
            found_ids = {cat.id for cat in cats}
            missing_ids = set(cat_ids) - found_ids
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cats not found: {missing_ids}"
            )
        
        mission.cat.extend(cats)
        await self.db.commit()
        await self.db.refresh(mission)
        return mission

    async def set_completed_target(self, target_id: int) -> Target:
        result = await self.db.execute(
            select(Target).where(Target.id == target_id)
        )
        target = result.scalar_one_or_none()
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target not found"
            )
        target.is_completed = True
        await self.db.commit()
        await self.db.refresh(target)
        return target

async def get_mission_repository(db: AsyncSession = Depends(get_db)) -> MissionRepository:
    return MissionRepository(db)