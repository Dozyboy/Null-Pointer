import { describe, expect, it } from 'vitest'
import { patientProfileSchema } from './patient.schemas'

describe('patientProfileSchema', () => {
  it('kiểm tra dữ liệu hồ sơ bệnh nhân từ backend', () => {
    const result = patientProfileSchema.parse({
      id: 'BN-00847',
      full_name: 'Nguyễn Thị Mai',
      date_of_birth: '1987-04-16',
      gender: 'female',
      phone: '0900000847',
      email: 'mai.nguyen@example.test',
      national_id: '001087000847',
      health_insurance_number: 'HN40100847',
      address: 'Hà Nội',
      emergency_contact_name: 'Nguyễn Văn Nam',
      emergency_contact_phone: '0911000847',
      blood_type: 'A+',
      allergies: ['Penicillin'],
      chronic_conditions: ['Tăng huyết áp'],
      mobility_support: false,
      visual_support: false,
      hearing_support: false,
      current_encounter_id: 'TM-2026-00847',
      attending_doctor_name: 'BS. Trần Văn Hùng',
      doctor_room_code: 'PK-305',
      created_at: '2026-07-18T08:00:00Z',
    })

    expect(result.id).toBe('BN-00847')
    expect(result.allergies).toEqual(['Penicillin'])
  })
})
