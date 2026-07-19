import { apiRequest } from '../../../shared/api/http-client'
import {
  indoorNavigationGraphSchema,
  type CreateIndoorEdgePayload,
  type CreateIndoorNodePayload,
  type IndoorNavigationGraph,
  type UpdateIndoorNodePayload,
} from '../model/indoor-navigation.schemas'

export function getIndoorNavigationGraph(): Promise<IndoorNavigationGraph> {
  return apiRequest('/indoor-navigation/graph', indoorNavigationGraphSchema)
}

export function createIndoorNode(
  payload: CreateIndoorNodePayload,
): Promise<IndoorNavigationGraph> {
  return apiRequest(
    '/simulation/indoor-navigation/nodes',
    indoorNavigationGraphSchema,
    {
      method: 'POST',
      body: JSON.stringify({
        floor_id: payload.floorId,
        name: payload.name,
        x_percent: payload.xPercent,
        y_percent: payload.yPercent,
        type: payload.type,
        connector_code: payload.connectorCode ?? null,
      }),
    },
  )
}

export function updateIndoorNode(
  nodeId: string,
  payload: UpdateIndoorNodePayload,
): Promise<IndoorNavigationGraph> {
  return apiRequest(
    `/simulation/indoor-navigation/nodes/${encodeURIComponent(nodeId)}`,
    indoorNavigationGraphSchema,
    {
      method: 'PATCH',
      body: JSON.stringify({
        ...(payload.name !== undefined && { name: payload.name }),
        ...(payload.xPercent !== undefined && {
          x_percent: payload.xPercent,
        }),
        ...(payload.yPercent !== undefined && {
          y_percent: payload.yPercent,
        }),
        ...(payload.type !== undefined && { type: payload.type }),
        ...(payload.connectorCode !== undefined && {
          connector_code: payload.connectorCode,
        }),
      }),
    },
  )
}

export function deleteIndoorNode(nodeId: string): Promise<IndoorNavigationGraph> {
  return apiRequest(
    `/simulation/indoor-navigation/nodes/${encodeURIComponent(nodeId)}`,
    indoorNavigationGraphSchema,
    { method: 'DELETE' },
  )
}

export function createIndoorEdge(
  payload: CreateIndoorEdgePayload,
): Promise<IndoorNavigationGraph> {
  return apiRequest(
    '/simulation/indoor-navigation/edges',
    indoorNavigationGraphSchema,
    {
      method: 'POST',
      body: JSON.stringify({
        from_node_id: payload.fromNodeId,
        to_node_id: payload.toNodeId,
        type: payload.type,
      }),
    },
  )
}

export function deleteIndoorEdge(edgeId: string): Promise<IndoorNavigationGraph> {
  return apiRequest(
    `/simulation/indoor-navigation/edges/${encodeURIComponent(edgeId)}`,
    indoorNavigationGraphSchema,
    { method: 'DELETE' },
  )
}

export function assignRoomToIndoorNode(
  roomCode: string,
  nodeId: string | null,
): Promise<IndoorNavigationGraph> {
  return apiRequest(
    `/simulation/indoor-navigation/room-assignments/${encodeURIComponent(roomCode)}`,
    indoorNavigationGraphSchema,
    {
      method: 'PUT',
      body: JSON.stringify({ node_id: nodeId }),
    },
  )
}

export function resetIndoorNavigationGraph(): Promise<IndoorNavigationGraph> {
  return apiRequest(
    '/simulation/indoor-navigation/reset',
    indoorNavigationGraphSchema,
    { method: 'POST' },
  )
}
