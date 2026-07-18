import { z } from 'zod'

const envSchema = z.object({
  VITE_API_URL: z
    .string()
    .url()
    .default('https://nhip-vien-backend-845428428754.asia-east1.run.app/api/v1'),
})

export const env = envSchema.parse(import.meta.env)
