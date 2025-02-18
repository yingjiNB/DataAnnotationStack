from fastapi import APIRouter
from backend.api.v1.endpoints import files, annotations
from backend.routers import files as file_router

api_router = APIRouter()

api_router.include_router(
    files.router,
    prefix="/files",
    tags=["files"]
)

api_router.include_router(
    file_router.router,
    prefix="/files",
    tags=["files"]
)

api_router.include_router(
    annotations.router,
    prefix="/annotations",
    tags=["annotations"]
) 