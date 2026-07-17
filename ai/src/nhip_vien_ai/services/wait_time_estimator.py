import math

from nhip_vien_ai.contracts import WaitEstimateRequest, WaitEstimateResponse


class WaitTimeEstimator:
    def __init__(self, model_version: str = "queue-window-v1") -> None:
        self._model_version = model_version

    def estimate(self, request: WaitEstimateRequest) -> WaitEstimateResponse:
        expected = (
            request.queue_length
            * request.average_service_minutes
            / request.active_capacity
        )
        return WaitEstimateResponse(
            wait_minutes_min=max(0, math.floor(expected * 0.8)),
            wait_minutes_max=max(0, math.ceil(expected * 1.2)),
            model_version=self._model_version,
        )
