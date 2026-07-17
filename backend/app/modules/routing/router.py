from fastapi import APIRouter, status

from app.modules.routing.schemas import (
    CreateRouteProposalRequest,
    RouteProposalResponse,
)
from app.modules.routing.service import RouteProposalService

router = APIRouter(prefix="/encounters", tags=["routing"])
service = RouteProposalService()


@router.post(
    "/{encounter_id}/route-proposals",
    response_model=RouteProposalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo các phương án lộ trình",
)
async def create_route_proposal(
    encounter_id: str,
    request: CreateRouteProposalRequest,
) -> RouteProposalResponse:
    return service.create_demo_proposal(encounter_id, request)
