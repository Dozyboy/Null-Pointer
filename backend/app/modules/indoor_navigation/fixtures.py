from dataclasses import dataclass

from app.modules.indoor_navigation.entities import IndoorEdgeType, IndoorNodeType


@dataclass(frozen=True, slots=True)
class FloorSeed:
    id: str
    floor_number: int
    name: str
    map_image_url: str
    map_width: int
    map_height: int


@dataclass(frozen=True, slots=True)
class NodeSeed:
    id: str
    floor_id: str
    name: str
    x_percent: float
    y_percent: float
    type: IndoorNodeType
    connector_code: str | None = None


@dataclass(frozen=True, slots=True)
class EdgeSeed:
    id: str
    floor_id: str
    from_node_id: str
    to_node_id: str
    type: IndoorEdgeType
    is_inter_floor: bool = False


def floor_id(number: int) -> str:
    return f"hospital-floor-{number}"


def node_id(base: str, number: int) -> str:
    return f"{base}-floor-{number}"


FLOOR_SEEDS = (
    FloorSeed(floor_id(1), 1, "Tầng 1", "/maps/floor-1.png", 1528, 1029),
    FloorSeed(floor_id(2), 2, "Tầng 2", "/maps/floor-2.png", 1536, 1024),
    FloorSeed(floor_id(3), 3, "Tầng 3", "/maps/floor-3.png", 1632, 964),
    FloorSeed(floor_id(4), 4, "Tầng 4", "/maps/floor-4.png", 1602, 982),
)


