import { z } from 'zod'

export const patientActivityTypeSchema = z.enum([
  'clinical_order_dispatched',
  'route_confirmed',
  'service_completed',
  'journey_completed',
])

export const patientActivitySchema = z.object({
  id: z.string(),
  patient_code: z.string(),
  encounter_id: z.string(),
  activity_type: patientActivityTypeSchema,
  title: z.string(),
  description: z.string(),
  occurred_at: z.string(),
  room_code: z.string().nullable(),
  clinical_order_id: z.string().nullable(),
  reservation_id: z.string().nullable(),
})

export const patientActivityListSchema = z.array(patientActivitySchema)

export type PatientActivity = z.infer<typeof patientActivitySchema>
