from fastapi import APIRouter, HTTPException, status

from app.modules.indoor_navigation.entities import IndoorNavigationGraph
from app.modules.indoor_navigation.repository import IndoorNavigationConflictError
from app.modules.indoor_navigation.runtime import indoor_navigation_service as service
from app.modules.indoor_navigation.schemas import (
    CreateIndoorEdgeRequest,
    CreateIndoorNodeRequest,
    IndoorNavigationGraphResponse,
    UpdateIndoorNodeRequest,
    UpdateRoomAssignmentRequest,
)
from app.modules.indoor_navigation.service import (
    IndoorNavigationNotFoundError,
    IndoorNavigationValidationError,
)

public_router = APIRouter(prefix="/indoor-navigation", tags=["indoor-navigation"])
simulation_router = APIRouter(
    prefix="/simulation/indoor-navigation",
    tags=["demo-indoor-navigation"],
)


def _response(graph: IndoorNavigationGraph) -> IndoorNavigationGraphResponse:
    return IndoorNavigationGraphResponse(
        version=graph.version,
        updated_at=graph.updated_at.isoformat(),
        floors=list(graph.floors),
        nodes=list(graph.nodes),
        edges=list(graph.edges),
        room_assignments=list(graph.room_assignments),
    )


def _raise_http_error(error: Exception) -> None:
    if isinstance(error, IndoorNavigationNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    if isinstance(error, IndoorNavigationConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(error),
    ) from error


@public_router.get(
    "/graph",
    response_model=IndoorNavigationGraphResponse,
    summary="Lấy mạng đường đi hiện hành của bệnh viện",
)
def get_indoor_navigation_graph() -> IndoorNavigationGraphResponse:
    return _response(service.get_graph())


@simulation_router.post(
    "/nodes",
    response_model=IndoorNavigationGraphResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm node vào sơ đồ",
)
def create_indoor_node(request: CreateIndoorNodeRequest) -> IndoorNavigationGraphResponse:
    try:
        return _response(
            service.create_node(
                floor_id=request.floor_id,
                name=request.name,
                x_percent=request.x_percent,
                y_percent=request.y_percent,
                node_type=request.type,
                connector_code=request.connector_code,
            )
        )
    except (
        IndoorNavigationNotFoundError,
        IndoorNavigationValidationError,
        IndoorNavigationConflictError,
    ) as error:
        _raise_http_error(error)


@simulation_router.patch(
    "/nodes/{node_id}",
    response_model=IndoorNavigationGraphResponse,
    summary="Cập nhật node trên sơ đồ",
)
def update_indoor_node(
    node_id: str,
    request: UpdateIndoorNodeRequest,
) -> IndoorNavigationGraphResponse:
    try:
        changes = request.model_dump(exclude_unset=True)
        return _response(service.update_node(node_id, changes))
    except (IndoorNavigationNotFoundError, IndoorNavigationValidationError) as error:
        _raise_http_error(error)


@simulation_router.delete(
    "/nodes/{node_id}",
    response_model=IndoorNavigationGraphResponse,
    summary="Xóa node và các cạnh liên quan",
)
def delete_indoor_node(node_id: str) -> IndoorNavigationGraphResponse:
    try:
        return _response(service.delete_node(node_id))
    except IndoorNavigationNotFoundError as error:
        _raise_http_error(error)


@simulation_router.post(
    "/edges",
    response_model=IndoorNavigationGraphResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Nối hai node",
)
def create_indoor_edge(request: CreateIndoorEdgeRequest) -> IndoorNavigationGraphResponse:
    try:
        return _response(
            service.create_edge(
                from_node_id=request.from_node_id,
                to_node_id=request.to_node_id,
                edge_type=request.type,
            )
        )
    except (
        IndoorNavigationNotFoundError,
        IndoorNavigationValidationError,
        IndoorNavigationConflictError,
    ) as error:
        _raise_http_error(error)


@simulation_router.delete(
    "/edges/{edge_id}",
    response_model=IndoorNavigationGraphResponse,
    summary="Xóa cạnh nối",
)
def delete_indoor_edge(edge_id: str) -> IndoorNavigationGraphResponse:
    try:
        return _response(service.delete_edge(edge_id))
    except IndoorNavigationNotFoundError as error:
        _raise_http_error(error)


@simulation_router.put(
    "/room-assignments/{room_code}",
    response_model=IndoorNavigationGraphResponse,
    summary="Gán hoặc bỏ gán phòng vào node cửa",
)
def update_room_assignment(
    room_code: str,
    request: UpdateRoomAssignmentRequest,
) -> IndoorNavigationGraphResponse:
    try:
        return _response(service.assign_room(room_code, request.node_id))
    except (IndoorNavigationNotFoundError, IndoorNavigationValidationError) as error:
        _raise_http_error(error)


@simulation_router.post(
    "/reset",
    response_model=IndoorNavigationGraphResponse,
    summary="Khôi phục sơ đồ mặc định",
)
def reset_indoor_navigation_graph() -> IndoorNavigationGraphResponse:
    return _response(service.reset())
