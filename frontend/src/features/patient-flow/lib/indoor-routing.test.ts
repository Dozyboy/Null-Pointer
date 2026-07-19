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

  it('đi từ P405 đến cầu thang theo các giao điểm hành lang Tầng 4', () => {
    const plan = createIndoorNavigationPlan({
      originFloorLabel: 'Tầng 4',
      originRoomCode: 'P405',
      destinationFloorLabel: 'Tầng 1',
      destinationRoomCode: 'XN-113',
    })

    const floorFourRoute = plan?.route.filter((node) => node.floorNumber === 4)

    expect(floorFourRoute?.map((node) => node.id)).toEqual([
      'p405-floor-4',
      'central-junction-floor-4',
      'north-center-floor-4',
      'p404-floor-4',
      'p403-floor-4',
      'p402-floor-4',
      'p401-floor-4',
      'stairs-a-floor-4',
    ])
    expect(
      floorFourRoute?.every((node, index, route) => {
        const nextNode = route[index + 1]
        return (
          !nextNode ||
          node.xPercent === nextNode.xPercent ||
          node.yPercent === nextNode.yPercent
        )
      }),
    ).toBe(true)
  })

  it('gán node cửa phòng riêng cho toàn bộ P401 đến P408', () => {
    const roomNumbers = Array.from({ length: 8 }, (_, index) => 401 + index)
    const originNodeIds = roomNumbers.map((roomNumber) =>
      createIndoorNavigationPlan({
        originFloorLabel: 'Tầng 4',
        originRoomCode: `P${roomNumber}`,
        destinationFloorLabel: 'Tầng 4',
        destinationRoomCode: 'P401',
      })?.originNode.id,
    )

    expect(originNodeIds).toEqual(
      roomNumbers.map((roomNumber) => `p${roomNumber}-floor-4`),
    )
    expect(new Set(originNodeIds).size).toBe(8)
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
