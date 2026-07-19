import type { IndoorNavigationGraph } from '../../../entities/indoor-navigation/model/indoor-navigation.schemas'
import type {
  IndoorFloor,
  IndoorFloorNumber,
  IndoorNavigationPlan,
  IndoorRouteEdge,
  IndoorRouteNode,
} from '../model/indoor-navigation.types'
import { findIndoorRoute } from './indoor-routing'

interface CreateRuntimePlanInput {
  graph: IndoorNavigationGraph
  originFloorLabel?: string
  originRoomCode?: string
  destinationFloorLabel: string
  destinationRoomCode?: string
}

const VALID_FLOOR_NUMBERS = new Set([1, 2, 3, 4])

function parseFloorNumber(
  floorLabel?: string,
  roomCode?: string,
): IndoorFloorNumber | undefined {
  const floorFromLabel = Number(floorLabel?.match(/\d+/)?.[0])
  if (VALID_FLOOR_NUMBERS.has(floorFromLabel)) {
    return floorFromLabel as IndoorFloorNumber
  }
  const roomNumber = roomCode?.match(/\d{3}/)?.[0]
  const floorFromRoom = Number(roomNumber?.[0])
  return VALID_FLOOR_NUMBERS.has(floorFromRoom)
    ? (floorFromRoom as IndoorFloorNumber)
    : undefined
}

function normalizeRoomCode(value?: string) {
  return value?.toUpperCase().trim()
}

function roomNumber(value?: string) {
  return value?.match(/\d{3}/)?.[0]
}

function findAssignedNode(
  graph: IndoorNavigationGraph,
  nodes: IndoorRouteNode[],
  requestedRoomCode?: string,
) {
  const normalizedRequestedCode = normalizeRoomCode(requestedRoomCode)
  const requestedNumber = roomNumber(requestedRoomCode)
  const assignment = graph.roomAssignments.find((item) => {
    const normalizedAssignmentCode = normalizeRoomCode(item.roomCode)
    return (
      normalizedAssignmentCode === normalizedRequestedCode ||
      Boolean(requestedNumber && roomNumber(item.roomCode) === requestedNumber)
    )
  })
  return assignment
    ? nodes.find((node) => node.id === assignment.nodeId)
    : undefined
}

export function createIndoorNavigationPlanFromGraph({
  graph,
  originFloorLabel,
  originRoomCode,
  destinationFloorLabel,
  destinationRoomCode,
}: CreateRuntimePlanInput): IndoorNavigationPlan | undefined {
  const floors: IndoorFloor[] = graph.floors
    .filter((floor) => VALID_FLOOR_NUMBERS.has(floor.floorNumber))
    .map((floor) => ({
      ...floor,
      floorNumber: floor.floorNumber as IndoorFloorNumber,
    }))
  const floorNumberById = new Map(
    floors.map((floor) => [floor.id, floor.floorNumber]),
  )
  const nodes: IndoorRouteNode[] = graph.nodes.flatMap((node) => {
    const floorNumber = floorNumberById.get(node.floorId)
    return floorNumber ? [{ ...node, floorNumber }] : []
  })
  const nodeIds = new Set(nodes.map((node) => node.id))
  const edges: IndoorRouteEdge[] = graph.edges.filter(
    (edge) => nodeIds.has(edge.fromNodeId) && nodeIds.has(edge.toNodeId),
  )

  const assignedDestination = findAssignedNode(
    graph,
    nodes,
    destinationRoomCode,
  )
  if (!assignedDestination) return undefined

  const destinationFloor =
    assignedDestination.floorNumber ??
    parseFloorNumber(destinationFloorLabel, destinationRoomCode)
  if (!destinationFloor) return undefined

  const assignedOrigin = findAssignedNode(graph, nodes, originRoomCode)
  const originFloor =
    assignedOrigin?.floorNumber ??
    parseFloorNumber(originFloorLabel, originRoomCode) ??
    destinationFloor
  const originNode =
    assignedOrigin ??
    nodes.find(
      (node) =>
        node.floorNumber === originFloor &&
        (node.type === 'ENTRANCE' || node.type === 'STAIRS'),
    ) ??
    nodes.find((node) => node.floorNumber === originFloor)
  if (!originNode) return undefined

  const route = findIndoorRoute(
    nodes,
    edges,
    originNode.id,
    assignedDestination.id,
  )
  if (route.length === 0) return undefined

  const floorSequence = route.reduce<IndoorFloorNumber[]>((result, node) => {
    if (result.at(-1) !== node.floorNumber) result.push(node.floorNumber)
    return result
  }, [])

  return {
    floors,
    nodes,
    edges,
    route,
    originNode,
    destinationNode: assignedDestination,
    floorSequence,
  }
}
