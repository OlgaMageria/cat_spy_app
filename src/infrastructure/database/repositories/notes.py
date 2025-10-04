from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status, Depends

from src.infrastructure.database.models.tables import Mission, Note, Target, Cat

from src.infrastructure.database.session import get_db

class NoteRepository:
    """Repository for managing Note entities in the database."""
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, target_id: int, content: str, cat_id: int) -> Note:
        cat = await self.db.execute(
            select(Cat).where(Cat.id == cat_id)
        )   
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found"
            )
        cat = cat.scalar_one_or_none()

        target = await self.db.execute(
            select(Target).where(Target.id == target_id)
        )
        target = target.scalar_one_or_none()
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target not found"
            )
        cat_mission = await self.db.execute(
            select(Mission)
            .join(Mission.cat)
            .where(Mission.id == target.mission_id, Cat.id == cat_id)
        )
        cat_mission = cat_mission.scalar_one_or_none()
        if not cat_mission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cat is not assigned to the mission of this target"
            )

        note = Note(
            content=content,
            target_id=target.id,
            cat_id=cat.id
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_note_by_id(self, note_id: int) -> Optional[Note]:
        result = await self.db.execute(
            select(Note).where(Note.id == note_id)
        )
        return result.scalar_one_or_none()

    async def update_note(self, note_id: int, new_content: str, cat_id: int) -> Note:
        note = await self.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        is_target_completed = await self.db.execute(
            select(Target).where(Target.id == note.target_id, Target.is_completed)
        )
        if is_target_completed.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update note for a completed target"
            )
        cat = await self.db.execute(
            select(Cat).where(Cat.id == cat_id)
        )
        cat = cat.scalar_one_or_none()
        if not cat or note.cat_id != cat.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cat is not the author of this note"
            )

        note.content = new_content
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_all_for_cat(self, cat_id: int) -> List[Note]:
        result = await self.db.execute(
            select(Note)
            .where(Note.cat_id == cat_id)
            .options(selectinload(Note.note_cat))
        )
        return result.scalars().all()

async def get_note_repository(db: AsyncSession = Depends(get_db)) -> NoteRepository:
    return NoteRepository(db)