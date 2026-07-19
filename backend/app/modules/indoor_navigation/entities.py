from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class IndoorNodeType(StrEnum):
    CORRIDOR = "CORRIDOR"
    DOOR = "DOOR"
    STAIRS = "STAIRS"
    ELEVATOR = "ELEVATOR"
    ENTRANCE = "ENTRANCE"


class IndoorEdgeType(StrEnum):
    CORRIDOR = "CORRIDOR"
    STAIRS = "STAIRS"
    ELEVATOR = "ELEVATOR"


@dataclass(frozen=True, slots=True)
class IndoorFloor:
    id: str
    floor_number: int
    name: str
    map_image_url: str
    map_width: int
    map_height: int


@dataclass(frozen=True, slots=True)
class IndoorRouteNode:
    id: str
    floor_id: str
    name: str
    x_percent: float
    y_percent: float
    type: IndoorNodeType
    connector_code: str | None = None


@dataclass(frozen=True, slots=True)
class IndoorRouteEdge:
    id: str
    floor_id: str
    from_node_id: str
    to_node_id: str
    type: IndoorEdgeType
    is_inter_floor: bool


@dataclass(frozen=True, slots=True)
class IndoorRoomAssignment:
    room_code: str
    node_id: str


@dataclass(frozen=True, slots=True)
class IndoorNavigationGraph:
    version: int
    updated_at: datetime
    floors: tuple[IndoorFloor, ...]
    nodes: tuple[IndoorRouteNode, ...]
    edges: tuple[IndoorRouteEdge, ...]
    room_assignments: tuple[IndoorRoomAssignment, ...]
