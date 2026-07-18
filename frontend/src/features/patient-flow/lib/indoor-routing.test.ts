import { describe, expect, it } from 'vitest'
import { createIndoorNavigationPlan } from './indoor-map-data'
import { findIndoorRoute } from './indoor-routing'
import type {
  IndoorRouteEdge,
  IndoorRouteNode,
} from '../model/indoor-navigation.types'

describe('thuật toán chỉ đường trong bệnh viện', () => {
  it('tìm tuyến ngắn nhất giữa các điểm trong cùng tầng', () => {
    const nodes: IndoorRouteNode[] = [
      {
        id: 'a',
        floorId: 'floor-1',
        floorNumber: 1,
        name: 'A',
        xPercent: 0,
        yPercent: 0,
        type: 'DOOR',
      },
      {
        id: 'b',
        floorId: 'floor-1',
        floorNumber: 1,
        name: 'B',
        xPercent: 10,
        yPercent: 0,
        type: 'CORRIDOR',
      },
      {
        id: 'c',
        floorId: 'floor-1',
        floorNumber: 1,
        name: 'C',
        xPercent: 20,
        yPercent: 0,
        type: 'DOOR',
      },
    ]
    const edges: IndoorRouteEdge[] = [
      {
        id: 'a-b',
        floorId: 'floor-1',
        fromNodeId: 'a',
        toNodeId: 'b',
        type: 'CORRIDOR',
        isInterFloor: false,
      },
      {
        id: 'b-c',
        floorId: 'floor-1',
        fromNodeId: 'b',
        toNodeId: 'c',
        type: 'CORRIDOR',
        isInterFloor: false,
      },
    ]

    expect(findIndoorRoute(nodes, edges, 'a', 'c').map((node) => node.id)).toEqual([
      'a',
      'b',
      'c',
    ])
  })

  it('tạo tuyến liên tầng từ phòng xét nghiệm đến phòng X-quang', () => {
    const plan = createIndoorNavigationPlan({
      originFloorLabel: 'Tầng 1',
      originRoomCode: 'XN-113',
      destinationFloorLabel: 'Tầng 2',
      destinationRoomCode: 'XQ-201',
    })

    expect(plan).toBeDefined()
    expect(plan?.floorSequence).toEqual([1, 2])
    expect(plan?.route.some((node) => node.type === 'STAIRS')).toBe(true)
    expect(plan?.originNode.id).toContain('laboratory')
    expect(plan?.destinationNode.id).toContain('xray')
  })

  it('không tạo tuyến giả khi tầng chưa có bản đồ', () => {
    expect(
      createIndoorNavigationPlan({
        originFloorLabel: 'Tầng 1',
        destinationFloorLabel: 'Tầng 5',
        destinationRoomCode: 'P501',
      }),
    ).toBeUndefined()
  })
})
