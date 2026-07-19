export type IndoorFloorNumber = 1 | 2 | 3 | 4

export interface IndoorFloor {
  id: string
  floorNumber: IndoorFloorNumber
  name: string
  mapImageUrl: string
  mapWidth: number
  mapHeight: number
}
export type IndoorRouteNodeType =
  | 'CORRIDOR'
  | 'DOOR'
  | 'STAIRS'
  | 'ELEVATOR'
  | 'ENTRANCE'

export interface IndoorRouteNode {
  id: string
  floorId: string
  floorNumber: IndoorFloorNumber
  name: string
  xPercent: number
  yPercent: number
  type: IndoorRouteNodeType
}

export interface IndoorRouteEdge {
  id: string
  floorId: string
  fromNodeId: string
  toNodeId: string
  type: 'CORRIDOR' | 'STAIRS' | 'ELEVATOR'
  isInterFloor: boolean
}

export interface IndoorNavigationPlan {
  floors: IndoorFloor[]
  nodes: IndoorRouteNode[]
  edges: IndoorRouteEdge[]
  route: IndoorRouteNode[]
  originNode: IndoorRouteNode
  destinationNode: IndoorRouteNode
  floorSequence: IndoorFloorNumber[]
}
