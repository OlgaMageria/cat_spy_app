from typing import List
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.presentation.rest.auth import router as auth_router
# from src.presentation.rest.users import router as users_router
# from src.presentation.rest.issues import router as issues_router
# from src.presentation.rest.chat import router as chat_router
# from src.presentation.rest.manager import router as manager_router
from src.presentation.rest.admin import router as admin_router

from src.infrastructure.database.session import get_db


app = FastAPI(
    title="Spy Cat API",
    description="Web app on Fast API for Spy Cat Agency",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def register_routers(app, routers: List[APIRouter], prefix: str = "/api") -> None:
    for router in routers:
        app.include_router(router, prefix=prefix)


api_routers = [
    auth_router,
#     users_router,
#     issues_router,
#     chat_router,
#     manager_router,
    admin_router,
]

register_routers(app, api_routers)


@app.get("/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        row = result.fetchone()
        if row is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
