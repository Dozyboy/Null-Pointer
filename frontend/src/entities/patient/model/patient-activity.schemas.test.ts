import { describe, expect, it } from 'vitest'
import { patientActivitySchema } from './patient-activity.schemas'

describe('patientActivitySchema', () => {
  it('kiểm tra bản ghi hoạt động thật nhận từ backend', () => {
    const activity = patientActivitySchema.parse({
      id: 'ACT-001',
      patient_code: 'BN-00847',
      encounter_id: 'TM-2026-00847',
      activity_type: 'clinical_order_dispatched',
      title: 'Đã nhận 2 chỉ định mới',
      description: 'Bác sĩ đã gửi xét nghiệm máu và X-quang.',
      occurred_at: '2026-07-18T03:00:00Z',
      room_code: 'PK-305',
      clinical_order_id: 'SIM-ORDER-001',
      reservation_id: null,
    })

    expect(activity.patient_code).toBe('BN-00847')
    expect(activity.activity_type).toBe('clinical_order_dispatched')
  })
})
