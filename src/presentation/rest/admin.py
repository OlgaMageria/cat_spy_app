from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.application.auth import get_current_admin
from src.presentation.schemas.cats import CatResponse
from src.presentation.schemas.missions import MissionCreate, MissionResponse, AssignCatsRequest
from src.infrastructure.database.models.tables import Cat
from src.infrastructure.database.repositories.cats import (
    get_cat_repository,
    CatRepository,
)
from src.infrastructure.database.repositories.missions import (
    get_mission_repository,
    MissionRepository,
)


router = APIRouter(prefix="/admin", tags=["Admins"])

    
@router.get("/cats")
async def get_all_cats(
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Get all cats in the system. Admin access required."""
    return await cat_repository.get_all_cats()

@router.get("/cats/name", response_model=list[CatResponse])
async def get_cat_by_name(
    search_query: str = Query(..., min_length=1),
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Get a cat by its name. Admin access required."""
    cats_by_query = await cat_repository.search_by_name(search_query)
    if not cats_by_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    return cats_by_query

@router.put("/cats/update/{cat_id}", response_model=CatResponse)
async def update_cat_salary(
    cat_id: int,
    salary: int = Query(..., ge=0),
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Update a cat's salary. Admin access required."""
    cat = await cat_repository.get_by_id(cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    updated_cat = await cat_repository.update_salary(cat, salary)
    return updated_cat

@router.delete("/cats/delete/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat_by_id(
    cat_id: int,
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Delete a cat by its ID. Admin access required."""
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
    """Get a cat by its ID. Admin access required."""
    cat = await cat_repository.get_by_id(cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    return cat

@router.post("/mission/create", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission(
    body: MissionCreate,
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Create a new mission. Admin access required."""
    new_mission = await mission_repository.create(body)
    return MissionResponse.from_mission(new_mission)

@router.get("/missions", response_model=list[MissionResponse])
async def get_all_missions(
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Get all missions in the system. Admin access required."""
    missions = await mission_repository.get_all_missions()
    return [MissionResponse.from_mission(mission) for mission in missions]

@router.get("/mission/{mission_id}", response_model=MissionResponse)
async def get_mission_by_id(
    mission_id: int,
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Get a mission by its ID. Admin access required."""
    mission = await mission_repository.get_by_id(mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    return MissionResponse.from_mission(mission)

@router.delete("/mission/delete/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission_by_id(
    mission_id: int,
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Delete a mission by its ID. Admin access required."""
    mission = await mission_repository.get_by_id(mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
        )
    await mission_repository.delete_mission_by_id(mission_id)

@router.put("/mission/complete/{mission_id}", response_model=MissionResponse)
async def complete_mission_by_id(
    mission_id: int,
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Mark a mission as completed by its ID. Admin access required."""
    mission = await mission_repository.set_completed_mission(mission_id)
    return MissionResponse.from_mission(mission)

@router.put("/mission/assign/{mission_id}", response_model=MissionResponse)
async def assign_cats_to_mission(
    mission_id: int,
    request: AssignCatsRequest,
    mission_repository: MissionRepository = Depends(get_mission_repository),
    current_cat: Cat = Depends(get_current_admin),
):
    """Assign cats to a mission. Admin access required."""
    if not request.cat_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cat_ids query parameter is required and cannot be empty"
        )
    mission = await mission_repository.assigne_cats_to_mission(mission_id, request.cat_ids)
    return MissionResponse.from_mission(mission)