_NODE_DEFINITIONS: dict[int, tuple[tuple[str, str, float, float, IndoorNodeType], ...]] = {
    1: (
        ("entrance", "Lối vào Đường Hùng Vương", 53, 96, IndoorNodeType.ENTRANCE),
        ("south", "Hành lang phía Nam", 53, 81, IndoorNodeType.CORRIDOR),
        ("south-left", "Hành lang Nam bên trái", 22, 81, IndoorNodeType.CORRIDOR),
        ("middle", "Hành lang trung tâm", 58, 58, IndoorNodeType.CORRIDOR),
        ("north", "Hành lang phía Bắc", 58, 18, IndoorNodeType.CORRIDOR),
        ("north-left", "Hành lang Bắc bên trái", 15, 18, IndoorNodeType.CORRIDOR),
        ("stairs-a", "Cầu thang A", 12, 13, IndoorNodeType.STAIRS),
        ("clinic", "Cửa khu phòng khám", 18, 18, IndoorNodeType.DOOR),
        ("laboratory", "Cửa khu xét nghiệm máu", 86, 35, IndoorNodeType.DOOR),
        ("urine", "Cửa phòng nhận mẫu nước tiểu", 25, 27, IndoorNodeType.DOOR),
        ("ct", "Cửa khu CT Scanner", 8, 88, IndoorNodeType.DOOR),
        ("mri", "Cửa khu chụp MRI", 35, 88, IndoorNodeType.DOOR),
    ),
    2: (
        ("stairs-a", "Cầu thang A", 11, 17, IndoorNodeType.STAIRS),
        ("north-left", "Hành lang Bắc bên trái", 22, 18, IndoorNodeType.CORRIDOR),
        ("north", "Hành lang phía Bắc", 58, 18, IndoorNodeType.CORRIDOR),
        ("north-right", "Hành lang Bắc bên phải", 80, 18, IndoorNodeType.CORRIDOR),
        ("middle-right", "Hành lang giữa bên phải", 80, 58, IndoorNodeType.CORRIDOR),
        ("south-right", "Hành lang Nam bên phải", 76, 80, IndoorNodeType.CORRIDOR),
        ("south", "Hành lang phía Nam", 55, 80, IndoorNodeType.CORRIDOR),
        ("south-left", "Hành lang Nam bên trái", 20, 80, IndoorNodeType.CORRIDOR),
        ("xray", "Cửa khu X-quang P201–P203", 30, 87, IndoorNodeType.DOOR),
        ("abdominal-ultrasound", "Cửa khu siêu âm P204–P206", 72, 30, IndoorNodeType.DOOR),
        ("soft-ultrasound", "Cửa khu siêu âm P208–P209", 12, 52, IndoorNodeType.DOOR),
    ),
    3: (
        ("stairs-a", "Cầu thang A", 14, 18, IndoorNodeType.STAIRS),
        ("north-left", "Hành lang Bắc bên trái", 28, 18, IndoorNodeType.CORRIDOR),
        ("north", "Hành lang phía Bắc", 58, 18, IndoorNodeType.CORRIDOR),
        ("north-right", "Hành lang Bắc bên phải", 82, 18, IndoorNodeType.CORRIDOR),
        ("middle-right", "Hành lang giữa bên phải", 82, 61, IndoorNodeType.CORRIDOR),
        ("middle", "Hành lang trung tâm", 58, 61, IndoorNodeType.CORRIDOR),
        ("middle-left", "Hành lang giữa bên trái", 30, 61, IndoorNodeType.CORRIDOR),
        ("south", "Hành lang phía Nam", 55, 82, IndoorNodeType.CORRIDOR),
        ("ecg-eeg", "Cửa khu điện tim và điện não", 19, 50, IndoorNodeType.DOOR),
        ("echocardiography", "Cửa khu siêu âm tim", 42, 18, IndoorNodeType.DOOR),
        ("doppler", "Cửa khu siêu âm Doppler", 38, 61, IndoorNodeType.DOOR),
    ),
    4: (
        ("stairs-a", "Cầu thang A", 11, 18, IndoorNodeType.STAIRS),
        ("p401", "Cửa phòng nội soi P401", 25, 18, IndoorNodeType.DOOR),
        ("p402", "Cửa phòng nội soi P402", 31, 18, IndoorNodeType.DOOR),
        ("p403", "Cửa phòng nội soi P403", 37, 18, IndoorNodeType.DOOR),
        ("p404", "Cửa phòng nội soi P404", 44, 18, IndoorNodeType.DOOR),
        ("north-center", "Hành lang Bắc ở giữa", 57, 18, IndoorNodeType.CORRIDOR),
        ("north-right", "Hành lang Bắc bên phải", 82, 18, IndoorNodeType.CORRIDOR),
        ("central-junction", "Giao điểm hành lang trung tâm", 57, 56, IndoorNodeType.CORRIDOR),
        ("right-junction", "Hành lang giữa bên phải", 73, 56, IndoorNodeType.CORRIDOR),
        ("right-south", "Góc hành lang Đông Nam", 73, 78, IndoorNodeType.CORRIDOR),
        ("south-center", "Hành lang Nam ở giữa", 57, 78, IndoorNodeType.CORRIDOR),
        ("south-left", "Hành lang Nam bên trái", 29, 78, IndoorNodeType.CORRIDOR),
        ("left-top", "Góc hành lang Tây Bắc", 29, 18, IndoorNodeType.CORRIDOR),
        ("left-upper", "Hành lang trái phía trên", 29, 30, IndoorNodeType.CORRIDOR),
        ("left-lower", "Hành lang trái phía dưới", 29, 56, IndoorNodeType.CORRIDOR),
        ("p405", "Cửa phòng đo chức năng hô hấp P405", 50, 56, IndoorNodeType.DOOR),
        ("p406", "Cửa phòng đo chức năng hô hấp P406", 63, 56, IndoorNodeType.DOOR),
        ("p407", "Cửa phòng nội soi phế quản P407", 20, 30, IndoorNodeType.DOOR),
        ("p408", "Cửa phòng nội soi phế quản P408", 20, 56, IndoorNodeType.DOOR),
    ),
}


NODE_SEEDS = tuple(
    NodeSeed(
        id=node_id(base, number),
        floor_id=floor_id(number),
        name=f"{name} · Tầng {number}",
        x_percent=x_percent,
        y_percent=y_percent,
        type=node_type,
        connector_code="STAIRS_A" if base == "stairs-a" else None,
    )
    for number, nodes in _NODE_DEFINITIONS.items()
    for base, name, x_percent, y_percent, node_type in nodes
)


