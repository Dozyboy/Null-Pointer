import type {
  IndoorFloor,
  IndoorFloorNumber,
  IndoorNavigationPlan,
  IndoorRouteEdge,
  IndoorRouteNode,
  IndoorRouteNodeType,
} from '../model/indoor-navigation.types'
import { findIndoorRoute } from './indoor-routing'

type NodeSeed = [
  id: string,
  name: string,
  xPercent: number,
  yPercent: number,
  type: IndoorRouteNodeType,
]

interface FloorSeed {
  width: number
  height: number
  startNodeId: string
  nodes: NodeSeed[]
  edges: [fromNodeId: string, toNodeId: string][]
}
const floorId = (floorNumber: IndoorFloorNumber) =>
  `hospital-floor-${floorNumber}`
const nodeId = (baseId: string, floorNumber: IndoorFloorNumber) =>
  `${baseId}-floor-${floorNumber}`

const FLOOR_SEEDS: Record<IndoorFloorNumber, FloorSeed> = {
  1: {
    width: 1528,
    height: 1029,
    startNodeId: 'entrance',
    nodes: [
      ['entrance', 'Lối vào Đường Hùng Vương', 53, 96, 'ENTRANCE'],
      ['south', 'Hành lang phía Nam', 53, 81, 'CORRIDOR'],
      ['south-left', 'Hành lang Nam bên trái', 22, 81, 'CORRIDOR'],
      ['middle', 'Hành lang trung tâm', 58, 58, 'CORRIDOR'],
      ['north', 'Hành lang phía Bắc', 58, 18, 'CORRIDOR'],
      ['north-left', 'Hành lang Bắc bên trái', 15, 18, 'CORRIDOR'],
      ['stairs-a', 'Cầu thang A', 12, 13, 'STAIRS'],
      ['clinic', 'Cửa khu phòng khám', 18, 18, 'DOOR'],
      ['laboratory', 'Cửa khu xét nghiệm máu', 86, 35, 'DOOR'],
      ['urine', 'Cửa phòng nhận mẫu nước tiểu', 25, 27, 'DOOR'],
      ['ct', 'Cửa khu CT Scanner', 8, 88, 'DOOR'],
      ['mri', 'Cửa khu chụp MRI', 35, 88, 'DOOR'],
    ],
    edges: [
      ['entrance', 'south'],
      ['south', 'south-left'],
      ['south', 'middle'],
      ['middle', 'north'],
      ['north', 'north-left'],
      ['north-left', 'stairs-a'],
      ['north-left', 'clinic'],
      ['north', 'laboratory'],
      ['north-left', 'urine'],
      ['south-left', 'ct'],
      ['south-left', 'mri'],
    ],
  },
  2: {
    width: 1536,
    height: 1024,
    startNodeId: 'stairs-a',
    nodes: [
      ['stairs-a', 'Cầu thang A', 11, 17, 'STAIRS'],
      ['north-left', 'Hành lang Bắc bên trái', 22, 18, 'CORRIDOR'],
      ['north', 'Hành lang phía Bắc', 58, 18, 'CORRIDOR'],
      ['north-right', 'Hành lang Bắc bên phải', 80, 18, 'CORRIDOR'],
      ['middle-right', 'Hành lang giữa bên phải', 80, 58, 'CORRIDOR'],
      ['south-right', 'Hành lang Nam bên phải', 76, 80, 'CORRIDOR'],
      ['south', 'Hành lang phía Nam', 55, 80, 'CORRIDOR'],
      ['south-left', 'Hành lang Nam bên trái', 20, 80, 'CORRIDOR'],
      ['xray', 'Cửa khu X-quang P201–P203', 30, 87, 'DOOR'],
      ['abdominal-ultrasound', 'Cửa khu siêu âm P204–P206', 72, 30, 'DOOR'],
      ['soft-ultrasound', 'Cửa khu siêu âm P208–P209', 12, 52, 'DOOR'],
    ],
    edges: [
      ['stairs-a', 'north-left'],
      ['north-left', 'north'],
      ['north', 'north-right'],
      ['north-right', 'middle-right'],
      ['middle-right', 'south-right'],
      ['south-right', 'south'],
      ['south', 'south-left'],
      ['south-left', 'xray'],
      ['north-right', 'abdominal-ultrasound'],
      ['north-left', 'soft-ultrasound'],
    ],
  },
  3: {
    width: 1632,
    height: 964,
    startNodeId: 'stairs-a',
    nodes: [
      ['stairs-a', 'Cầu thang A', 14, 18, 'STAIRS'],
      ['north-left', 'Hành lang Bắc bên trái', 28, 18, 'CORRIDOR'],
      ['north', 'Hành lang phía Bắc', 58, 18, 'CORRIDOR'],
      ['north-right', 'Hành lang Bắc bên phải', 82, 18, 'CORRIDOR'],
      ['middle-right', 'Hành lang giữa bên phải', 82, 61, 'CORRIDOR'],
      ['middle', 'Hành lang trung tâm', 58, 61, 'CORRIDOR'],
      ['middle-left', 'Hành lang giữa bên trái', 30, 61, 'CORRIDOR'],
      ['south', 'Hành lang phía Nam', 55, 82, 'CORRIDOR'],
      ['ecg-eeg', 'Cửa khu điện tim và điện não', 19, 50, 'DOOR'],
      ['echocardiography', 'Cửa khu siêu âm tim', 42, 18, 'DOOR'],
      ['doppler', 'Cửa khu siêu âm Doppler', 38, 61, 'DOOR'],
    ],
    edges: [
      ['stairs-a', 'north-left'],
      ['north-left', 'north'],
      ['north', 'north-right'],
      ['north-right', 'middle-right'],
      ['middle-right', 'middle'],
      ['middle', 'middle-left'],
      ['middle', 'south'],
      ['middle-left', 'ecg-eeg'],
      ['north', 'echocardiography'],
      ['middle-left', 'doppler'],
    ],
  },
  4: {
    width: 1602,
    height: 982,
    startNodeId: 'stairs-a',
    nodes: [
      ['stairs-a', 'Cầu thang A', 11, 18, 'STAIRS'],
      ['p401', 'Cửa phòng nội soi P401', 25, 18, 'DOOR'],
      ['p402', 'Cửa phòng nội soi P402', 31, 18, 'DOOR'],
      ['p403', 'Cửa phòng nội soi P403', 37, 18, 'DOOR'],
      ['p404', 'Cửa phòng nội soi P404', 44, 18, 'DOOR'],
      ['north-center', 'Hành lang Bắc ở giữa', 57, 18, 'CORRIDOR'],
      ['north-right', 'Hành lang Bắc bên phải', 82, 18, 'CORRIDOR'],
      ['central-junction', 'Giao điểm hành lang trung tâm', 57, 56, 'CORRIDOR'],
      ['right-junction', 'Hành lang giữa bên phải', 73, 56, 'CORRIDOR'],
      ['right-south', 'Góc hành lang Đông Nam', 73, 78, 'CORRIDOR'],
      ['south-center', 'Hành lang Nam ở giữa', 57, 78, 'CORRIDOR'],
      ['south-left', 'Hành lang Nam bên trái', 29, 78, 'CORRIDOR'],
      ['left-top', 'Góc hành lang Tây Bắc', 29, 18, 'CORRIDOR'],
      ['left-upper', 'Hành lang trái phía trên', 29, 30, 'CORRIDOR'],
      ['left-lower', 'Hành lang trái phía dưới', 29, 56, 'CORRIDOR'],
      ['p405', 'Cửa phòng đo chức năng hô hấp P405', 50, 56, 'DOOR'],
      ['p406', 'Cửa phòng đo chức năng hô hấp P406', 63, 56, 'DOOR'],
      ['p407', 'Cửa phòng nội soi phế quản P407', 20, 30, 'DOOR'],
      ['p408', 'Cửa phòng nội soi phế quản P408', 20, 56, 'DOOR'],
    ],
    edges: [
      ['stairs-a', 'p401'],
      ['p401', 'p402'],
      ['p402', 'p403'],
      ['p403', 'p404'],
      ['p404', 'north-center'],
      ['north-center', 'north-right'],
      ['north-center', 'central-junction'],
      ['central-junction', 'right-junction'],
      ['right-junction', 'right-south'],
      ['right-south', 'south-center'],
      ['south-center', 'south-left'],
      ['south-left', 'left-lower'],
      ['left-lower', 'left-upper'],
      ['left-upper', 'left-top'],
      ['left-top', 'p401'],
      ['central-junction', 'p405'],
      ['central-junction', 'p406'],
      ['left-upper', 'p407'],
      ['left-lower', 'p408'],
    ],
  },
}

