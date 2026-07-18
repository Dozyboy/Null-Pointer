from datetime import UTC, datetime, timedelta
from threading import RLock
from typing import Protocol
from uuid import uuid4

from app.modules.audit.schemas import PatientActivityType
from app.modules.audit.service import PatientActivityLogService
from app.modules.reservations.exceptions import (
    ReservationExpiredError,
    ReservationNotFoundError,
    ReservationStateError,
)
from app.modules.reservations.repository import (
    InMemoryRouteReservationRepository,
    ReservationRecord,
    RouteReservationRepository,
)
from app.modules.reservations.schemas import (
    CreateRouteReservationRequest,
    JourneyStatus,
    ReservationStatus,
    RouteReservationResponse,
)
from app.modules.routing.runtime import route_proposal_service
from app.modules.routing.schemas import RouteProposalResponse
from app.modules.routing.service import RouteProposalService


class ClinicalOrderRouteUpdater(Protocol):
    def commit_route_proposal(
        self,
        clinical_order_id: str,
        proposal: RouteProposalResponse,
    ) -> None: ...


class RouteReservationService:
    """Giữ chỗ demo có khóa đồng thời và xác nhận lặp an toàn."""

    def __init__(
        self,
        proposal_service: RouteProposalService | None = None,
        hold_seconds: int = 120,
        repository: RouteReservationRepository | None = None,
        activities: PatientActivityLogService | None = None,
        route_updater: ClinicalOrderRouteUpdater | None = None,
    ) -> None:
        self._proposal_service = proposal_service or route_proposal_service
        self._hold_seconds = hold_seconds
        self._repository = repository or InMemoryRouteReservationRepository()
        self._activities = activities
        self._route_updater = route_updater
        self._lock = RLock()

    def create_hold(
        self,
        request: CreateRouteReservationRequest,
    ) -> RouteReservationResponse:
        now = datetime.now(UTC)
        with self._lock:
            existing = self._repository.get_by_idempotency_key(request.idempotency_key)
            if existing is not None:
                if self._expire_if_needed(existing, now):
                    self._repository.save(existing)
                if existing.status in {
                    ReservationStatus.HELD,
                    ReservationStatus.CONFIRMED,
                }:
                    return self._to_response(existing)

            self._proposal_service.get_valid_option(
                request.route_proposal_id,
                request.route_option_id,
                request.encounter_id,
            )
            record = ReservationRecord(
                id=str(uuid4()),
                encounter_id=request.encounter_id,
                route_proposal_id=request.route_proposal_id,
                route_option_id=request.route_option_id,
                idempotency_key=request.idempotency_key,
                status=ReservationStatus.HELD,
                created_at=now,
                expires_at=now + timedelta(seconds=self._hold_seconds),
                patient_code=request.patient_code,
                clinical_order_id=request.clinical_order_id,
            )
            self._repository.save(record)
            return self._to_response(record)

    def confirm(self, reservation_id: str) -> RouteReservationResponse:
        now = datetime.now(UTC)
        with self._lock:
            record = self._get_record(reservation_id)
            if self._expire_if_needed(record, now):
                self._repository.save(record)
            if record.status is ReservationStatus.CONFIRMED:
                return self._to_response(record)
            if record.status is ReservationStatus.EXPIRED:
                raise ReservationExpiredError("Chỗ giữ đã hết hạn")
            if record.status is not ReservationStatus.HELD:
                raise ReservationStateError("Chỗ giữ không còn ở trạng thái có thể xác nhận")
            proposal, _ = self._proposal_service.get_valid_option(
                record.route_proposal_id,
                record.route_option_id,
                record.encounter_id,
            )
            record.status = ReservationStatus.CONFIRMED
            record.confirmed_at = now
            record.journey_id = record.journey_id or f"journey-{uuid4()}"
            record.journey_status = JourneyStatus.ACTIVE
            self._repository.save(record)
            if record.clinical_order_id and self._route_updater:
                self._route_updater.commit_route_proposal(
                    record.clinical_order_id,
                    proposal,
                )
            if record.patient_code and self._activities:
                self._activities.record(
                    idempotency_key=f"reservation:{record.id}:confirmed",
                    patient_code=record.patient_code,
                    encounter_id=record.encounter_id,
                    activity_type=PatientActivityType.ROUTE_CONFIRMED,
                    title="Đã xác nhận lộ trình",
                    description="Hệ thống đã giữ chỗ và bắt đầu theo dõi tiến độ hành trình.",
                    clinical_order_id=record.clinical_order_id,
                    reservation_id=record.id,
                    occurred_at=now,
                )
            return self._to_response(record)

    def extend(self, reservation_id: str) -> RouteReservationResponse:
        now = datetime.now(UTC)
        with self._lock:
            record = self._get_record(reservation_id)
            if self._expire_if_needed(record, now):
                self._repository.save(record)
            if record.status is ReservationStatus.EXPIRED:
                raise ReservationExpiredError("Chỗ giữ đã hết hạn")
            if record.status is not ReservationStatus.HELD:
                raise ReservationStateError("Chỉ có thể gia hạn chỗ đang được giữ")
            if record.extension_count >= 1:
                raise ReservationStateError("Bản demo chỉ cho phép gia hạn một lần")
            record.extension_count += 1
            record.expires_at = max(now, record.expires_at) + timedelta(
                seconds=self._hold_seconds
            )
            self._repository.save(record)
            return self._to_response(record)

    def get_latest_for_patient(self, patient_code: str) -> RouteReservationResponse:
        with self._lock:
            record = self._repository.get_latest_for_patient(patient_code.strip())
            if record is None:
                raise ReservationNotFoundError("Bệnh nhân chưa có hành trình đã lưu")
            return self._to_response(record)

    def update_progress(
        self,
        reservation_id: str,
        *,
        current_step: int,
        journey_status: JourneyStatus,
    ) -> RouteReservationResponse:
        with self._lock:
            record = self._get_record(reservation_id)
            if record.status is not ReservationStatus.CONFIRMED:
                raise ReservationStateError("Chỉ cập nhật được hành trình đã xác nhận")
            previous_step = record.current_step
            previous_status = record.journey_status
            if previous_step == current_step and previous_status is journey_status:
                return self._to_response(record)
            record.current_step = current_step
            record.journey_status = journey_status
            self._repository.save(record)
            if record.patient_code and self._activities:
                is_completed = journey_status is JourneyStatus.COMPLETED
                self._activities.record(
                    idempotency_key=(
                        f"reservation:{record.id}:progress:{current_step}:"
                        f"{journey_status.value}"
                    ),
                    patient_code=record.patient_code,
                    encounter_id=record.encounter_id,
                    activity_type=(
                        PatientActivityType.JOURNEY_COMPLETED
                        if is_completed
                        else PatientActivityType.SERVICE_COMPLETED
                    ),
                    title=(
                        "Đã hoàn thành hành trình khám"
                        if is_completed
                        else f"Đã hoàn thành dịch vụ bước {previous_step + 1}"
                    ),
                    description=(
                        f"Hệ thống đã ghi nhận hoàn thành tại bước {current_step + 1}."
                        if is_completed
                        else f"Hành trình đã chuyển sang bước {current_step + 1}."
                    ),
                    clinical_order_id=record.clinical_order_id,
                    reservation_id=record.id,
                )
            return self._to_response(record)

    def reset(self) -> None:
        with self._lock:
            self._repository.clear()

    def _get_record(self, reservation_id: str) -> ReservationRecord:
        record = self._repository.get_by_id(reservation_id)
        if record is None:
            raise ReservationNotFoundError("Không tìm thấy lượt giữ chỗ")
        return record

    @staticmethod
    def _expire_if_needed(record: ReservationRecord, now: datetime) -> bool:
        if record.status is ReservationStatus.HELD and record.expires_at <= now:
            record.status = ReservationStatus.EXPIRED
            return True
        return False

    @staticmethod
    def _to_response(record: ReservationRecord) -> RouteReservationResponse:
        return RouteReservationResponse(
            id=record.id,
            encounter_id=record.encounter_id,
            route_proposal_id=record.route_proposal_id,
            route_option_id=record.route_option_id,
            status=record.status,
            is_demo=True,
            created_at=record.created_at,
            expires_at=record.expires_at,
            confirmed_at=record.confirmed_at,
            journey_id=record.journey_id,
            extension_count=record.extension_count,
            patient_code=record.patient_code,
            clinical_order_id=record.clinical_order_id,
            current_step=record.current_step,
            journey_status=record.journey_status,
        )
