from uuid import uuid4

from app.modules.indoor_navigation.entities import (
    IndoorEdgeType,
    IndoorNavigationGraph,
    IndoorNodeType,
    IndoorRouteEdge,
    IndoorRouteNode,
)
from app.modules.indoor_navigation.repository import IndoorNavigationRepository


class IndoorNavigationNotFoundError(LookupError):
    pass


class IndoorNavigationValidationError(ValueError):
    pass


CONNECTOR_NODE_TYPES = {IndoorNodeType.STAIRS, IndoorNodeType.ELEVATOR}


def _connector_suffix(index: int) -> str:
    if index < 26:
        return chr(65 + index)
    return f"{index // 26}{chr(65 + (index % 26))}"


def _connector_label(node_type: IndoorNodeType) -> str:
    return "Cầu thang" if node_type == IndoorNodeType.STAIRS else "Thang máy"


def _connector_edge_type(node_type: IndoorNodeType) -> IndoorEdgeType:
    return (
        IndoorEdgeType.STAIRS
        if node_type == IndoorNodeType.STAIRS
        else IndoorEdgeType.ELEVATOR
    )


class IndoorNavigationService:
    def __init__(self, repository: IndoorNavigationRepository) -> None:
        self._repository = repository

    def get_graph(self) -> IndoorNavigationGraph:
        return self._repository.get_graph()

    def create_node(
        self,
        *,
        floor_id: str,
        name: str,
        x_percent: float,
        y_percent: float,
        node_type: IndoorNodeType,
        connector_code: str | None,
    ) -> IndoorNavigationGraph:
        graph = self.get_graph()
        if not any(floor.id == floor_id for floor in graph.floors):
            raise IndoorNavigationNotFoundError("Không tìm thấy tầng đã chọn.")
        cleaned_name = name.strip()
        if not cleaned_name:
            raise IndoorNavigationValidationError("Tên node không được để trống.")
        normalized_connector_code = connector_code.strip().upper() if connector_code else None
        if node_type in CONNECTOR_NODE_TYPES:
            normalized_connector_code = normalized_connector_code or self._next_connector_code(
                graph,
                node_type,
                floor_id,
            )
            expected_prefix = f"{node_type.value}_"
            if not normalized_connector_code.startswith(expected_prefix):
                raise IndoorNavigationValidationError(
                    "Mã trục phải đúng loại cầu thang hoặc thang máy đã chọn."
                )
            if any(
                node.floor_id == floor_id
                and node.type == node_type
                and node.connector_code == normalized_connector_code
                for node in graph.nodes
            ):
                raise IndoorNavigationValidationError(
                    "Tầng này đã có một điểm thuộc trục liên tầng đã chọn."
                )
            connector_suffix = normalized_connector_code.removeprefix(expected_prefix)
            cleaned_name = f"{_connector_label(node_type)} {connector_suffix}"
        elif normalized_connector_code is not None:
            raise IndoorNavigationValidationError(
                "Chỉ node cầu thang hoặc thang máy mới được có mã trục liên tầng."
            )
        node = IndoorRouteNode(
            id=f"node-{uuid4().hex}",
            floor_id=floor_id,
            name=cleaned_name,
            x_percent=x_percent,
            y_percent=y_percent,
            type=node_type,
            connector_code=normalized_connector_code,
        )
        self._repository.create_node(node)
        if node.type in CONNECTOR_NODE_TYPES:
            self._connect_adjacent_connector_nodes(node)
        return self.get_graph()

    def update_node(self, node_id: str, changes: dict[str, object]) -> IndoorNavigationGraph:
        graph = self.get_graph()
        node = next((item for item in graph.nodes if item.id == node_id), None)
        if node is None:
            raise IndoorNavigationNotFoundError("Không tìm thấy node cần cập nhật.")
        if node.type in CONNECTOR_NODE_TYPES:
            changes_connector_identity = (
                ("name" in changes and changes["name"] != node.name)
                or ("type" in changes and changes["type"] != node.type)
                or (
                    "connector_code" in changes
                    and changes["connector_code"] != node.connector_code
                )
            )
            if changes_connector_identity:
                raise IndoorNavigationValidationError(
                    "Tên và trục cầu thang/thang máy được hệ thống quản lý tự động."
                )
        elif changes.get("type") in CONNECTOR_NODE_TYPES:
            raise IndoorNavigationValidationError(
                "Hãy tạo node cầu thang hoặc thang máy mới để hệ thống tự cấp trục."
            )
        elif changes.get("connector_code") is not None:
            raise IndoorNavigationValidationError(
                "Node thường không được gán mã trục liên tầng."
            )
        if "name" in changes and isinstance(changes["name"], str):
            cleaned_name = changes["name"].strip()
            if not cleaned_name:
                raise IndoorNavigationValidationError("Tên node không được để trống.")
            changes["name"] = cleaned_name
        if not self._repository.update_node(node_id, changes):
            raise IndoorNavigationNotFoundError("Không tìm thấy node cần cập nhật.")
        return self.get_graph()

    def delete_node(self, node_id: str) -> IndoorNavigationGraph:
        if not self._repository.delete_node(node_id):
            raise IndoorNavigationNotFoundError("Không tìm thấy node cần xóa.")
        return self.get_graph()

    def create_edge(
        self,
        *,
        from_node_id: str,
        to_node_id: str,
        edge_type: IndoorEdgeType,
    ) -> IndoorNavigationGraph:
        if from_node_id == to_node_id:
            raise IndoorNavigationValidationError("Không thể nối một node với chính nó.")
        graph = self.get_graph()
        node_by_id = {node.id: node for node in graph.nodes}
        source = node_by_id.get(from_node_id)
        target = node_by_id.get(to_node_id)
        if source is None or target is None:
            raise IndoorNavigationNotFoundError("Không tìm thấy một trong hai node cần nối.")
        if any(
            {edge.from_node_id, edge.to_node_id} == {from_node_id, to_node_id}
            for edge in graph.edges
        ):
            raise IndoorNavigationValidationError("Hai node này đã được nối.")

        is_inter_floor = source.floor_id != target.floor_id
        if is_inter_floor:
            if edge_type not in {IndoorEdgeType.STAIRS, IndoorEdgeType.ELEVATOR}:
                raise IndoorNavigationValidationError(
                    "Kết nối liên tầng phải là cầu thang hoặc thang máy."
                )
            expected_node_type = (
                IndoorNodeType.STAIRS
                if edge_type == IndoorEdgeType.STAIRS
                else IndoorNodeType.ELEVATOR
            )
            if source.type != expected_node_type or target.type != expected_node_type:
                raise IndoorNavigationValidationError(
                    "Hai node liên tầng phải cùng loại với kết nối."
                )
            if (
                source.connector_code is None
                or source.connector_code != target.connector_code
            ):
                raise IndoorNavigationValidationError(
                    "Chỉ được nối cầu thang hoặc thang máy thuộc cùng một trục A, B, C."
                )
            floor_number_by_id = {
                floor.id: floor.floor_number for floor in graph.floors
            }
            if abs(
                floor_number_by_id[source.floor_id]
                - floor_number_by_id[target.floor_id]
            ) != 1:
                raise IndoorNavigationValidationError(
                    "Kết nối liên tầng chỉ được nối hai tầng liền kề."
                )
        elif edge_type != IndoorEdgeType.CORRIDOR:
            raise IndoorNavigationValidationError(
                "Hai node cùng tầng phải nối bằng hành lang."
            )

        edge = IndoorRouteEdge(
            id=f"edge-{uuid4().hex}",
            floor_id=source.floor_id,
            from_node_id=source.id,
            to_node_id=target.id,
            type=edge_type,
            is_inter_floor=is_inter_floor,
        )
        self._repository.create_edge(edge)
        return self.get_graph()

    def delete_edge(self, edge_id: str) -> IndoorNavigationGraph:
        if not self._repository.delete_edge(edge_id):
            raise IndoorNavigationNotFoundError("Không tìm thấy cạnh nối cần xóa.")
        return self.get_graph()

    def assign_room(self, room_code: str, node_id: str | None) -> IndoorNavigationGraph:
        normalized_room_code = room_code.strip().upper()
        if not normalized_room_code:
            raise IndoorNavigationValidationError("Mã phòng không được để trống.")
        if node_id is not None:
            node = next((item for item in self.get_graph().nodes if item.id == node_id), None)
            if node is None:
                raise IndoorNavigationNotFoundError("Không tìm thấy node được chọn.")
            if node.type != IndoorNodeType.DOOR:
                raise IndoorNavigationValidationError("Chỉ có thể gán phòng vào node cửa phòng.")
        self._repository.assign_room(normalized_room_code, node_id)
        return self.get_graph()

    def reset(self) -> IndoorNavigationGraph:
        self._repository.reset()
        return self.get_graph()

    @staticmethod
    def _next_connector_code(
        graph: IndoorNavigationGraph,
        node_type: IndoorNodeType,
        floor_id: str,
    ) -> str:
        existing_codes = sorted(
            {
                node.connector_code
                for node in graph.nodes
                if node.type == node_type and node.connector_code is not None
            }
        )
        codes_on_floor = {
            node.connector_code
            for node in graph.nodes
            if node.floor_id == floor_id and node.type == node_type
        }
        available_code = next(
            (code for code in existing_codes if code not in codes_on_floor),
            None,
        )
        if available_code is not None:
            return available_code
        index = 0
        while True:
            candidate = f"{node_type.value}_{_connector_suffix(index)}"
            if candidate not in existing_codes:
                return candidate
            index += 1

    def _connect_adjacent_connector_nodes(self, source: IndoorRouteNode) -> None:
        graph = self.get_graph()
        floor_number_by_id = {
            floor.id: floor.floor_number for floor in graph.floors
        }
        source_floor_number = floor_number_by_id[source.floor_id]
        connected_pairs = {
            frozenset((edge.from_node_id, edge.to_node_id)) for edge in graph.edges
        }
        adjacent_nodes = [
            node
            for node in graph.nodes
            if node.id != source.id
            and node.type == source.type
            and node.connector_code == source.connector_code
            and abs(floor_number_by_id[node.floor_id] - source_floor_number) == 1
        ]
        for target in adjacent_nodes:
            if frozenset((source.id, target.id)) in connected_pairs:
                continue
            self.create_edge(
                from_node_id=source.id,
                to_node_id=target.id,
                edge_type=_connector_edge_type(source.type),
            )
