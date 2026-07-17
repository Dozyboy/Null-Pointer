from datetime import UTC, datetime

from nhip_vien_ai.contracts import (
    OptimizeRoutesRequest,
    OptimizeRoutesResponse,
    RankedRouteOption,
    RouteCandidate,
    RoutePriority,
)


class RouteOptimizer:
    def __init__(self, model_version: str) -> None:
        self._model_version = model_version

    def optimize(self, request: OptimizeRoutesRequest) -> OptimizeRoutesResponse:
        accepted: list[RouteCandidate] = []
        rejected_ids: list[str] = []

        for candidate in request.candidates:
            service_codes = {step.service_code for step in candidate.steps}
            if not request.required_service_codes.issubset(service_codes):
                rejected_ids.append(candidate.id)
                continue
            if request.priority == RoutePriority.ACCESSIBLE and not candidate.is_accessible:
                rejected_ids.append(candidate.id)
                continue
            accepted.append(candidate)

        ranked = sorted(
            accepted,
            key=lambda candidate: self._score(candidate, request.priority),
        )[: request.max_options]

        return OptimizeRoutesResponse(
            request_id=request.request_id,
            model_version=self._model_version,
            generated_at=datetime.now(UTC),
            options=[
                RankedRouteOption(
                    candidate_id=candidate.id,
                    rank=index + 1,
                    score=round(self._score(candidate, request.priority), 3),
                    reason_codes=self._reason_codes(request.priority),
                )
                for index, candidate in enumerate(ranked)
            ],
            rejected_candidate_ids=rejected_ids,
        )

    def _score(self, candidate: RouteCandidate, priority: RoutePriority) -> float:
        average_duration = (
            candidate.duration_minutes_min + candidate.duration_minutes_max
        ) / 2
        average_wait = sum(
            (step.wait_minutes_min + step.wait_minutes_max) / 2
            for step in candidate.steps
        )

        if priority == RoutePriority.FASTEST:
            return average_duration
        if priority == RoutePriority.LESS_WALK:
            return candidate.distance_meters + candidate.floor_changes * 100
        if priority == RoutePriority.LESS_CROWD:
            return average_wait
        if priority == RoutePriority.ACCESSIBLE:
            return average_duration + candidate.distance_meters / 20
        return (
            average_duration
            + average_wait * 0.25
            + candidate.distance_meters / 25
            + candidate.floor_changes * 5
        )

    def _reason_codes(self, priority: RoutePriority) -> list[str]:
        reason_by_priority = {
            RoutePriority.SYSTEM: ["balanced_duration_wait_distance"],
            RoutePriority.FASTEST: ["lowest_expected_duration"],
            RoutePriority.LESS_WALK: ["shorter_distance_and_fewer_floors"],
            RoutePriority.LESS_CROWD: ["lower_expected_queue"],
            RoutePriority.ACCESSIBLE: ["accessible_route_only"],
        }
        return reason_by_priority[priority]
