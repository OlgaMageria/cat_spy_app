from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from src.infrastructure.database.models.tables import Cat
from src.presentation.schemas.cats import (
    TokenModel,
    CatModel,
    PasswordResetRequest,
    PasswordReset,
)
from src.application.auth import auth_service
from src.application.password_service import password_service
from src.infrastructure.database.repositories.cats import (
    get_cat_repository,
    CatRepository,
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter(prefix="/auth", tags=["Authorization"])
get_refresh_token = HTTPBearer()


@router.post("/signup")
async def signup(
    body: CatModel,
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    exist_cat = await cat_repository.get_by_name(body.name)
    if exist_cat:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    body.password = password_service.get_password_hash(body.password)
    new_cat = await cat_repository.create(body)
    return new_cat


@router.post("/login", response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login(
    body: OAuth2PasswordRequestForm = Depends(),
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    cat = await cat_repository.get_by_name(body.username)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid name or password"
        )
    if not password_service.verify_password(body.password, cat.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(data={"sub": cat.name})
    refresh_token = await auth_service.create_refresh_token(data={"sub": cat.name})
    await cat_repository.update_token(cat, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    current_cat: Cat = Depends(auth_service.get_current_cat),
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    token = credentials.credentials
    name = await auth_service.decode_refresh_token(token)
    cat = await cat_repository.get_by_name(name)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )
    if cat.refresh_token != token:
        await cat_repository.update_token(cat, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": name})
    refresh_token = await auth_service.create_refresh_token(data={"sub": name})
    await cat_repository.update_token(cat, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/forgot_password")
async def forgot_password(
    body: PasswordResetRequest,
    request: Request,
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    cat = await cat_repository.get_by_name(body.name)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    reset_token = auth_service.create_email_token({"sub": body.email})

    await cat_repository.store_reset_token(cat.name, reset_token)

    return {"message": "Reset password link sent to your email"}


@router.post("/reset_password/{token}")
async def reset_password(
    body: PasswordReset,
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    name = await auth_service.get_name_from_token(body.token)
    cat = await cat_repository.get_by_name(name)

    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
        )
    if not await cat_repository.verify_reset_token(cat.name, body.token):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    await cat_repository.update_password(cat.name, body.new_password)
    return {"message": "Password reset successfully"}
