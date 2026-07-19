import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from threading import RLock
from typing import Protocol

from app.modules.indoor_navigation.entities import (
    IndoorEdgeType,
    IndoorFloor,
    IndoorNavigationGraph,
    IndoorNodeType,
    IndoorRoomAssignment,
    IndoorRouteEdge,
    IndoorRouteNode,
)
from app.modules.indoor_navigation.fixtures import (
    EDGE_SEEDS,
    FLOOR_SEEDS,
    NODE_SEEDS,
    ROOM_ASSIGNMENT_SEEDS,
)


class IndoorNavigationConflictError(ValueError):
    pass


class IndoorNavigationRepository(Protocol):
    def get_graph(self) -> IndoorNavigationGraph: ...

    def create_node(self, node: IndoorRouteNode) -> None: ...

    def update_node(self, node_id: str, changes: dict[str, object]) -> bool: ...

    def delete_node(self, node_id: str) -> bool: ...

    def create_edge(self, edge: IndoorRouteEdge) -> None: ...

    def delete_edge(self, edge_id: str) -> bool: ...

    def assign_room(self, room_code: str, node_id: str | None) -> None: ...

    def reset(self) -> None: ...


def sqlite_path_from_url(database_url: str) -> Path:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Cấu hình sơ đồ hiện chỉ hỗ trợ DATABASE_URL sử dụng SQLite.")
    return Path(database_url.removeprefix(prefix)).resolve()


