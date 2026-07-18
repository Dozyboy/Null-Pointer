from fastapi import APIRouter, HTTPException, status

from app.modules.clinical_orders.exceptions import ClinicalServiceNotFoundError
from app.modules.patients.service import PatientNotFoundError
from app.modules.routing.exceptions import NoFeasibleRouteError
from app.modules.simulation.clinical_order_runtime import (
    clinical_order_simulation_service as service,
)
from app.modules.simulation.clinical_order_schemas import (
    ClinicalOrderDispatchResponse,
    DispatchClinicalOrderRequest,
    RecalculateClinicalOrderRouteRequest,
)
from app.modules.simulation.clinical_order_service import ClinicalOrderNotFoundError

router = APIRouter(prefix="/simulation", tags=["demo-clinical-order-dispatch"])


@router.post(
    "/clinical-orders",
    response_model=ClinicalOrderDispatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Gửi chỉ định giả lập và tạo lộ trình cho bệnh nhân",
)
def dispatch_clinical_order(
    request: DispatchClinicalOrderRequest,
) -> ClinicalOrderDispatchResponse:
    try:
        return service.dispatch(request)
    except ClinicalServiceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy dịch vụ {error.args[0]} trong danh mục.",
        ) from error
    except PatientNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bệnh nhân đã chọn trong cơ sở dữ liệu.",
        ) from error
    except NoFeasibleRouteError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.get(
    "/patients/{patient_code}/clinical-orders/latest",
    response_model=ClinicalOrderDispatchResponse,
    summary="Lấy chỉ định mới nhất bệnh nhân đã nhận",
)
def get_latest_patient_order(patient_code: str) -> ClinicalOrderDispatchResponse:
    try:
        return service.get_latest_for_patient(patient_code)
    except ClinicalOrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bệnh nhân chưa nhận chỉ định giả lập nào.",
        ) from error


@router.post(
    "/patients/{patient_code}/clinical-orders/latest/route-proposals",
    response_model=ClinicalOrderDispatchResponse,
    summary="Tính lại phần lịch trình còn lại từ trạng thái phòng hiện tại",
)
def recalculate_latest_patient_route(
    patient_code: str,
    request: RecalculateClinicalOrderRouteRequest,
) -> ClinicalOrderDispatchResponse:
    try:
        return service.recalculate_route(patient_code, request)
    except ClinicalOrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bệnh nhân chưa nhận chỉ định giả lập nào.",
        ) from error
    except ClinicalServiceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy dịch vụ {error.args[0]} trong danh mục.",
        ) from error
    except NoFeasibleRouteError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
