from typing import Protocol

from app.intelligence.contracts import (
    AiOptimizeRoutesRequest,
    AiOptimizeRoutesResponse,
)


class RoutingEnginePort(Protocol):
    async def rank_options(
        self,
        request: AiOptimizeRoutesRequest,
    ) -> AiOptimizeRoutesResponse: ...


class WaitEstimatorPort(Protocol):
    async def estimate_wait_minutes(
        self,
        queue_length: int,
        average_service_minutes: float,
        active_capacity: int,
    ) -> tuple[int, int]: ...