class SqliteIndoorNavigationRepository:
    """Lưu mạng đường đi bền vững trong cùng cơ sở dữ liệu của backend."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._lock = RLock()
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._lock, self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS indoor_map_metadata (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    version INTEGER NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS indoor_floors (
                    id TEXT PRIMARY KEY,
                    floor_number INTEGER NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    map_image_url TEXT NOT NULL,
                    map_width INTEGER NOT NULL,
                    map_height INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS indoor_route_nodes (
                    id TEXT PRIMARY KEY,
                    floor_id TEXT NOT NULL REFERENCES indoor_floors(id) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    x_percent REAL NOT NULL CHECK (x_percent BETWEEN 0 AND 100),
                    y_percent REAL NOT NULL CHECK (y_percent BETWEEN 0 AND 100),
                    type TEXT NOT NULL,
                    connector_code TEXT
                );

                CREATE TABLE IF NOT EXISTS indoor_route_edges (
                    id TEXT PRIMARY KEY,
                    floor_id TEXT NOT NULL REFERENCES indoor_floors(id) ON DELETE CASCADE,
                    from_node_id TEXT NOT NULL REFERENCES indoor_route_nodes(id) ON DELETE CASCADE,
                    to_node_id TEXT NOT NULL REFERENCES indoor_route_nodes(id) ON DELETE CASCADE,
                    type TEXT NOT NULL,
                    is_inter_floor INTEGER NOT NULL DEFAULT 0,
                    CHECK (from_node_id <> to_node_id)
                );

                CREATE TABLE IF NOT EXISTS indoor_room_node_assignments (
                    room_code TEXT PRIMARY KEY,
                    node_id TEXT NOT NULL REFERENCES indoor_route_nodes(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS indoor_map_change_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    changed_at TEXT NOT NULL
                );
                """
            )
            existing = connection.execute(
                "SELECT COUNT(*) AS total FROM indoor_floors"
            ).fetchone()
            if existing is not None and existing["total"] == 0:
                self._seed(connection)

    @staticmethod
    def _seed(connection: sqlite3.Connection) -> None:
        now = datetime.now(UTC).replace(microsecond=0).isoformat()
        connection.execute(
            "INSERT OR REPLACE INTO indoor_map_metadata (id, version, updated_at) VALUES (1, 1, ?)",
            (now,),
        )
        connection.executemany(
            """
            INSERT INTO indoor_floors (
                id, floor_number, name, map_image_url, map_width, map_height
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    floor.id,
                    floor.floor_number,
                    floor.name,
                    floor.map_image_url,
                    floor.map_width,
                    floor.map_height,
                )
                for floor in FLOOR_SEEDS
            ],
        )
        connection.executemany(
            """
            INSERT INTO indoor_route_nodes (
                id, floor_id, name, x_percent, y_percent, type, connector_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    node.id,
                    node.floor_id,
                    node.name,
                    node.x_percent,
                    node.y_percent,
                    node.type.value,
                    node.connector_code,
                )
                for node in NODE_SEEDS
            ],
        )
        connection.executemany(
            """
            INSERT INTO indoor_route_edges (
                id, floor_id, from_node_id, to_node_id, type, is_inter_floor
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    edge.id,
                    edge.floor_id,
                    edge.from_node_id,
                    edge.to_node_id,
                    edge.type.value,
                    int(edge.is_inter_floor),
                )
                for edge in EDGE_SEEDS
            ],
        )
        connection.executemany(
            "INSERT INTO indoor_room_node_assignments (room_code, node_id) VALUES (?, ?)",
            list(ROOM_ASSIGNMENT_SEEDS.items()),
        )
        connection.execute(
            """
            INSERT INTO indoor_map_change_log (
                version, action, entity_type, entity_id, payload_json, actor, changed_at
            ) VALUES (1, 'seed', 'graph', 'default', '{}', 'system', ?)
            """,
            (now,),
        )

    def get_graph(self) -> IndoorNavigationGraph:
        with self._lock, self._connect() as connection:
            metadata = connection.execute(
                "SELECT version, updated_at FROM indoor_map_metadata WHERE id = 1"
            ).fetchone()
            floor_rows = connection.execute(
                "SELECT * FROM indoor_floors ORDER BY floor_number"
            ).fetchall()
            node_rows = connection.execute(
                "SELECT * FROM indoor_route_nodes ORDER BY floor_id, name, id"
            ).fetchall()
            edge_rows = connection.execute(
                "SELECT * FROM indoor_route_edges ORDER BY floor_id, id"
            ).fetchall()
            assignment_rows = connection.execute(
                "SELECT * FROM indoor_room_node_assignments ORDER BY room_code"
            ).fetchall()

        if metadata is None:
            raise RuntimeError("Thiếu metadata của sơ đồ chỉ đường.")
        return IndoorNavigationGraph(
            version=metadata["version"],
            updated_at=datetime.fromisoformat(metadata["updated_at"]),
            floors=tuple(
                IndoorFloor(
                    id=row["id"],
                    floor_number=row["floor_number"],
                    name=row["name"],
                    map_image_url=row["map_image_url"],
                    map_width=row["map_width"],
                    map_height=row["map_height"],
                )
                for row in floor_rows
            ),
            nodes=tuple(self._node_from_row(row) for row in node_rows),
            edges=tuple(
                IndoorRouteEdge(
                    id=row["id"],
                    floor_id=row["floor_id"],
                    from_node_id=row["from_node_id"],
                    to_node_id=row["to_node_id"],
                    type=IndoorEdgeType(row["type"]),
                    is_inter_floor=bool(row["is_inter_floor"]),
                )
                for row in edge_rows
            ),
            room_assignments=tuple(
                IndoorRoomAssignment(
                    room_code=row["room_code"],
                    node_id=row["node_id"],
                )
                for row in assignment_rows
            ),
        )

    def create_node(self, node: IndoorRouteNode) -> None:
        try:
            with self._lock, self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO indoor_route_nodes (
                        id, floor_id, name, x_percent, y_percent, type, connector_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        node.id,
                        node.floor_id,
                        node.name,
                        node.x_percent,
                        node.y_percent,
                        node.type.value,
                        node.connector_code,
                    ),
                )
                self._record_change(connection, "create", "node", node.id, node)
        except sqlite3.IntegrityError as error:
            raise IndoorNavigationConflictError(
                "Không thể tạo node với dữ liệu đã chọn."
            ) from error

    def update_node(self, node_id: str, changes: dict[str, object]) -> bool:
        columns = {
            "name": "name",
            "x_percent": "x_percent",
            "y_percent": "y_percent",
            "type": "type",
            "connector_code": "connector_code",
        }
        filtered = {key: value for key, value in changes.items() if key in columns}
        if not filtered:
            return False
        assignments = ", ".join(f"{columns[key]} = ?" for key in filtered)
        values = [
            value.value if isinstance(value, IndoorNodeType) else value
            for value in filtered.values()
        ]
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                f"UPDATE indoor_route_nodes SET {assignments} WHERE id = ?",
                (*values, node_id),
            )
            if cursor.rowcount:
                self._record_change(connection, "update", "node", node_id, filtered)
            return cursor.rowcount == 1

    def delete_node(self, node_id: str) -> bool:
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM indoor_route_nodes WHERE id = ?", (node_id,)
            )
            if cursor.rowcount:
                self._record_change(connection, "delete", "node", node_id, {})
            return cursor.rowcount == 1

    def create_edge(self, edge: IndoorRouteEdge) -> None:
        try:
            with self._lock, self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO indoor_route_edges (
                        id, floor_id, from_node_id, to_node_id, type, is_inter_floor
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        edge.id,
                        edge.floor_id,
                        edge.from_node_id,
                        edge.to_node_id,
                        edge.type.value,
                        int(edge.is_inter_floor),
                    ),
                )
                self._record_change(connection, "create", "edge", edge.id, edge)
        except sqlite3.IntegrityError as error:
            raise IndoorNavigationConflictError("Không thể tạo cạnh nối đã chọn.") from error

    def delete_edge(self, edge_id: str) -> bool:
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM indoor_route_edges WHERE id = ?", (edge_id,)
            )
            if cursor.rowcount:
                self._record_change(connection, "delete", "edge", edge_id, {})
            return cursor.rowcount == 1

    def assign_room(self, room_code: str, node_id: str | None) -> None:
        with self._lock, self._connect() as connection:
            if node_id is None:
                connection.execute(
                    "DELETE FROM indoor_room_node_assignments WHERE room_code = ?",
                    (room_code,),
                )
                action = "unassign"
            else:
                connection.execute(
                    """
                    INSERT INTO indoor_room_node_assignments (room_code, node_id)
                    VALUES (?, ?)
                    ON CONFLICT(room_code) DO UPDATE SET node_id = excluded.node_id
                    """,
                    (room_code, node_id),
                )
                action = "assign"
            self._record_change(
                connection,
                action,
                "room_assignment",
                room_code,
                {"node_id": node_id},
            )

    def reset(self) -> None:
        with self._lock, self._connect() as connection:
            connection.execute("DELETE FROM indoor_room_node_assignments")
            connection.execute("DELETE FROM indoor_route_edges")
            connection.execute("DELETE FROM indoor_route_nodes")
            connection.execute("DELETE FROM indoor_floors")
            connection.execute("DELETE FROM indoor_map_change_log")
            connection.execute("DELETE FROM indoor_map_metadata")
            self._seed(connection)

    @staticmethod
    def _node_from_row(row: sqlite3.Row) -> IndoorRouteNode:
        return IndoorRouteNode(
            id=row["id"],
            floor_id=row["floor_id"],
            name=row["name"],
            x_percent=row["x_percent"],
            y_percent=row["y_percent"],
            type=IndoorNodeType(row["type"]),
            connector_code=row["connector_code"],
        )

    @staticmethod
    def _json_payload(payload: object) -> str:
        if hasattr(payload, "__dataclass_fields__"):
            values = {
                field: getattr(payload, field)
                for field in payload.__dataclass_fields__
            }
        elif isinstance(payload, dict):
            values = payload
        else:
            values = {"value": payload}
        return json.dumps(
            values,
            ensure_ascii=False,
            default=lambda value: value.value if hasattr(value, "value") else str(value),
        )

    def _record_change(
        self,
        connection: sqlite3.Connection,
        action: str,
        entity_type: str,
        entity_id: str,
        payload: object,
    ) -> None:
        now = datetime.now(UTC).replace(microsecond=0).isoformat()
        row = connection.execute(
            "SELECT version FROM indoor_map_metadata WHERE id = 1"
        ).fetchone()
        version = (row["version"] if row else 0) + 1
        connection.execute(
            """
            INSERT INTO indoor_map_metadata (id, version, updated_at)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                version = excluded.version,
                updated_at = excluded.updated_at
            """,
            (version, now),
        )
        connection.execute(
            """
            INSERT INTO indoor_map_change_log (
                version, action, entity_type, entity_id, payload_json, actor, changed_at
            ) VALUES (?, ?, ?, ?, ?, 'simulator', ?)
            """,
            (
                version,
                action,
                entity_type,
                entity_id,
                self._json_payload(payload),
                now,
            ),
        )
