from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructure.database.session import get_db
from src.infrastructure.database.repositories.notes import NoteRepository
from src.infrastructure.database.repositories.missions import MissionRepository
from src.infrastructure.database.repositories.targets import TargetRepository
from src.infrastructure.database.repositories.cats import CatRepository


async def get_cat_repository(db: AsyncSession = Depends(get_db)) -> CatRepository:
    return CatRepository(db)

async def get_mission_repository(db: AsyncSession = Depends(get_db)) -> MissionRepository:
    return MissionRepository(db)

async def get_target_repository(db: AsyncSession = Depends(get_db)) -> TargetRepository:
    return TargetRepository(db)

async def get_note_repository(db: AsyncSession = Depends(get_db)) -> NoteRepository:
    return NoteRepository(db)

