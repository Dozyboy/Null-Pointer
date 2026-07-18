from fastapi import APIRouter, HTTPException, status

from app.modules.support.runtime import support_request_service as service
from app.modules.support.schemas import (
    CreateSupportRequest,
    SupportRequestResponse,
)
from app.modules.support.service import SupportRequestNotFoundError

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
    return service.create(request)


@router.get(
    "/{request_id}",
    response_model=SupportRequestResponse,
    summary="Đọc trạng thái yêu cầu hỗ trợ",
)
async def get_support_request(request_id: str) -> SupportRequestResponse:
    try:
        return service.get(request_id)
    except SupportRequestNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy yêu cầu hỗ trợ.",
        ) from error
