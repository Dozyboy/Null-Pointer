import { apiRequest } from '../../../shared/api/http-client'
import {
  patientProfileListSchema,
  patientProfileSchema,
  type PatientProfile,
} from '../model/patient.schemas'

export function getPatients(): Promise<PatientProfile[]> {
  return apiRequest('/patients', patientProfileListSchema)
}

export function getPatient(patientId: string): Promise<PatientProfile> {
  return apiRequest(
    '/patients/' + encodeURIComponent(patientId),
    patientProfileSchema,
  )
}
