import { describe, expect, it } from 'vitest'
import { indoorNavigationGraphSchema } from './indoor-navigation.schemas'

describe('indoorNavigationGraphSchema', () => {
  it('chuyển hợp đồng API sang dữ liệu dùng trong React', () => {
    const graph = indoorNavigationGraphSchema.parse({
      version: 2,
      updated_at: '2026-07-18T12:00:00Z',
      floors: [
        {
          id: 'floor-1',
          floor_number: 1,
          name: 'Tầng 1',
          map_image_url: '/maps/floor-1.png',
          map_width: 1000,
          map_height: 800,
        },
      ],
      nodes: [
        {
          id: 'node-1',
          floor_id: 'floor-1',
          name: 'Cửa phòng 101',
          x_percent: 20,
          y_percent: 30,
          type: 'DOOR',
          connector_code: null,
        },
      ],
      edges: [],
      room_assignments: [{ room_code: '101', node_id: 'node-1' }],
    })

    expect(graph.version).toBe(2)
    expect(graph.floors[0].floorNumber).toBe(1)
    expect(graph.nodes[0].xPercent).toBe(20)
    expect(graph.roomAssignments[0].roomCode).toBe('101')
  })
})