_FLOOR_EDGES: dict[int, tuple[tuple[str, str], ...]] = {
    1: (
        ("entrance", "south"), ("south", "south-left"), ("south", "middle"),
        ("middle", "north"), ("north", "north-left"), ("north-left", "stairs-a"),
        ("north-left", "clinic"), ("north", "laboratory"), ("north-left", "urine"),
        ("south-left", "ct"), ("south-left", "mri"),
    ),
    2: (
        ("stairs-a", "north-left"), ("north-left", "north"), ("north", "north-right"),
        ("north-right", "middle-right"), ("middle-right", "south-right"),
        ("south-right", "south"), ("south", "south-left"), ("south-left", "xray"),
        ("north-right", "abdominal-ultrasound"), ("north-left", "soft-ultrasound"),
    ),
    3: (
        ("stairs-a", "north-left"), ("north-left", "north"), ("north", "north-right"),
        ("north-right", "middle-right"), ("middle-right", "middle"),
        ("middle", "middle-left"), ("middle", "south"), ("middle-left", "ecg-eeg"),
        ("north", "echocardiography"), ("middle-left", "doppler"),
    ),
    4: (
        ("stairs-a", "p401"), ("p401", "p402"), ("p402", "p403"),
        ("p403", "p404"), ("p404", "north-center"), ("north-center", "north-right"),
        ("north-center", "central-junction"), ("central-junction", "right-junction"),
        ("right-junction", "right-south"), ("right-south", "south-center"),
        ("south-center", "south-left"), ("south-left", "left-lower"),
        ("left-lower", "left-upper"), ("left-upper", "left-top"), ("left-top", "p401"),
        ("central-junction", "p405"), ("central-junction", "p406"),
        ("left-upper", "p407"), ("left-lower", "p408"),
    ),
}


EDGE_SEEDS = tuple(
    EdgeSeed(
        id=f"corridor-{number}-{index}",
        floor_id=floor_id(number),
        from_node_id=node_id(source, number),
        to_node_id=node_id(target, number),
        type=IndoorEdgeType.CORRIDOR,
    )
    for number, edges in _FLOOR_EDGES.items()
    for index, (source, target) in enumerate(edges)
) + tuple(
    EdgeSeed(
        id=f"stairs-{number}-{number + 1}",
        floor_id=floor_id(number),
        from_node_id=node_id("stairs-a", number),
        to_node_id=node_id("stairs-a", number + 1),
        type=IndoorEdgeType.STAIRS,
        is_inter_floor=True,
    )
    for number in (1, 2, 3)
)


ROOM_ASSIGNMENT_SEEDS = {
    "101": node_id("laboratory", 1), "102": node_id("laboratory", 1),
    "103": node_id("laboratory", 1), "104": node_id("urine", 1),
    "105": node_id("urine", 1), "109": node_id("ct", 1),
    "110": node_id("ct", 1), "111": node_id("mri", 1),
    "112": node_id("mri", 1), "113": node_id("laboratory", 1),
    "201": node_id("xray", 2), "202": node_id("xray", 2),
    "203": node_id("xray", 2), "204": node_id("abdominal-ultrasound", 2),
    "205": node_id("abdominal-ultrasound", 2), "206": node_id("abdominal-ultrasound", 2),
    "208": node_id("soft-ultrasound", 2), "209": node_id("soft-ultrasound", 2),
    "301": node_id("ecg-eeg", 3), "302": node_id("ecg-eeg", 3),
    "303": node_id("ecg-eeg", 3), "304": node_id("ecg-eeg", 3),
    "305": node_id("echocardiography", 3), "306": node_id("echocardiography", 3),
    "307": node_id("doppler", 3), "308": node_id("doppler", 3),
    "401": node_id("p401", 4), "402": node_id("p402", 4),
    "403": node_id("p403", 4), "404": node_id("p404", 4),
    "405": node_id("p405", 4), "406": node_id("p406", 4),
    "407": node_id("p407", 4), "408": node_id("p408", 4),
}
