from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from nhip_vien_ai.config import Settings, get_settings
from nhip_vien_ai.contracts import (
    OptimizeRoutesRequest,
    OptimizeRoutesResponse,
    WaitEstimateRequest,
    WaitEstimateResponse,
)
from nhip_vien_ai.governance.policy import (
    AuditRecord,
    InMemoryAuditTrail,
    load_policy,
)
from nhip_vien_ai.services.route_optimizer import RouteOptimizer
from nhip_vien_ai.services.wait_time_estimator import WaitTimeEstimator

router = APIRouter()
audit_trail = InMemoryAuditTrail()
SettingsDependency = Annotated[Settings, Depends(get_settings)]


@router.get("/health", tags=["health"])
async def health_check(settings: SettingsDependency) -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai",
        "model_version": settings.model_version,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.post(
    "/v1/route-options",
    response_model=OptimizeRoutesResponse,
    tags=["routing"],
    summary="Xếp hạng các lộ trình đã được backend kiểm tra",
)
async def optimize_routes(
    request: OptimizeRoutesRequest,
    settings: SettingsDependency,
) -> OptimizeRoutesResponse:
    policy = load_policy(settings.governance_policy_path)
    policy.ensure_allowed("rank_prevalidated_routes")
    if len(request.candidates) > policy.max_candidates_per_request:
        raise ValueError("Số phương án vượt giới hạn chính sách")

    response = RouteOptimizer(settings.model_version).optimize(request)
    if policy.audit_enabled:
        audit_trail.append(
            AuditRecord(
                request_id=request.request_id,
                operation="rank_prevalidated_routes",
                action="allowed",
                policy_name=policy.name,
                model_version=settings.model_version,
            )
        )
    return response


@router.post(
    "/v1/wait-estimates",
    response_model=WaitEstimateResponse,
    tags=["waiting"],
    summary="Ước lượng khoảng thời gian chờ",
)
async def estimate_wait(
    request: WaitEstimateRequest,
    settings: SettingsDependency,
) -> WaitEstimateResponse:
    policy = load_policy(settings.governance_policy_path)
    policy.ensure_allowed("estimate_wait_window")
    return WaitTimeEstimator().estimate(request)
