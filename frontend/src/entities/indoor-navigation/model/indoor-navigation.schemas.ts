import { z } from 'zod'

export const indoorNodeTypeSchema = z.enum([
  'CORRIDOR',
  'DOOR',
  'STAIRS',
  'ELEVATOR',
  'ENTRANCE',
])
export const indoorEdgeTypeSchema = z.enum([
  'CORRIDOR',
  'STAIRS',
  'ELEVATOR',
])

const floorSchema = z.object({
  id: z.string(),
  floor_number: z.number().int().min(1),
  name: z.string(),
  map_image_url: z.string(),
  map_width: z.number().int().positive(),
  map_height: z.number().int().positive(),
})

const nodeSchema = z.object({
  id: z.string(),
  floor_id: z.string(),
  name: z.string(),
  x_percent: z.number().min(0).max(100),
  y_percent: z.number().min(0).max(100),
  type: indoorNodeTypeSchema,
  connector_code: z.string().nullable(),
})

const edgeSchema = z.object({
  id: z.string(),
  floor_id: z.string(),
  from_node_id: z.string(),
  to_node_id: z.string(),
  type: indoorEdgeTypeSchema,
  is_inter_floor: z.boolean(),
})

const roomAssignmentSchema = z.object({
  room_code: z.string(),
  node_id: z.string(),
})

export const indoorNavigationGraphSchema = z
  .object({
    version: z.number().int().positive(),
    updated_at: z.string(),
    floors: z.array(floorSchema),
    nodes: z.array(nodeSchema),
    edges: z.array(edgeSchema),
    room_assignments: z.array(roomAssignmentSchema),
  })
  .transform((value) => ({
    version: value.version,
    updatedAt: value.updated_at,
    floors: value.floors.map((floor) => ({
      id: floor.id,
      floorNumber: floor.floor_number,
      name: floor.name,
      mapImageUrl: floor.map_image_url,
      mapWidth: floor.map_width,
      mapHeight: floor.map_height,
    })),
    nodes: value.nodes.map((node) => ({
      id: node.id,
      floorId: node.floor_id,
      name: node.name,
      xPercent: node.x_percent,
      yPercent: node.y_percent,
      type: node.type,
      ...(node.connector_code ? { connectorCode: node.connector_code } : {}),
    })),
    edges: value.edges.map((edge) => ({
      id: edge.id,
      floorId: edge.floor_id,
      fromNodeId: edge.from_node_id,
      toNodeId: edge.to_node_id,
      type: edge.type,
      isInterFloor: edge.is_inter_floor,
    })),
    roomAssignments: value.room_assignments.map((assignment) => ({
      roomCode: assignment.room_code,
      nodeId: assignment.node_id,
    })),
  }))

export type IndoorNodeType = z.infer<typeof indoorNodeTypeSchema>
export type IndoorEdgeType = z.infer<typeof indoorEdgeTypeSchema>
export type IndoorNavigationGraph = z.infer<typeof indoorNavigationGraphSchema>
export type IndoorFloor = IndoorNavigationGraph['floors'][number]
export type IndoorRouteNode = IndoorNavigationGraph['nodes'][number]
export type IndoorRouteEdge = IndoorNavigationGraph['edges'][number]

export interface CreateIndoorNodePayload {
  floorId: string
  name: string
  xPercent: number
  yPercent: number
  type: IndoorNodeType
  connectorCode?: string
}

export interface UpdateIndoorNodePayload {
  name?: string
  xPercent?: number
  yPercent?: number
  type?: IndoorNodeType
  connectorCode?: string | null
}

export interface CreateIndoorEdgePayload {
  fromNodeId: string
  toNodeId: string
  type: IndoorEdgeType
}
