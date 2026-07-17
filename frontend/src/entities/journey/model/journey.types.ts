import type { CareRouteStep } from '../../care-route/model/care-route.types'

export type JourneyStepStatus =
  | 'pending'
  | 'held'
  | 'navigating'
  | 'arrived'
  | 'waiting'
  | 'in_service'
  | 'result_pending'
  | 'completed'
  | 'blocked'
  | 'cancelled'

export interface JourneyStep extends CareRouteStep {
  status: JourneyStepStatus
}

export interface Journey {
  id: string
  encounterId: string
  currentStepId: string
  steps: JourneyStep[]
  updatedAt: string
}
