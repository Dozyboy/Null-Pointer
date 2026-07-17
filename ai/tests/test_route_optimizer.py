from nhip_vien_ai.contracts import (
    CandidateStep,
    OptimizeRoutesRequest,
    RouteCandidate,
    RoutePriority,
)
from nhip_vien_ai.services.route_optimizer import RouteOptimizer


def build_candidate(candidate_id: str, duration: int, distance: int) -> RouteCandidate:
    return RouteCandidate(
        id=candidate_id,
        duration_minutes_min=duration,
        duration_minutes_max=duration + 10,
        distance_meters=distance,
        floor_changes=1,
        is_accessible=True,
        steps=[
            CandidateStep(
                service_code="blood_test",
                room_id=f"{candidate_id}-blood",
                room_name="Lấy máu",
                floor="Tầng 1",
                wait_minutes_min=5,
                wait_minutes_max=10,
            )
        ],
    )


def test_fastest_priority_ranks_shorter_duration_first() -> None:
    request = OptimizeRoutesRequest(
        request_id="request-1",
        encounter_reference="anonymous-encounter",
        priority=RoutePriority.FASTEST,
        required_service_codes={"blood_test"},
        candidates=[
            build_candidate("slow", duration=80, distance=100),
            build_candidate("fast", duration=50, distance=300),
        ],
    )

    response = RouteOptimizer("test-model").optimize(request)

    assert response.options[0].candidate_id == "fast"


def test_candidate_missing_required_service_is_rejected() -> None:
    request = OptimizeRoutesRequest(
        request_id="request-2",
        encounter_reference="anonymous-encounter",
        priority=RoutePriority.SYSTEM,
        required_service_codes={"blood_test", "xray"},
        candidates=[build_candidate("incomplete", duration=50, distance=100)],
    )

    response = RouteOptimizer("test-model").optimize(request)

    assert response.options == []
    assert response.rejected_candidate_ids == ["incomplete"]
