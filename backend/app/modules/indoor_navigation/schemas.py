from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modules.indoor_navigation.entities import IndoorEdgeType, IndoorNodeType


class FromAttributesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IndoorFloorResponse(FromAttributesModel):
    id: str
    floor_number: int
    name: str
    map_image_url: str
    map_width: int
    map_height: int


class IndoorRouteNodeResponse(FromAttributesModel):
    id: str
    floor_id: str
    name: str
    x_percent: float
    y_percent: float
    type: IndoorNodeType
    connector_code: str | None = None


class IndoorRouteEdgeResponse(FromAttributesModel):
    id: str
    floor_id: str
    from_node_id: str
    to_node_id: str
    type: IndoorEdgeType
    is_inter_floor: bool


class IndoorRoomAssignmentResponse(FromAttributesModel):
    room_code: str
    node_id: str


class IndoorNavigationGraphResponse(BaseModel):
    version: int
    updated_at: str
    floors: list[IndoorFloorResponse]
    nodes: list[IndoorRouteNodeResponse]
    edges: list[IndoorRouteEdgeResponse]
    room_assignments: list[IndoorRoomAssignmentResponse]


class CreateIndoorNodeRequest(BaseModel):
    floor_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=160)
    x_percent: float = Field(ge=0, le=100)
    y_percent: float = Field(ge=0, le=100)
    type: IndoorNodeType
    connector_code: str | None = Field(default=None, max_length=100)


class UpdateIndoorNodeRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    x_percent: float | None = Field(default=None, ge=0, le=100)
    y_percent: float | None = Field(default=None, ge=0, le=100)
    type: IndoorNodeType | None = None
    connector_code: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def require_change(self) -> "UpdateIndoorNodeRequest":
        if not self.model_fields_set:
            raise ValueError("Phải gửi ít nhất một thuộc tính cần cập nhật.")
        return self


class CreateIndoorEdgeRequest(BaseModel):
    from_node_id: str = Field(min_length=1, max_length=100)
    to_node_id: str = Field(min_length=1, max_length=100)
    type: IndoorEdgeType = IndoorEdgeType.CORRIDOR


class UpdateRoomAssignmentRequest(BaseModel):
    node_id: str | None = Field(default=None, max_length=100)
