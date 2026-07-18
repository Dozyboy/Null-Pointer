/* @vitest-environment jsdom */

import '@testing-library/jest-dom/vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { MapScreen } from './MapScreen'

describe('MapScreen', () => {
  it('yêu cầu xác nhận trước khi chuyển sang điểm tiếp theo', () => {
    const onServiceCompleted = vi.fn()

    render(
      <MapScreen
        origin="Phòng xét nghiệm máu 113"
        originRoomCode="XN-113"
        originFloor="Tầng 1"
        destination="Phòng X-quang 201"
        destinationRoomCode="XQ-201"
        floor="Tầng 2"
        travelMinutes={4}
        onServiceCompleted={onServiceCompleted}
        onBack={() => undefined}
      />,
    )

    expect(screen.getByAltText('Sơ đồ Tầng 1')).toHaveAttribute(
      'src',
      '/maps/floor-1.png',
    )
    expect(screen.getByLabelText('Đường đi được đề xuất')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Đã lên Tầng 2' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Tôi đã khám xong' }))

    expect(onServiceCompleted).not.toHaveBeenCalled()
    expect(screen.getByRole('dialog', { name: 'Xác nhận đã khám xong?' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Xác nhận đã khám xong' }))

    expect(onServiceCompleted).toHaveBeenCalledOnce()
  })
})
