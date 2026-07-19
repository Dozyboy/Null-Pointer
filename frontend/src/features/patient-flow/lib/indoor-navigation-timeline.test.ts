import { describe, expect, it } from 'vitest'
import { createIndoorNavigationPlan } from './indoor-map-data'
import { buildMovementTimeline } from './indoor-navigation-timeline'

describe('lịch trình di chuyển trong bệnh viện', () => {
  it('tạo đủ chặng đi bộ, chuyển tầng và điểm đến', () => {
    const plan = createIndoorNavigationPlan({
      originFloorLabel: 'Tầng 1',
      originRoomCode: 'XN-113',
      destinationFloorLabel: 'Tầng 2',
      destinationRoomCode: 'XQ-201',
    })

    expect(plan).toBeDefined()
    const items = buildMovementTimeline({
      plan: plan!,
      originName: 'Phòng xét nghiệm máu 113',
      originRoomCode: 'XN-113',
      destinationName: 'Phòng X-quang 201',
      destinationRoomCode: 'XQ-201',
    })

    expect(items.map((item) => item.kind)).toEqual([
      'origin',
      'walk',
      'transition',
      'walk',
      'destination',
    ])
    expect(items[2]).toMatchObject({
      title: 'Lên Tầng 2 bằng Cầu thang A',
      transitionDirection: 'up',
    })
    expect(
      items
        .filter((item) => item.kind === 'walk')
        .map((item) => item.sequenceNumber),
    ).toEqual([1, 2])
    expect(items.at(-1)?.title).toBe('Đến Phòng X-quang 201')
  })

  it('hiển thị lần lượt các tầng khi đi từ Tầng 4 xuống Tầng 1', () => {
    const plan = createIndoorNavigationPlan({
      originFloorLabel: 'Tầng 4',
      originRoomCode: 'P405',
      destinationFloorLabel: 'Tầng 1',
      destinationRoomCode: 'XN-113',
    })

    expect(plan).toBeDefined()
    const items = buildMovementTimeline({
      plan: plan!,
      originName: 'Phòng P405',
      destinationName: 'Phòng xét nghiệm máu 113',
    })

    expect(
      items
        .filter((item) => item.kind === 'transition')
        .map((item) => item.title),
    ).toEqual([
      'Xuống Tầng 3 bằng Cầu thang A',
      'Xuống Tầng 2 bằng Cầu thang A',
      'Xuống Tầng 1 bằng Cầu thang A',
    ])
  })
})
