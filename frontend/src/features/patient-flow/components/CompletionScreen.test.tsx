/* @vitest-environment jsdom */

import '@testing-library/jest-dom/vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { Route } from '../model/patient-flow.types'
import { CompletionScreen } from './CompletionScreen'

const route: Route = {
  id: 'balanced',
  proposalId: 'proposal-1',
  backendOptionId: 'option-1',
  encounterId: 'encounter-1',
  label: 'Cân bằng',
  badge: 'CÂN BẰNG',
  badgeColor: 'bg-primary',
  duration: '30–40 phút',
  steps: ['Phòng 113'],
  stepDetails: [
    {
      id: 'step-1',
      serviceCode: 'blood_test',
      serviceName: 'Xét nghiệm máu',
      roomCode: 'XN-113',
      roomName: 'Phòng 113',
      floor: 'Tầng 1',
      waitMinutesMin: 2,
      waitMinutesMax: 5,
      serviceMinutes: 5,
      travelMinutes: 2,
      isLocked: false,
    },
  ],
  distance: 30,
  floorChanges: 0,
  reason: 'Lộ trình kiểm thử',
  updatedAt: 'vừa xong',
  expiresAt: '2026-07-18T12:00:00Z',
  waitTimes: ['2–5 phút'],
}

describe('CompletionScreen', () => {
  it('cho phép quay lại màn hình chính', () => {
    const onBackToDashboard = vi.fn()

    render(
      <CompletionScreen
        route={route}
        doctorName="BS. Kiểm thử"
        onBackToDashboard={onBackToDashboard}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'Quay lại màn hình chính' }))

    expect(onBackToDashboard).toHaveBeenCalledOnce()
  })
})
