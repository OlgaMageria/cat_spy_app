from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.application.auth import get_current_admin
from src.presentation.schemas.cats import CatResponse
from src.infrastructure.database.models.tables import Cat
from src.infrastructure.database.repositories.cats import (
    get_cat_repository,
    CatRepository,
)


router = APIRouter(prefix="/admin", tags=["Admins"])

    
@router.get("/cats")
async def get_all_cats(
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    return await cat_repository.get_all_cats()

@router.get("/cats/name", response_model=list[CatResponse])
async def get_cat_by_name(
    search_query: str = Query(..., min_length=1),
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    cats_by_query = await cat_repository.search_by_name(search_query)
    if not cats_by_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    return cats_by_query

@router.delete("/cats/delete/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat_by_id(
    cat_id: int,
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    cat = await cat_repository.get_by_id(cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    await cat_repository.delete_by_id(cat_id)
    return

@router.get("/cats/{cat_id}")
async def get_cat_by_id(
    cat_id: int,
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    cat = await cat_repository.get_by_id(cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    return cat



