import { z } from 'zod'

const envSchema = z.object({
  VITE_API_URL: z.string().url().default('http://localhost:8000/api/v1'),
})

export const env = envSchema.parse(import.meta.env)
