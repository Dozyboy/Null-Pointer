import { describe, expect, it } from 'vitest'
import type { IndoorNavigationGraph } from '../../../entities/indoor-navigation/model/indoor-navigation.schemas'
import { createIndoorNavigationPlanFromGraph } from './indoor-map-runtime'

const graph: IndoorNavigationGraph = {
  version: 3,
  updatedAt: '2026-07-18T12:00:00Z',
  floors: [
    {
      id: 'floor-1',
      floorNumber: 1,
      name: 'Tầng 1',
      mapImageUrl: '/maps/floor-1.png',
      mapWidth: 1000,
      mapHeight: 800,
    },
  ],
  nodes: [
    {
      id: 'entrance',
      floorId: 'floor-1',
      name: 'Lối vào',
      xPercent: 10,
      yPercent: 90,
      type: 'ENTRANCE',
    },
    {
      id: 'hall',
      floorId: 'floor-1',
      name: 'Hành lang đã chỉnh',
      xPercent: 55,
      yPercent: 55,
      type: 'CORRIDOR',
    },
    {
      id: 'room-103',
      floorId: 'floor-1',
      name: 'Cửa phòng 103',
      xPercent: 88,
      yPercent: 20,
      type: 'DOOR',
    },
  ],
  edges: [
    {
      id: 'edge-1',
      floorId: 'floor-1',
      fromNodeId: 'entrance',
      toNodeId: 'hall',
      type: 'CORRIDOR',
      isInterFloor: false,
    },
    {
      id: 'edge-2',
      floorId: 'floor-1',
      fromNodeId: 'hall',
      toNodeId: 'room-103',
      type: 'CORRIDOR',
      isInterFloor: false,
    },
  ],
  roomAssignments: [{ roomCode: 'XN-103', nodeId: 'room-103' }],
}

describe('createIndoorNavigationPlanFromGraph', () => {
  it('dùng node và cạnh tải từ backend để lập tuyến', () => {
    const plan = createIndoorNavigationPlanFromGraph({
      graph,
      originFloorLabel: 'Tầng 1',
      destinationFloorLabel: 'Tầng 1',
      destinationRoomCode: 'ROOM-XN-103',
    })

    expect(plan?.route.map((node) => node.id)).toEqual([
      'entrance',
      'hall',
      'room-103',
    ])
    expect(plan?.destinationNode.xPercent).toBe(88)
  })
})
