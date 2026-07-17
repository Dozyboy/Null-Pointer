from enum import StrEnum


class RoutePriority(StrEnum):
    SYSTEM = "system"
    FASTEST = "fastest"
    LESS_WALK = "less_walk"
    LESS_CROWD = "less_crowd"
    ACCESSIBLE = "accessible"


class JourneyStepStatus(StrEnum):
    PENDING = "pending"
    HELD = "held"
    NAVIGATING = "navigating"
    ARRIVED = "arrived"
    WAITING = "waiting"
    IN_SERVICE = "in_service"
    RESULT_PENDING = "result_pending"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
