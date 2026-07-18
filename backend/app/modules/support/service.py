from datetime import UTC, datetime
from uuid import uuid4

from app.modules.support.repository import SqliteSupportRequestRepository
from app.modules.support.schemas import CreateSupportRequest, SupportRequestResponse


class SupportRequestNotFoundError(LookupError):
    pass


class SupportRequestService:
    def __init__(self, repository: SqliteSupportRequestRepository) -> None:
        self._repository = repository

    def create(self, request: CreateSupportRequest) -> SupportRequestResponse:
        response = SupportRequestResponse(
            id=f"SUP-{uuid4().hex.upper()}",
            encounter_id=request.encounter_id,
            support_type=request.support_type,
            location=request.location,
            note=request.note,
            status="received",
            is_demo=True,
            estimated_response_minutes_min=3,
            estimated_response_minutes_max=5,
            created_at=datetime.now(UTC),
        )
        self._repository.save(response)
        return response

    def get(self, request_id: str) -> SupportRequestResponse:
        response = self._repository.get_by_id(request_id)
        if response is None:
            raise SupportRequestNotFoundError(request_id)
        return response
