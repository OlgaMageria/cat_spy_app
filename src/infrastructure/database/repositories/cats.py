from typing import Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_db
from src.infrastructure.database.models.tables import Cat
from src.application.password_service import password_service
from src.presentation.schemas.cats import CatCreate, CatUpdate

class CatRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_id(self, cat_id: int) -> Optional[Cat]:
        result = await self.db.execute(select(Cat).where(Cat.id == cat_id))
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Cat]:
        result = await self.db.execute(select(Cat).where(func.lower(Cat.name) == name.lower()))
        return result.scalars().first()

    async def search_by_name(self, name: str) -> list[Cat]:
        result = await self.db.execute(select(Cat).where(func.lower(Cat.name).like(f"%{name.lower()}%")))
        return result.scalars().all()

    async def get_all_cats(self) -> list[Cat]:
        result = await self.db.execute(select(Cat))
        return result.scalars().all()

    async def create(self, body: CatCreate) -> Cat:
        cat_data = body.model_dump()
        new_cat = Cat(**cat_data)
        self.db.add(new_cat)
        await self.db.commit()
        await self.db.refresh(new_cat)
        return new_cat

    async def update_salary(self, cat: Cat, body: CatUpdate) -> Cat:
        if body.salary:
            cat.salary = body.salary
        await self.db.commit()
        await self.db.refresh(cat)
        return cat

    async def delete_by_id(self, cat_id: int) -> None:
        cat = await self.get_by_id(cat_id)
        if cat:
            await self.db.delete(cat)
            await self.db.commit()

    async def update_token(self, cat: Cat, refresh_token: Optional[str] = None) -> Cat:
        cat.refresh_token = refresh_token
        await self.db.commit()
        await self.db.refresh(cat)
        return cat

    async def store_reset_token(self, name: str, reset_token: str) -> Cat:
        cat = await self.get_by_name(name)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found"
            )
        cat.reset_token = reset_token
        await self.db.commit()
        await self.db.refresh(cat)
        return cat

    async def verify_reset_token(self, reset_token: str) -> Optional[Cat]:
        result = await self.db.execute(select(Cat).where(Cat.reset_token == reset_token))
        return result.scalars().first()

    async def update_password(self, name: str, new_password: str) -> Cat:
        cat = await self.get_by_name(name)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found"
            )
        hashed_password = password_service.hash_password(new_password)
        cat.password = hashed_password
        await self.db.commit()
        return cat

async def get_cat_repository(db: AsyncSession = Depends(get_db)) -> CatRepository:
    return CatRepository(db)