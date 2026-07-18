export type ScheduleStrategy = 'balanced' | 'finish_early' | 'leave_fast'

export type RoutePriority =
  | 'system'
  | 'fastest'
  | 'less_walk'
  | 'less_crowd'
  | 'accessible'

export interface CareRouteStep {
  id: string
  order: number
  serviceName: string
  roomName: string
  floor: string
  waitMinutesMin: number
  waitMinutesMax: number
  isLocked: boolean
  lockReason?: string
}

export interface CareRouteOption {
  id: string
  label:
    | 'balanced'
    | 'early_service'
    | 'doctor_ready'
    | 'recommended'
    | 'less_walk'
    | 'less_crowd'
  durationMinutesMin: number
  durationMinutesMax: number
  distanceMeters: number
  floorChanges: number
  reason: string
  updatedAt: string
  expiresAt: string
  steps: CareRouteStep[]
}
