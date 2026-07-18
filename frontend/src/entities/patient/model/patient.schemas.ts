import { z } from 'zod'

export const patientGenderSchema = z.enum(['male', 'female', 'other'])

export const patientProfileSchema = z.object({
  id: z.string(),
  full_name: z.string(),
  date_of_birth: z.string(),
  gender: patientGenderSchema,
  phone: z.string(),
  email: z.string().nullable(),
  national_id: z.string(),
  health_insurance_number: z.string(),
  address: z.string(),
  emergency_contact_name: z.string(),
  emergency_contact_phone: z.string(),
  blood_type: z.string(),
  allergies: z.array(z.string()),
  chronic_conditions: z.array(z.string()),
  mobility_support: z.boolean(),
  visual_support: z.boolean(),
  hearing_support: z.boolean(),
  current_encounter_id: z.string(),
  attending_doctor_name: z.string(),
  doctor_room_code: z.string(),
  created_at: z.string(),
})

export const patientProfileListSchema = z.array(patientProfileSchema)

export type PatientProfile = z.infer<typeof patientProfileSchema>
