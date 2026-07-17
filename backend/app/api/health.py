from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Kiểm tra dịch vụ")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "backend",
        "timestamp": datetime.now(UTC).isoformat(),
    }
