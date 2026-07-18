import { describe, expect, it } from 'vitest'
import { buildPatientAccessUrl } from './patient-access'

describe('buildPatientAccessUrl', () => {
  it('tạo đường dẫn QR chứa mã bệnh nhân', () => {
    expect(buildPatientAccessUrl('https://demo.nhipvien.vn/', 'BN-00847')).toBe(
      'https://demo.nhipvien.vn/demo/patient/BN-00847',
    )
  })
})
