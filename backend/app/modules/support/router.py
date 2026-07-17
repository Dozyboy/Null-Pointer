from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, status

from app.modules.support.schemas import (
    CreateSupportRequest,
    SupportRequestResponse,
)

router = APIRouter(prefix="/support-requests", tags=["support"])


@router.post(
    "",
    response_model=SupportRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo yêu cầu hỗ trợ",
)
async def create_support_request(
    request: CreateSupportRequest,
) -> SupportRequestResponse:
    del request
    return SupportRequestResponse(
        id=str(uuid4()),
        status="received",
        is_demo=True,
        estimated_response_minutes_min=3,
        estimated_response_minutes_max=5,
        created_at=datetime.now(UTC),
    )
