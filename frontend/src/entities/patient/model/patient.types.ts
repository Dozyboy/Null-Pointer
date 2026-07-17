export interface PatientSummary {
  id: string
  fullName: string
  dateOfBirth: string
  encounterId: string
  accessibilityNeeds: AccessibilityNeeds
}

export interface AccessibilityNeeds {
  wheelchair: boolean
  avoidStairs: boolean
  visualAssistance: boolean
}
