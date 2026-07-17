import type { PatientSummary } from '../../entities/patient/model/patient.types'

export const patientFixture: PatientSummary = {
  id: 'patient-demo',
  fullName: 'Nguyễn Thị Mai',
  dateOfBirth: '1968-03-12',
  encounterId: 'TM-2026-00847',
  accessibilityNeeds: {
    wheelchair: false,
    avoidStairs: false,
    visualAssistance: false,
  },
}