export const INDOOR_FLOORS: IndoorFloor[] = (
  [1, 2, 3, 4] as IndoorFloorNumber[]
).map((floorNumber) => ({
  id: floorId(floorNumber),
  floorNumber,
  name: `Tầng ${floorNumber}`,
  mapImageUrl: `/maps/floor-${floorNumber}.png`,
  mapWidth: FLOOR_SEEDS[floorNumber].width,
  mapHeight: FLOOR_SEEDS[floorNumber].height,
}))

export const INDOOR_ROUTE_NODES: IndoorRouteNode[] = (
  Object.entries(FLOOR_SEEDS) as [string, FloorSeed][]
).flatMap(([floorNumberValue, seed]) => {
  const floorNumber = Number(floorNumberValue) as IndoorFloorNumber
  return seed.nodes.map(([id, name, xPercent, yPercent, type]) => ({
    id: nodeId(id, floorNumber),
    floorId: floorId(floorNumber),
    floorNumber,
    name: `${name} · Tầng ${floorNumber}`,
    xPercent,
    yPercent,
    type,
  }))
})

const intraFloorEdges: IndoorRouteEdge[] = (
  Object.entries(FLOOR_SEEDS) as [string, FloorSeed][]
).flatMap(([floorNumberValue, seed]) => {
  const floorNumber = Number(floorNumberValue) as IndoorFloorNumber
  return seed.edges.map(([fromNodeId, toNodeId], index) => ({
    id: `corridor-${floorNumber}-${index}`,
    floorId: floorId(floorNumber),
    fromNodeId: nodeId(fromNodeId, floorNumber),
    toNodeId: nodeId(toNodeId, floorNumber),
    type: 'CORRIDOR' as const,
    isInterFloor: false,
  }))
})

