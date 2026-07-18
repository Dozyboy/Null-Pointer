import { apiRequest } from '../../../shared/api/http-client'
import {
  patientActivityListSchema,
  type PatientActivity,
} from '../model/patient-activity.schemas'

export function getTodayPatientActivities(
  patientCode: string,
): Promise<PatientActivity[]> {
  return apiRequest(
    '/patients/' + encodeURIComponent(patientCode) + '/activities/today',
    patientActivityListSchema,
  )
}
