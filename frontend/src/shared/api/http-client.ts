import type { z } from 'zod'
import { env } from '../config/env'

export class ApiError extends Error {
  readonly status: number
  readonly requestId?: string

  constructor(
    message: string,
    status: number,
    requestId?: string,
  ) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.requestId = requestId
  }
}

export async function apiRequest<TSchema extends z.ZodType>(
  path: string,
  schema: TSchema,
  init?: RequestInit,
): Promise<z.infer<TSchema>> {
  const response = await fetch(`${env.VITE_API_URL}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  })

  const requestId = response.headers.get('x-request-id') ?? undefined

  if (!response.ok) {
    throw new ApiError('Yêu cầu tới máy chủ thất bại.', response.status, requestId)
  }

  return schema.parse(await response.json())
}
