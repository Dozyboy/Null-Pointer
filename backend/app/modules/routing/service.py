from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.modules.routing.schemas import (
    CreateRouteProposalRequest,
    RouteLabel,
    RouteOptionResponse,
    RouteProposalResponse,
    RouteStepResponse,
)


class RouteProposalService:
    """Dịch vụ minh họa; sẽ được thay bằng kho dữ liệu và cổng AI."""

    def create_demo_proposal(
        self,
        encounter_id: str,
        request: CreateRouteProposalRequest,
    ) -> RouteProposalResponse:
        now = datetime.now(UTC)
        options = [
            self._build_option(
                label=RouteLabel.RECOMMENDED,
                rooms=("Lấy máu 01", "X-quang 03", "Siêu âm 05"),
                waits=((5, 10), (10, 20), (15, 25)),
                duration=(65, 85),
                distance=260,
                floor_changes=1,
                reason="Tận dụng thời gian xử lý mẫu máu để thực hiện các bước tiếp theo.",
            ),
            self._build_option(
                label=RouteLabel.LESS_WALK,
                rooms=("Lấy máu 02", "X-quang 01", "Siêu âm 02"),
                waits=((10, 15), (15, 25), (20, 30)),
                duration=(75, 95),
                distance=110,
                floor_changes=0,
                reason="Giảm quãng đường và không phải đổi tầng.",
            ),
            self._build_option(
                label=RouteLabel.LESS_CROWD,
                rooms=("Lấy máu 03", "X-quang 02", "Siêu âm 04"),
                waits=((3, 8), (5, 12), (8, 15)),
                duration=(70, 90),
                distance=320,
                floor_changes=1,
                reason="Các khu chờ dự kiến ít người hơn tại thời điểm tạo đề xuất.",
            ),
        ]
        return RouteProposalResponse(
            id=str(uuid4()),
            encounter_id=encounter_id,
            priority=request.priority,
            is_demo=True,
            updated_at=now,
            expires_at=now + timedelta(seconds=30),
            options=options,
        )

    def _build_option(
        self,
        *,
        label: RouteLabel,
        rooms: tuple[str, str, str],
        waits: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
        duration: tuple[int, int],
        distance: int,
        floor_changes: int,
        reason: str,
    ) -> RouteOptionResponse:
        services = (
            ("blood_test", "Xét nghiệm máu", "Tầng 1"),
            ("chest_xray", "Chụp X-quang ngực", "Tầng 2"),
            ("abdominal_ultrasound", "Siêu âm bụng", "Tầng 2"),
        )
        steps = [
            RouteStepResponse(
                id=str(uuid4()),
                order=index + 1,
                service_code=service[0],
                service_name=service[1],
                room_name=rooms[index],
                floor=service[2] if label != RouteLabel.LESS_WALK else "Tầng 1",
                wait_minutes_min=waits[index][0],
                wait_minutes_max=waits[index][1],
                is_locked=index == 0,
                lock_reason=(
                    "Lấy máu trước để mẫu được xử lý trong lúc thực hiện bước khác."
                    if index == 0
                    else None
                ),
            )
            for index, service in enumerate(services)
        ]
        return RouteOptionResponse(
            id=str(uuid4()),
            label=label,
            duration_minutes_min=duration[0],
            duration_minutes_max=duration[1],
            distance_meters=distance,
            floor_changes=floor_changes,
            reason=reason,
            steps=steps,
        )
