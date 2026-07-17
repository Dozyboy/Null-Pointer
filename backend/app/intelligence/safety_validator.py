from app.modules.routing.schemas import RouteOptionResponse


class UnsafeRouteError(ValueError):
    """Phương án thiếu dịch vụ hoặc vi phạm ràng buộc bắt buộc."""


def validate_required_services(
    option: RouteOptionResponse,
    required_service_codes: set[str],
) -> None:
    actual_codes = {step.service_code for step in option.steps}
    missing_codes = required_service_codes - actual_codes
    if missing_codes:
        raise UnsafeRouteError(
            f"Phương án thiếu dịch vụ bắt buộc: {', '.join(sorted(missing_codes))}"
        )
