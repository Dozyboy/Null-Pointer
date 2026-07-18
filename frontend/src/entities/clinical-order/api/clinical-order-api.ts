import { apiRequest } from '../../../shared/api/http-client'
import {
  clinicalOrderDispatchSchema,
  type ClinicalOrderDispatch,
  type DispatchClinicalOrderPayload,
  type RecalculateClinicalOrderRoutePayload,
} from '../model/clinical-order.schemas'

export function dispatchClinicalOrder(
  payload: DispatchClinicalOrderPayload,
): Promise<ClinicalOrderDispatch> {
  return apiRequest('/simulation/clinical-orders', clinicalOrderDispatchSchema, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getLatestPatientOrder(
  patientCode: string,
): Promise<ClinicalOrderDispatch> {
  return apiRequest(
    `/simulation/patients/${encodeURIComponent(patientCode)}/clinical-orders/latest`,
    clinicalOrderDispatchSchema,
  )
}

export function recalculateLatestPatientRoute(
  patientCode: string,
  payload: RecalculateClinicalOrderRoutePayload,
): Promise<ClinicalOrderDispatch> {
  return apiRequest(
    `/simulation/patients/${encodeURIComponent(patientCode)}/clinical-orders/latest/route-proposals`,
    clinicalOrderDispatchSchema,
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
  )
}
