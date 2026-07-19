import re
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import islice, permutations, product
from math import ceil

from app.modules.routing.catalog import (
    SERVICE_CATALOG,
    LockedPosition,
    ServiceDefinition,
)
from app.modules.routing.exceptions import NoFeasibleRouteError
from app.modules.routing.schemas import (
    CreateRouteProposalRequest,
    RouteLabel,
    ScheduleStrategy,
    ServiceCode,
)
from app.modules.simulation.schemas import (
    EquipmentStatus,
    RoomSnapshot,
    RoomStatus,
    SimulationSnapshot,
)
from app.shared.enums import RoutePriority

ALGORITHM_VERSION = "deterministic-routing-v2"
MAX_CANDIDATES = 200


@dataclass(frozen=True, slots=True)
class PlannedStep:
    service: ServiceDefinition
    room: RoomSnapshot
    wait_minutes_min: int
    wait_minutes_max: int
    service_minutes: int
    travel_minutes: int
    arrival_minutes: int
    complete_minutes: int
    result_ready_minutes: int


@dataclass(frozen=True, slots=True)
class RouteCandidate:
    key: str
    steps: tuple[PlannedStep, ...]
    duration_minutes_min: int
    duration_minutes_max: int
    distance_meters: int
    floor_changes: int
    total_wait_minutes: int
    tests_wait_minutes: int
    total_queue_patients: int
    first_service_start_minutes: int
    tests_completed_minutes: int
    results_ready_minutes: int
    doctor_return_minutes: int | None
    is_accessible: bool


@dataclass(frozen=True, slots=True)
class RankedCandidate:
    label: RouteLabel
    candidate: RouteCandidate
    ranking_score: float
    reason: str


