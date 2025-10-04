from fastapi import APIRouter, Depends, status

from src.infrastructure.database.models.tables import Cat
from src.infrastructure.database.repositories.cats import (
    get_cat_repository,
    CatRepository,
)
from src.infrastructure.database.repositories.notes import (
    NoteRepository,
    get_note_repository
)
from src.infrastructure.database.repositories.targets import (
    TargetRepository,
    get_target_repository
)
from src.application.auth import get_current_cat
from src.presentation.schemas.cats import CatProfile
from src.presentation.schemas.notes import NoteCreate, NoteResponse
from src.presentation.schemas.targets import TargetResponse


router = APIRouter(prefix="/cats", tags=["Cats"])


@router.get("/me")
async def get_my_cat(
    cat_repository: CatRepository = Depends(get_cat_repository),
    current_cat: Cat = Depends(get_current_cat),
) -> CatProfile:
    my_cat = CatProfile(
        name=current_cat.name,
        years_of_experience=current_cat.years_of_experience,
        breed=current_cat.breed,
        salary=current_cat.salary,
        created_at=current_cat.created_at,
    )
    return my_cat

@router.put("/target/complete/{target_id}", response_model=TargetResponse, status_code=status.HTTP_200_OK)
async def complete_target(
    target_id: int,
    target_repository: TargetRepository = Depends(get_target_repository),
    current_cat: Cat = Depends(get_current_cat),
):
    target = await target_repository.set_completed_target(
        target_id=target_id,
        current_cat=current_cat
    )
    return target

@router.post("/target/{target_id}", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note_for_target(
    target_id: int,
    note_create: NoteCreate,
    note_repository: NoteRepository = Depends(get_note_repository),
    current_cat: Cat = Depends(get_current_cat),
):
    note = await note_repository.create(
        target_id=target_id,
        content=note_create.content,
        cat_id=current_cat.id
    )
    return note

@router.get("/notes", response_model=list[NoteResponse])
async def get_notes(
    note_repository: NoteRepository = Depends(get_note_repository),
    current_cat: Cat = Depends(get_current_cat),
):
    return await note_repository.get_all_for_cat(current_cat.id)

@router.put("/note/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteCreate,
    note_repository: NoteRepository = Depends(get_note_repository),
    current_cat: Cat = Depends(get_current_cat),
):
    updated_note = await note_repository.update_note(
        note_id=note_id,
        new_content=note_update.content,
        cat_id=current_cat.id
    )
    return updated_note