const interFloorEdges: IndoorRouteEdge[] = ([1, 2, 3] as const).map(
  (floorNumber) => ({
    id: `stairs-${floorNumber}-${floorNumber + 1}`,
    floorId: floorId(floorNumber),
    fromNodeId: nodeId('stairs-a', floorNumber),
    toNodeId: nodeId(
      'stairs-a',
      (floorNumber + 1) as IndoorFloorNumber,
    ),
    type: 'STAIRS',
    isInterFloor: true,
  }),
)

export const INDOOR_ROUTE_EDGES = [...intraFloorEdges, ...interFloorEdges]

const roomNodeGroups: Record<
  IndoorFloorNumber,
  Record<string, string>
> = {
  1: {
    '101': 'laboratory',
    '102': 'laboratory',
    '103': 'laboratory',
    '104': 'urine',
    '105': 'urine',
    '109': 'ct',
    '110': 'ct',
    '111': 'mri',
    '112': 'mri',
    '113': 'laboratory',
  },
  2: {
    '201': 'xray',
    '202': 'xray',
    '203': 'xray',
    '204': 'abdominal-ultrasound',
    '205': 'abdominal-ultrasound',
    '206': 'abdominal-ultrasound',
    '208': 'soft-ultrasound',
    '209': 'soft-ultrasound',
  },
  3: {
    '301': 'ecg-eeg',
    '302': 'ecg-eeg',
    '303': 'ecg-eeg',
    '304': 'ecg-eeg',
    '305': 'echocardiography',
    '306': 'echocardiography',
    '307': 'doppler',
    '308': 'doppler',
  },
  4: {
    '401': 'p401',
    '402': 'p402',
    '403': 'p403',
    '404': 'p404',
    '405': 'p405',
    '406': 'p406',
    '407': 'p407',
    '408': 'p408',
  },
}

export function parseIndoorFloor(
  floorLabel?: string,
  roomCode?: string,
): IndoorFloorNumber | undefined {
  const floorFromLabel = Number(floorLabel?.match(/\d+/)?.[0])
  if (floorFromLabel >= 1 && floorFromLabel <= 4) {
    return floorFromLabel as IndoorFloorNumber
  }

  const roomNumber = roomCode?.match(/\d{3}/)?.[0]
  const floorFromRoom = Number(roomNumber?.[0])
  if (floorFromRoom >= 1 && floorFromRoom <= 4) {
    return floorFromRoom as IndoorFloorNumber
  }
  return undefined
}

function resolveRoomNode(
  roomCode: string | undefined,
  floorNumber: IndoorFloorNumber,
) {
  const roomNumber = roomCode?.match(/\d{3}/)?.[0]
  const mappedNodeId = roomNumber
    ? roomNodeGroups[floorNumber][roomNumber]
    : undefined
  const fallbackNodeId = FLOOR_SEEDS[floorNumber].startNodeId
  return INDOOR_ROUTE_NODES.find(
    (node) => node.id === nodeId(mappedNodeId ?? fallbackNodeId, floorNumber),
  )
}

export function createIndoorNavigationPlan({
  originFloorLabel,
  originRoomCode,
  destinationFloorLabel,
  destinationRoomCode,
}: {
  originFloorLabel?: string
  originRoomCode?: string
  destinationFloorLabel: string
  destinationRoomCode?: string
}): IndoorNavigationPlan | undefined {
  const destinationFloor = parseIndoorFloor(
    destinationFloorLabel,
    destinationRoomCode,
  )
  if (!destinationFloor) return undefined

  const originFloor =
    parseIndoorFloor(originFloorLabel, originRoomCode) ?? destinationFloor
  const originNode = resolveRoomNode(originRoomCode, originFloor)
  const destinationNode = resolveRoomNode(
    destinationRoomCode,
    destinationFloor,
  )
  if (!originNode || !destinationNode) return undefined

  const route = findIndoorRoute(
    INDOOR_ROUTE_NODES,
    INDOOR_ROUTE_EDGES,
    originNode.id,
    destinationNode.id,
  )
  if (route.length === 0) return undefined

  const floorSequence = route.reduce<IndoorFloorNumber[]>((result, node) => {
    if (result.at(-1) !== node.floorNumber) result.push(node.floorNumber)
    return result
  }, [])

  return {
    floors: INDOOR_FLOORS,
    nodes: INDOOR_ROUTE_NODES,
    edges: INDOOR_ROUTE_EDGES,
    route,
    originNode,
    destinationNode,
    floorSequence,
  }
}
