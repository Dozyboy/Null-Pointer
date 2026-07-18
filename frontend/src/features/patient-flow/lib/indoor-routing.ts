import type {
  IndoorRouteEdge,
  IndoorRouteNode,
} from '../model/indoor-navigation.types'

function distanceBetween(a: IndoorRouteNode, b: IndoorRouteNode) {
  return Math.hypot(a.xPercent - b.xPercent, a.yPercent - b.yPercent)
}
function estimateRemainingDistance(a: IndoorRouteNode, b: IndoorRouteNode) {
  return a.floorId === b.floorId ? distanceBetween(a, b) : 0
}

export function findIndoorRoute(
  nodes: IndoorRouteNode[],
  edges: IndoorRouteEdge[],
  startId: string,
  endId: string,
): IndoorRouteNode[] {
  if (startId === endId) {
    return nodes.filter((node) => node.id === startId)
  }

  const nodesById = new Map(nodes.map((node) => [node.id, node]))
  const startNode = nodesById.get(startId)
  const endNode = nodesById.get(endId)
  if (!startNode || !endNode) return []

  const openNodeIds = new Set([startId])
  const previousNodeIds = new Map<string, string>()
  const travelledCosts = new Map<string, number>([[startId, 0]])
  const estimatedCosts = new Map<string, number>([
    [startId, estimateRemainingDistance(startNode, endNode)],
  ])

  while (openNodeIds.size > 0) {
    const currentId = [...openNodeIds].reduce((bestId, candidateId) =>
      (estimatedCosts.get(bestId) ?? Number.POSITIVE_INFINITY) <=
      (estimatedCosts.get(candidateId) ?? Number.POSITIVE_INFINITY)
        ? bestId
        : candidateId,
    )

    if (currentId === endId) {
      const routeIds = [currentId]
      while (previousNodeIds.has(routeIds[0])) {
        routeIds.unshift(previousNodeIds.get(routeIds[0])!)
      }
      return routeIds
        .map((nodeId) => nodesById.get(nodeId))
        .filter((node): node is IndoorRouteNode => node !== undefined)
    }

    openNodeIds.delete(currentId)
    const neighbours = edges.flatMap((edge) => {
      if (edge.fromNodeId === currentId) {
        return [{ nodeId: edge.toNodeId, edge }]
      }
      if (edge.toNodeId === currentId) {
        return [{ nodeId: edge.fromNodeId, edge }]
      }
      return []
    })

    for (const neighbour of neighbours) {
      const currentNode = nodesById.get(currentId)
      const nextNode = nodesById.get(neighbour.nodeId)
      if (!currentNode || !nextNode) continue

      const stepCost = neighbour.edge.isInterFloor
        ? neighbour.edge.type === 'STAIRS'
          ? 25
          : 18
        : distanceBetween(currentNode, nextNode)
      const candidateCost =
        (travelledCosts.get(currentId) ?? Number.POSITIVE_INFINITY) + stepCost

      if (
        candidateCost <
        (travelledCosts.get(neighbour.nodeId) ?? Number.POSITIVE_INFINITY)
      ) {
        previousNodeIds.set(neighbour.nodeId, currentId)
        travelledCosts.set(neighbour.nodeId, candidateCost)
        estimatedCosts.set(
          neighbour.nodeId,
          candidateCost + estimateRemainingDistance(nextNode, endNode),
        )
        openNodeIds.add(neighbour.nodeId)
      }
    }
  }

  return []
}
