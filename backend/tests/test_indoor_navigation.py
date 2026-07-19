import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.indoor_navigation.entities import IndoorEdgeType, IndoorNodeType
from app.modules.indoor_navigation.repository import SqliteIndoorNavigationRepository
from app.modules.indoor_navigation.service import (
    IndoorNavigationService,
    IndoorNavigationValidationError,
)


def test_indoor_graph_is_available_through_api() -> None:
    response = TestClient(app).get("/api/v1/indoor-navigation/graph")

    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] >= 1
    assert [floor["floor_number"] for floor in payload["floors"]] == [1, 2, 3, 4]
    assert payload["nodes"]
    assert payload["edges"]


def test_node_edge_and_room_assignment_are_persisted(tmp_path) -> None:
    database_path = tmp_path / "indoor-navigation.db"
    repository = SqliteIndoorNavigationRepository(database_path)
    service = IndoorNavigationService(repository)
    initial = service.get_graph()

    after_corridor = service.create_node(
        floor_id="hospital-floor-1",
        name="Điểm hành lang kiểm thử",
        x_percent=40,
        y_percent=45,
        node_type=IndoorNodeType.CORRIDOR,
        connector_code=None,
    )
    corridor = next(node for node in after_corridor.nodes if node.name == "Điểm hành lang kiểm thử")
    source = next(
        node
        for node in after_corridor.nodes
        if node.floor_id == corridor.floor_id and node.type == IndoorNodeType.CORRIDOR
        and node.id != corridor.id
    )
    after_edge = service.create_edge(
        from_node_id=source.id,
        to_node_id=corridor.id,
        edge_type=IndoorEdgeType.CORRIDOR,
    )
    assert any(
        {edge.from_node_id, edge.to_node_id} == {source.id, corridor.id}
        for edge in after_edge.edges
    )

    after_door = service.create_node(
        floor_id="hospital-floor-1",
        name="Cửa phòng kiểm thử",
        x_percent=42,
        y_percent=47,
        node_type=IndoorNodeType.DOOR,
        connector_code=None,
    )
    door = next(node for node in after_door.nodes if node.name == "Cửa phòng kiểm thử")
    assigned = service.assign_room("XN-999", door.id)
    assert any(
        item.room_code == "XN-999" and item.node_id == door.id
        for item in assigned.room_assignments
    )

    service.update_node(door.id, {"x_percent": 60.5, "y_percent": 61.5})
    reloaded = IndoorNavigationService(
        SqliteIndoorNavigationRepository(database_path)
    ).get_graph()
    persisted_door = next(node for node in reloaded.nodes if node.id == door.id)
    assert persisted_door.x_percent == 60.5
    assert persisted_door.y_percent == 61.5
    assert reloaded.version >= initial.version + 5

    with sqlite3.connect(database_path) as connection:
        change_count = connection.execute(
            "SELECT COUNT(*) FROM indoor_map_change_log"
        ).fetchone()[0]
    assert change_count >= 6


def test_deleting_node_removes_edges_and_room_assignment(tmp_path) -> None:
    service = IndoorNavigationService(
        SqliteIndoorNavigationRepository(tmp_path / "cascade.db")
    )
    graph = service.create_node(
        floor_id="hospital-floor-1",
        name="Cửa tạm",
        x_percent=50,
        y_percent=50,
        node_type=IndoorNodeType.DOOR,
        connector_code=None,
    )
    door = next(node for node in graph.nodes if node.name == "Cửa tạm")
    corridor = next(
        node
        for node in graph.nodes
        if node.floor_id == door.floor_id and node.type == IndoorNodeType.CORRIDOR
    )
    service.create_edge(
        from_node_id=corridor.id,
        to_node_id=door.id,
        edge_type=IndoorEdgeType.CORRIDOR,
    )
    service.assign_room("TMP-001", door.id)

    after_delete = service.delete_node(door.id)

    assert all(
        edge.from_node_id != door.id and edge.to_node_id != door.id
        for edge in after_delete.edges
    )
    assert all(item.node_id != door.id for item in after_delete.room_assignments)


def test_connector_shaft_is_named_and_connected_automatically(tmp_path) -> None:
    service = IndoorNavigationService(
        SqliteIndoorNavigationRepository(tmp_path / "connector-shaft.db")
    )

    first_graph = service.create_node(
        floor_id="hospital-floor-1",
        name="Tên tạm sẽ được thay tự động",
        x_percent=70,
        y_percent=70,
        node_type=IndoorNodeType.STAIRS,
        connector_code=None,
    )
    first = next(
        node
        for node in first_graph.nodes
        if node.floor_id == "hospital-floor-1"
        and node.connector_code == "STAIRS_B"
    )
    assert first.name == "Cầu thang B"

    second_graph = service.create_node(
        floor_id="hospital-floor-2",
        name="Tên tạm",
        x_percent=72,
        y_percent=72,
        node_type=IndoorNodeType.STAIRS,
        connector_code=None,
    )
    second = next(
        node
        for node in second_graph.nodes
        if node.floor_id == "hospital-floor-2"
        and node.connector_code == "STAIRS_B"
    )
    assert any(
        edge.is_inter_floor
        and {edge.from_node_id, edge.to_node_id} == {first.id, second.id}
        for edge in second_graph.edges
    )

    with pytest.raises(IndoorNavigationValidationError):
        service.update_node(first.id, {"name": "Không được đổi tên trục"})


def test_inter_floor_edge_rejects_crossed_or_non_adjacent_shaft(tmp_path) -> None:
    service = IndoorNavigationService(
        SqliteIndoorNavigationRepository(tmp_path / "invalid-connector.db")
    )
    graph = service.get_graph()
    stairs_a_floor_1 = next(
        node
        for node in graph.nodes
        if node.floor_id == "hospital-floor-1"
        and node.connector_code == "STAIRS_A"
    )
    stairs_a_floor_2 = next(
        node
        for node in graph.nodes
        if node.floor_id == "hospital-floor-2"
        and node.connector_code == "STAIRS_A"
    )
    stairs_a_floor_3 = next(
        node
        for node in graph.nodes
        if node.floor_id == "hospital-floor-3"
        and node.connector_code == "STAIRS_A"
    )
    graph = service.create_node(
        floor_id="hospital-floor-1",
        name="Tên tạm",
        x_percent=75,
        y_percent=75,
        node_type=IndoorNodeType.STAIRS,
        connector_code=None,
    )
    stairs_b_floor_1 = next(
        node for node in graph.nodes if node.connector_code == "STAIRS_B"
    )

    with pytest.raises(IndoorNavigationValidationError, match="cùng một trục"):
        service.create_edge(
            from_node_id=stairs_b_floor_1.id,
            to_node_id=stairs_a_floor_2.id,
            edge_type=IndoorEdgeType.STAIRS,
        )

    with pytest.raises(IndoorNavigationValidationError, match="liền kề"):
        service.create_edge(
            from_node_id=stairs_a_floor_1.id,
            to_node_id=stairs_a_floor_3.id,
            edge_type=IndoorEdgeType.STAIRS,
        )
