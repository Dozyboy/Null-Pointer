import httpx

from app.core.config import Settings
from app.intelligence.contracts import (
    AiOptimizeRoutesRequest,
    AiOptimizeRoutesResponse,
)


class AiRoutingClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.ai_service_url.rstrip("/")
        self._timeout = settings.ai_request_timeout_seconds

    async def rank_options(
        self,
        request: AiOptimizeRoutesRequest,
    ) -> AiOptimizeRoutesResponse:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/v1/route-options",
                json=request.model_dump(mode="json"),
            )
            response.raise_for_status()
            return AiOptimizeRoutesResponse.model_validate(response.json())
