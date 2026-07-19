import type {
  IndoorNavigationPlan,
  IndoorRouteNode,
} from '../model/indoor-navigation.types'

export type MovementTimelineItemKind =
  | 'origin'
  | 'walk'
  | 'transition'
  | 'destination'

export interface MovementTimelineItem {
  id: string
  kind: MovementTimelineItemKind
  title: string
  description: string
  floorNumber: number
  sequenceNumber?: number
  transitionDirection?: 'up' | 'down'
}

interface BuildMovementTimelineInput {
  plan: IndoorNavigationPlan
  originName: string
  originRoomCode?: string
  destinationName: string
  destinationRoomCode?: string
}

interface FloorRouteSegment {
  floorNumber: number
  nodes: IndoorRouteNode[]
}

const FLOOR_SUFFIX_PATTERN = /\s*·\s*Tầng\s+\d+$/u

function cleanNodeName(name: string) {
  return name.replace(FLOOR_SUFFIX_PATTERN, '')
}

function splitRouteByFloor(route: IndoorRouteNode[]) {
  return route.reduce<FloorRouteSegment[]>((segments, node) => {
    const currentSegment = segments.at(-1)
    if (currentSegment?.floorNumber === node.floorNumber) {
      currentSegment.nodes.push(node)
      return segments
    }

    segments.push({ floorNumber: node.floorNumber, nodes: [node] })
    return segments
  }, [])
}

function describeWaypoints(nodes: IndoorRouteNode[]) {
  const waypointNames = nodes
    .slice(1, -1)
    .map((node) => cleanNodeName(node.name))

  return waypointNames.length > 0
    ? `Đi qua ${waypointNames.join(' → ')}.`
    : 'Đi theo tuyến màu xanh trên sơ đồ.'
}

export function buildMovementTimeline({
  plan,
  originName,
  originRoomCode,
  destinationName,
  destinationRoomCode,
}: BuildMovementTimelineInput): MovementTimelineItem[] {
  const segments = splitRouteByFloor(plan.route)
  let walkSequenceNumber = 0
  const items: MovementTimelineItem[] = [
    {
      id: 'movement-origin',
      kind: 'origin',
      title: `Bắt đầu tại ${originName}`,
      description: `Tầng ${plan.originNode.floorNumber}${
        originRoomCode ? ` · Mã phòng ${originRoomCode}` : ''
      }`,
      floorNumber: plan.originNode.floorNumber,
    },
  ]

  segments.forEach((segment, segmentIndex) => {
    const nextSegment = segments[segmentIndex + 1]
    const isDestinationFloor = nextSegment === undefined

    if (segment.nodes.length > 1) {
      walkSequenceNumber += 1
      items.push({
        id: `movement-walk-${segment.floorNumber}-${segmentIndex}`,
        kind: 'walk',
        title: isDestinationFloor
          ? `Đi theo hành lang Tầng ${segment.floorNumber} đến ${destinationName}`
          : `Đi theo hành lang Tầng ${segment.floorNumber} đến Cầu thang A`,
        description: describeWaypoints(segment.nodes),
        floorNumber: segment.floorNumber,
        sequenceNumber: walkSequenceNumber,
      })
    }

    if (nextSegment) {
      const isMovingUp = nextSegment.floorNumber > segment.floorNumber
      items.push({
        id: `movement-transition-${segment.floorNumber}-${nextSegment.floorNumber}`,
        kind: 'transition',
        title: `${isMovingUp ? 'Lên' : 'Xuống'} Tầng ${nextSegment.floorNumber} bằng Cầu thang A`,
        description: 'Đến đúng tầng rồi tiếp tục theo tuyến chỉ dẫn trên màn hình.',
        floorNumber: nextSegment.floorNumber,
        transitionDirection: isMovingUp ? 'up' : 'down',
      })
    }
  })

  items.push({
    id: 'movement-destination',
    kind: 'destination',
    title: `Đến ${destinationName}`,
    description: `Tầng ${plan.destinationNode.floorNumber}${
      destinationRoomCode ? ` · Đối chiếu mã phòng ${destinationRoomCode}` : ''
    }`,
    floorNumber: plan.destinationNode.floorNumber,
  })

  return items
}
