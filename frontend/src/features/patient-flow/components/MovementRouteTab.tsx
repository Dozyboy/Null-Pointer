import { useMemo } from 'react'
import {
  ArrowDown,
  ArrowUp,
  Footprints,
  MapPin,
  Navigation,
} from 'lucide-react'
import type { IndoorNavigationGraph } from '../../../entities/indoor-navigation/model/indoor-navigation.schemas'
import { createIndoorNavigationPlan } from '../lib/indoor-map-data'
import { createIndoorNavigationPlanFromGraph } from '../lib/indoor-map-runtime'
import {
  buildMovementTimeline,
  type MovementTimelineItem,
} from '../lib/indoor-navigation-timeline'

export interface MovementRouteTabData {
  origin: string
  originRoomCode?: string
  originFloor?: string
  destination: string
  destinationRoomCode?: string
  destinationFloor: string
  travelMinutes: number
  navigationGraph?: IndoorNavigationGraph
}

interface MovementRouteTabProps extends MovementRouteTabData {
  onViewMap: () => void
}

function TimelineMarker({ item }: { item: MovementTimelineItem }) {
  if (item.kind === 'origin') {
    return <Navigation size={16} aria-hidden="true" />
  }
  if (item.kind === 'destination') {
    return <MapPin size={17} aria-hidden="true" />
  }
  if (item.kind === 'transition') {
    return item.transitionDirection === 'up' ? (
      <ArrowUp size={17} aria-hidden="true" />
    ) : (
      <ArrowDown size={17} aria-hidden="true" />
    )
  }
  return <Footprints size={16} aria-hidden="true" />
}

export function MovementRouteTab({
  origin,
  originRoomCode,
  originFloor,
  destination,
  destinationRoomCode,
  destinationFloor,
  travelMinutes,
  navigationGraph,
  onViewMap,
}: MovementRouteTabProps) {
  const navigationPlan = useMemo(
    () => {
      const input = {
        originFloorLabel: originFloor,
        originRoomCode,
        destinationFloorLabel: destinationFloor,
        destinationRoomCode,
      }
      return (
        (navigationGraph
          ? createIndoorNavigationPlanFromGraph({ graph: navigationGraph, ...input })
          : undefined) ?? createIndoorNavigationPlan(input)
      )
    },
    [
      destinationFloor,
      destinationRoomCode,
      navigationGraph,
      originFloor,
      originRoomCode,
    ],
  )
  const timelineItems = useMemo(
    () =>
      navigationPlan
        ? buildMovementTimeline({
            plan: navigationPlan,
            originName: origin,
            originRoomCode,
            destinationName: destination,
            destinationRoomCode,
          })
        : [],
    [
      destination,
      destinationRoomCode,
      navigationPlan,
      origin,
      originRoomCode,
    ],
  )
  const floorChanges = Math.max(
    (navigationPlan?.floorSequence.length ?? 1) - 1,
    0,
  )

  return (
    <section
      aria-labelledby="movement-route-title"
      className="flex flex-col gap-3 px-4 pb-8 pt-4"
    >
      <div className="overflow-hidden rounded-2xl bg-primary text-primary-foreground">
        <div className="grid grid-cols-[1fr_auto] gap-4 p-4">
          <div className="min-w-0">
            <p className="text-white/70" style={{ fontSize: 11 }}>
              ĐIỂM ĐẾN TIẾP THEO
            </p>
            <h2
              id="movement-route-title"
              className="mt-1 truncate text-white"
              style={{ fontSize: 18 }}
            >
              {destination}
            </h2>
            <p className="mt-1 text-white/75" style={{ fontSize: 12 }}>
              {destinationFloor}
              {destinationRoomCode ? ` · Phòng ${destinationRoomCode}` : ''}
            </p>
          </div>
          <div className="border-l border-white/20 pl-4 text-right">
            <p className="text-white/70" style={{ fontSize: 11 }}>
              DỰ KIẾN
            </p>
            <p className="mt-1 whitespace-nowrap text-white" style={{ fontSize: 18 }}>
              {travelMinutes} phút
            </p>
            <p className="mt-1 whitespace-nowrap text-white/70" style={{ fontSize: 11 }}>
              Đổi tầng {floorChanges} lần
            </p>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-card">
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <div>
            <p className="text-foreground" style={{ fontSize: 15 }}>
              Các chặng đường cần đi
            </p>
            <p className="text-muted-foreground" style={{ fontSize: 12 }}>
              Từ {origin} đến phòng dịch vụ tiếp theo
            </p>
          </div>
          <span
            className="rounded-full bg-primary/10 px-2 py-1 text-primary"
            style={{ fontSize: 11 }}
          >
            {timelineItems.length} bước
          </span>
        </div>

        {timelineItems.length > 0 ? (
          <div className="relative px-4 py-4">
            <div className="absolute bottom-8 left-[33px] top-8 w-0.5 bg-border" />
            <div className="flex flex-col gap-4">
              {timelineItems.map((item, index) => {
                const isOrigin = item.kind === 'origin'
                const isDestination = item.kind === 'destination'
                const isTransition = item.kind === 'transition'
                const markerClass = isDestination
                  ? 'border-emerald-500 bg-emerald-50 text-emerald-700'
                  : isTransition
                    ? 'border-amber-400 bg-amber-50 text-amber-700'
                    : isOrigin
                      ? 'border-primary bg-primary text-white'
                      : 'border-primary/30 bg-secondary text-primary'

                return (
                  <div key={item.id} className="relative z-10 flex gap-3">
                    <div
                      className={`flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border-2 ${markerClass}`}
                    >
                      <TimelineMarker item={item} />
                    </div>
                    <div
                      className={`min-w-0 flex-1 rounded-xl border p-3 ${
                        isOrigin
                          ? 'border-primary/30 bg-primary/5'
                          : isDestination
                            ? 'border-emerald-200 bg-emerald-50/70'
                            : 'border-border bg-background'
                      }`}
                    >
                      <div className="mb-1 flex items-center justify-between gap-2">
                        <span
                          className={
                            isDestination
                              ? 'text-emerald-700'
                              : isTransition
                                ? 'text-amber-700'
                                : 'text-primary'
                          }
                          style={{ fontSize: 10, letterSpacing: '0.06em' }}
                        >
                          {isOrigin
                            ? 'HIỆN TẠI'
                            : isDestination
                              ? 'ĐIỂM ĐẾN'
                              : isTransition
                                ? 'CHUYỂN TẦNG'
                                : `CHẶNG ${item.sequenceNumber ?? index}`}
                        </span>
                        <span
                          className="text-muted-foreground"
                          style={{ fontSize: 11 }}
                        >
                          Tầng {item.floorNumber}
                        </span>
                      </div>
                      <p className="text-foreground" style={{ fontSize: 14 }}>
                        {item.title}
                      </p>
                      <p
                        className="mt-1 leading-relaxed text-muted-foreground"
                        style={{ fontSize: 12 }}
                      >
                        {item.description}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        ) : (
          <div role="alert" className="px-4 py-5 text-muted-foreground">
            <p style={{ fontSize: 14 }}>
              Chưa có dữ liệu sơ đồ cho phòng này. Bạn vẫn có thể mở bản đồ để
              xem vị trí phòng.
            </p>
          </div>
        )}

        <div className="border-t border-border p-4">
          <button
            type="button"
            onClick={onViewMap}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary py-3 text-primary-foreground transition-all active:scale-[0.98]"
            style={{ fontSize: 15, minHeight: 50 }}
          >
            <MapPin size={17} />
            Mở bản đồ chỉ đường
          </button>
        </div>
      </div>
    </section>
  )
}
