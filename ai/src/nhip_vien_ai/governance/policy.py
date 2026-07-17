from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import yaml


@dataclass(frozen=True)
class GovernancePolicy:
    name: str
    level: str
    allowed_operations: frozenset[str]
    blocked_operations: frozenset[str]
    require_human_approval: frozenset[str]
    max_candidates_per_request: int
    max_requests_per_minute: int
    fail_closed: bool
    audit_enabled: bool

    def ensure_allowed(self, operation: str) -> None:
        if operation in self.blocked_operations:
            raise PermissionError(f"Thao tác bị chính sách chặn: {operation}")
        if operation not in self.allowed_operations:
            raise PermissionError(f"Thao tác không nằm trong danh sách cho phép: {operation}")


def load_policy(path: str | Path) -> GovernancePolicy:
    with Path(path).open(encoding="utf-8") as policy_file:
        data = yaml.safe_load(policy_file)
    return GovernancePolicy(
        name=data["name"],
        level=data["level"],
        allowed_operations=frozenset(data.get("allowed_operations", [])),
        blocked_operations=frozenset(data.get("blocked_operations", [])),
        require_human_approval=frozenset(data.get("require_human_approval", [])),
        max_candidates_per_request=int(data["max_candidates_per_request"]),
        max_requests_per_minute=int(data["max_requests_per_minute"]),
        fail_closed=bool(data["fail_closed"]),
        audit_enabled=bool(data["audit_enabled"]),
    )


@dataclass(frozen=True)
class AuditRecord:
    request_id: str
    operation: str
    action: str
    policy_name: str
    model_version: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class InMemoryAuditTrail:
    """Bản phát triển; môi trường thật phải dùng kho chỉ được bổ sung."""

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self._records.append(record)

    def records(self) -> tuple[AuditRecord, ...]:
        return tuple(self._records)
