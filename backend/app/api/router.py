from fastapi import APIRouter

from app.api.health import router as health_router
from app.modules.routing.router import router as routing_router
from app.modules.support.router import router as support_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(routing_router, prefix="/api/v1")
api_router.include_router(support_router, prefix="/api/v1")