class DeterministicRoutingOptimizer:
    """Sinh và chấm điểm phương án bằng quy tắc có thể giải thích và kiểm thử."""

    def optimize(
        self,
        snapshot: SimulationSnapshot,
        request: CreateRouteProposalRequest,
        *,
        service_catalog: Mapping[ServiceCode, ServiceDefinition] | None = None,
        allowed_room_locations: Mapping[ServiceCode, frozenset[str]] | None = None,
    ) -> list[RankedCandidate]:
        candidates = self._generate_candidates(
            snapshot,
            request,
            service_catalog=service_catalog or SERVICE_CATALOG,
            allowed_room_locations=allowed_room_locations or {},
        )
        if not candidates:
            raise NoFeasibleRouteError(
                "Không có phương án đáp ứng đầy đủ chỉ định với trạng thái phòng hiện tại."
            )

        label_by_strategy = {
            ScheduleStrategy.BALANCED: RouteLabel.BALANCED,
            ScheduleStrategy.FINISH_EARLY: RouteLabel.EARLY_SERVICE,
            ScheduleStrategy.LEAVE_FAST: RouteLabel.DOCTOR_READY,
        }
        ordered_strategies = (
            request.schedule_strategy,
            *(
                strategy
                for strategy in ScheduleStrategy
                if strategy != request.schedule_strategy
            ),
        )
        selected: list[RankedCandidate] = []

        for strategy in ordered_strategies:
            label = label_by_strategy[strategy]
            ranked = sorted(
                candidates,
                key=lambda candidate: (
                    self._score(candidate, request.priority, strategy),
                    candidate.key,
                ),
            )
            candidate = ranked[0]

            selected.append(
                RankedCandidate(
                    label=label,
                    candidate=candidate,
                    ranking_score=round(
                        self._score(candidate, request.priority, strategy),
                        3,
                    ),
                    reason=self._build_reason(label, request.priority, strategy),
                )
            )

        return selected

    def _generate_candidates(
        self,
        snapshot: SimulationSnapshot,
        request: CreateRouteProposalRequest,
        *,
        service_catalog: Mapping[ServiceCode, ServiceDefinition],
        allowed_room_locations: Mapping[ServiceCode, frozenset[str]],
    ) -> list[RouteCandidate]:
        service_definitions = [
            service_catalog[service_code]
            for service_code in request.required_service_codes
        ]
        room_options = self._room_options(
            snapshot,
            service_definitions,
            allowed_room_locations=allowed_room_locations,
        )
        sequences = self._service_sequences(service_definitions)
        candidates: list[RouteCandidate] = []

        sequence_limit = min(len(sequences), MAX_CANDIDATES)
        candidates_per_sequence = max(1, MAX_CANDIDATES // sequence_limit)

        for sequence in sequences[:sequence_limit]:
            options_in_sequence = [room_options[service.code] for service in sequence]
            for selected_rooms in islice(
                product(*options_in_sequence),
                candidates_per_sequence,
            ):
                candidates.append(
                    self._simulate_candidate(
                        snapshot,
                        request,
                        sequence,
                        selected_rooms,
                    )
                )

        return candidates

    def _room_options(
        self,
        snapshot: SimulationSnapshot,
        services: list[ServiceDefinition],
        *,
        allowed_room_locations: Mapping[ServiceCode, frozenset[str]],
    ) -> dict[ServiceCode, list[RoomSnapshot]]:
        active_rooms = [
            room
            for room in snapshot.rooms
            if room.status != RoomStatus.PAUSED
            and room.equipment_status == EquipmentStatus.OPERATIONAL
        ]
        options: dict[ServiceCode, list[RoomSnapshot]] = {}

        for service in services:
            configured_locations = allowed_room_locations.get(service.code)
            matching_rooms = [
                room
                for room in active_rooms
                if room.service_type == service.room_service_type
                and (
                    configured_locations is None
                    or room.location_code in configured_locations
                )
            ]
            if not matching_rooms:
                raise NoFeasibleRouteError(
                    f"Không có phòng phù hợp đang hoạt động cho dịch vụ {service.name}."
                )
            matching_rooms.sort(
                key=lambda room: (
                    room.status == RoomStatus.OVERLOADED,
                    room.estimated_wait_minutes,
                    room.waiting_patients,
                    room.code,
                )
            )
            options[service.code] = matching_rooms

        return options

    def _service_sequences(
        self,
        services: list[ServiceDefinition],
    ) -> list[tuple[ServiceDefinition, ...]]:
        first = [
            service
            for service in services
            if service.locked_position == LockedPosition.FIRST
        ]
        last = [
            service
            for service in services
            if service.locked_position == LockedPosition.LAST
        ]
        middle = [
            service
            for service in services
            if service.locked_position is None
        ]
        middle_orders = list(permutations(middle)) if middle else [()]
        return [tuple(first) + order + tuple(last) for order in middle_orders]

    def _simulate_candidate(
        self,
        snapshot: SimulationSnapshot,
        request: CreateRouteProposalRequest,
        sequence: tuple[ServiceDefinition, ...],
        selected_rooms: tuple[RoomSnapshot, ...],
    ) -> RouteCandidate:
        room_by_code = {room.code: room for room in snapshot.rooms}
        previous_room = room_by_code.get(request.start_room_code or "")
        elapsed_minutes = 0
        total_distance = 0
        floor_changes = 0
        total_wait = 0
        tests_wait = 0
        total_queue_patients = 0
        first_service_start: int | None = None
        tests_completed = 0
        results_ready = 0
        doctor_return: int | None = None
        uncertainty_minutes = 0
        planned_steps: list[PlannedStep] = []

        for service, room in zip(sequence, selected_rooms, strict=True):
            distance, changed_floors = self._travel_metrics(previous_room, room)
            travel_minutes = self._travel_minutes(distance, request)
            total_distance += distance
            floor_changes += changed_floors
            arrival_minutes = elapsed_minutes + travel_minutes

            queue_from_patient_count = (
                room.waiting_patients * room.average_service_minutes
            )
            current_room_wait = max(
                room.estimated_wait_minutes,
                queue_from_patient_count,
            )
            projected_queue = max(0, current_room_wait - arrival_minutes)
            wait_min = max(0, round(projected_queue * 0.75))
            wait_max = max(wait_min, ceil(projected_queue * 1.25) + 2)
            expected_wait = (wait_min + wait_max) // 2

            if service.locked_position == LockedPosition.LAST:
                earliest_start = max(arrival_minutes + expected_wait, results_ready)
                expected_wait = earliest_start - arrival_minutes
                wait_min = max(0, expected_wait - 2)
                wait_max = expected_wait + 3

            complete_minutes = arrival_minutes + expected_wait + room.average_service_minutes
            result_ready_minutes = complete_minutes + service.result_turnaround_minutes
            total_wait += expected_wait
            uncertainty_minutes += max(0, wait_max - wait_min)

            if service.locked_position == LockedPosition.LAST:
                doctor_return = complete_minutes
            else:
                tests_wait += expected_wait
                total_queue_patients += room.waiting_patients
                if first_service_start is None:
                    first_service_start = arrival_minutes + expected_wait
                tests_completed = max(tests_completed, complete_minutes)
                results_ready = max(results_ready, result_ready_minutes)

            planned_steps.append(
                PlannedStep(
                    service=service,
                    room=room,
                    wait_minutes_min=wait_min,
                    wait_minutes_max=wait_max,
                    service_minutes=room.average_service_minutes,
                    travel_minutes=travel_minutes,
                    arrival_minutes=arrival_minutes,
                    complete_minutes=complete_minutes,
                    result_ready_minutes=result_ready_minutes,
                )
            )
            elapsed_minutes = complete_minutes
            previous_room = room

        expected_duration = max(elapsed_minutes, results_ready)
        half_uncertainty = ceil(uncertainty_minutes / 2)
        candidate_key = "|".join(
            f"{step.service.code}:{step.room.code}" for step in planned_steps
        )
        return RouteCandidate(
            key=candidate_key,
            steps=tuple(planned_steps),
            duration_minutes_min=max(0, expected_duration - half_uncertainty),
            duration_minutes_max=expected_duration + half_uncertainty,
            distance_meters=total_distance,
            floor_changes=floor_changes,
            total_wait_minutes=total_wait,
            tests_wait_minutes=tests_wait,
            total_queue_patients=total_queue_patients,
            first_service_start_minutes=first_service_start or 0,
            tests_completed_minutes=tests_completed,
            results_ready_minutes=results_ready,
            doctor_return_minutes=doctor_return,
            is_accessible=True,
        )

    def _score(
        self,
        candidate: RouteCandidate,
        priority: RoutePriority,
        strategy: ScheduleStrategy,
    ) -> float:
        expected_duration = (
            candidate.duration_minutes_min + candidate.duration_minutes_max
        ) / 2

        if strategy == ScheduleStrategy.FINISH_EARLY:
            score = (
                candidate.tests_completed_minutes * 0.55
                + candidate.first_service_start_minutes * 0.25
                + candidate.tests_wait_minutes * 0.15
                + candidate.total_queue_patients * 0.5
                + candidate.distance_meters / 100
            )
        elif strategy == ScheduleStrategy.LEAVE_FAST:
            doctor_ready = candidate.doctor_return_minutes or expected_duration
            score = (
                doctor_ready * 0.7
                + candidate.results_ready_minutes * 0.25
                + candidate.total_wait_minutes * 0.05
            )
        else:
            score = (
                expected_duration * 0.35
                + candidate.results_ready_minutes * 0.2
                + candidate.tests_completed_minutes * 0.1
                + candidate.total_wait_minutes * 0.2
                + candidate.total_queue_patients * 0.5
                + candidate.distance_meters / 30
                + candidate.floor_changes * 4
            )

        if priority == RoutePriority.FASTEST:
            score += expected_duration * 0.1
        elif priority == RoutePriority.LESS_WALK:
            score += candidate.distance_meters / 6 + candidate.floor_changes * 12
        elif priority == RoutePriority.LESS_CROWD:
            score += candidate.total_wait_minutes * 1.5
        elif priority == RoutePriority.ACCESSIBLE:
            if not candidate.is_accessible:
                return float("inf")
            score += candidate.distance_meters / 8 + candidate.floor_changes * 18

        return score

    def _travel_metrics(
        self,
        previous_room: RoomSnapshot | None,
        next_room: RoomSnapshot,
    ) -> tuple[int, int]:
        if previous_room is None or previous_room.code == next_room.code:
            return 0, 0

        previous_floor = self._floor_number(previous_room.floor)
        next_floor = self._floor_number(next_room.floor)
        floor_gap = abs(previous_floor - next_floor)
        if floor_gap > 0:
            return 60 + floor_gap * 85, floor_gap

        room_gap = abs(
            self._room_number(previous_room.code) - self._room_number(next_room.code)
        )
        return 35 + min(65, room_gap // 3), 0

    def _travel_minutes(
        self,
        distance_meters: int,
        request: CreateRouteProposalRequest,
    ) -> int:
        needs_assistance = any(
            (
                request.accessibility.wheelchair,
                request.accessibility.avoid_stairs,
                request.accessibility.visual_assistance,
            )
        )
        meters_per_minute = 40 if needs_assistance else 65
        return ceil(distance_meters / meters_per_minute)

    def _floor_number(self, floor: str) -> int:
        match = re.search(r"\d+", floor)
        return int(match.group()) if match else 0

    def _room_number(self, room_code: str) -> int:
        match = re.search(r"\d+", room_code)
        return int(match.group()) if match else 0

    def _build_reason(
        self,
        label: RouteLabel,
        priority: RoutePriority,
        strategy: ScheduleStrategy,
    ) -> str:
        strategy_reasons = {
            ScheduleStrategy.BALANCED: (
                "Cân bằng thời gian chờ, thời điểm có kết quả và việc di chuyển."
            ),
            ScheduleStrategy.FINISH_EARLY: (
                "Ưu tiên đưa người bệnh vào khám và hoàn thành các dịch vụ sớm; "
                "thời gian chờ gặp lại bác sĩ có thể dài hơn."
            ),
            ScheduleStrategy.LEAVE_FAST: (
                "Ưu tiên hoàn thành dịch vụ và đưa đủ kết quả đến bác sĩ sớm "
                "để người bệnh được gặp lại bác sĩ."
            ),
        }
        if label in {
            RouteLabel.BALANCED,
            RouteLabel.EARLY_SERVICE,
            RouteLabel.DOCTOR_READY,
        }:
            return strategy_reasons[strategy]

        if label == RouteLabel.LESS_WALK:
            return "Giảm quãng đường di chuyển và số lần đổi tầng trong toàn hành trình."
        if label == RouteLabel.LESS_CROWD:
            return "Ưu tiên các phòng có tổng thời gian hàng chờ dự kiến thấp hơn."

        priority_reasons = {
            RoutePriority.SYSTEM: "Cân bằng thời gian, hàng chờ và quãng đường.",
            RoutePriority.FASTEST: "Ưu tiên hoàn tất toàn bộ hành trình sớm.",
            RoutePriority.LESS_WALK: "Ưu tiên quãng đường ngắn và ít đổi tầng.",
            RoutePriority.LESS_CROWD: "Ưu tiên khu chờ ít đông hơn.",
            RoutePriority.ACCESSIBLE: "Ưu tiên hành trình phù hợp nhu cầu hỗ trợ di chuyển.",
        }
        legacy_strategy_reasons = {
            ScheduleStrategy.BALANCED: (
                " Hệ thống cân bằng hàng chờ, thời gian di chuyển "
                "và thời điểm có kết quả."
            ),
            ScheduleStrategy.FINISH_EARLY: (
                " Hệ thống ưu tiên đưa người bệnh vào phòng dịch vụ và hoàn thành "
                "các dịch vụ sớm; thời gian chờ bác sĩ có thể dài hơn."
            ),
            ScheduleStrategy.LEAVE_FAST: (
                " Hệ thống ưu tiên thời điểm bác sĩ có đủ toàn bộ kết quả "
                "để chẩn đoán sớm nhất."
            ),
        }
        return priority_reasons[priority] + legacy_strategy_reasons[strategy]
