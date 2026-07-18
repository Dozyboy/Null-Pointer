/* @vitest-environment jsdom */

import '@testing-library/jest-dom/vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { ClinicalOrderDispatch } from '../../../entities/clinical-order/model/clinical-order.schemas'
import { recalculateLatestPatientRoute } from '../../../entities/clinical-order/api/clinical-order-api'
import { mapClinicalOrderRoutes } from '../api/patient-flow-api'
import type { Route } from '../model/patient-flow.types'
import { RouteChoiceScreen } from './RouteChoiceScreen'

vi.mock('../../../entities/clinical-order/api/clinical-order-api', () => ({
  recalculateLatestPatientRoute: vi.fn(),
}))

vi.mock('../api/patient-flow-api', () => ({
  createRouteProposal: vi.fn(),
  mapClinicalOrderRoutes: vi.fn(),
}))

afterEach(() => {
  vi.clearAllMocks()
})

const recalculatedRoute: Route = {
  id: 'recommended',
  proposalId: 'PROPOSAL-NEW',
  backendOptionId: 'OPTION-NEW',
  encounterId: 'TM-TEST',
  label: 'Khuyến nghị',
  badge: 'KHUYẾN NGHỊ',
  badgeColor: 'bg-primary text-primary-foreground',
  duration: '35–45 phút',
  steps: ['Phòng nước tiểu 104 — Tầng 1'],
  stepDetails: [],
  distance: 80,
  floorChanges: 0,
  reason: 'Đã tính lại từ hàng chờ hiện tại.',
  updatedAt: 'vừa xong',
  expiresAt: '2026-07-18T05:00:00Z',
  waitTimes: ['2–5 phút'],
}

describe('RouteChoiceScreen', () => {
  it('gọi backend để tính lại phần dịch vụ chưa hoàn thành theo chế độ đã chọn', async () => {
    vi.mocked(recalculateLatestPatientRoute).mockResolvedValue(
      {} as ClinicalOrderDispatch,
    )
    vi.mocked(mapClinicalOrderRoutes).mockReturnValue([recalculatedRoute])
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    })

    render(
      <QueryClientProvider client={queryClient}>
        <RouteChoiceScreen
          priority="fastest"
          scheduleStrategy="leave_fast"
          recalculation={{
            patientCode: 'BN-TEST',
            completedServiceCodes: ['blood_test'],
            startRoomCode: 'XN-113',
          }}
          onBack={() => undefined}
          onSelect={() => undefined}
          onViewDetail={() => undefined}
        />
      </QueryClientProvider>,
    )

    expect(await screen.findByText('Phòng nước tiểu 104 — Tầng 1')).toBeInTheDocument()
    expect(recalculateLatestPatientRoute).toHaveBeenCalledWith('BN-TEST', {
      priority: 'fastest',
      schedule_strategy: 'leave_fast',
      completed_route_service_codes: ['blood_test'],
      start_room_code: 'XN-113',
    })
  })
})
