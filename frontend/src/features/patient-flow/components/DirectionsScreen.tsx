import { useMemo, useState } from 'react'
import {
  Accessibility,
  ArrowDown,
  ArrowUp,
  CheckCircle2,
  Footprints,
  ListChecks,
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
import { AppHeader } from './AppHeader'
import { IndoorNavigationPanel } from './IndoorNavigationPanel'
import { ServiceCompletionDialog } from './ServiceCompletionDialog'

interface DirectionsScreenProps {
  origin: string
  originRoomCode?: string
  originFloor?: string
  destination: string
  roomCode?: string
  floor: string
  distance: string
  navigationGraph?: IndoorNavigationGraph
  onServiceCompleted: () => void
  onBack: () => void
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

export function DirectionsScreen({
  origin,
  originRoomCode,
  originFloor,
  destination,
  roomCode,
  floor,
  distance,
  navigationGraph,
  onServiceCompleted,
  onBack,
}: DirectionsScreenProps) {
  const [showCompletionConfirmation, setShowCompletionConfirmation] =
    useState(false)
  const navigationPlan = useMemo(
    () => {
      const input = {
        originFloorLabel: originFloor,
        originRoomCode,
        destinationFloorLabel: floor,
        destinationRoomCode: roomCode,
      }
      return (
        (navigationGraph
          ? createIndoorNavigationPlanFromGraph({ graph: navigationGraph, ...input })
          : undefined) ?? createIndoorNavigationPlan(input)
      )
    },
    [floor, navigationGraph, originFloor, originRoomCode, roomCode],
  )
  const timelineItems = useMemo(
    () =>
      navigationPlan
        ? buildMovementTimeline({
            plan: navigationPlan,
            originName: origin,
            originRoomCode,
            destinationName: destination,
            destinationRoomCode: roomCode,
          })
        : [],
    [destination, navigationPlan, origin, originRoomCode, roomCode],
  )
  const floorChanges = Math.max(
    (navigationPlan?.floorSequence.length ?? 1) - 1,
    0,
  )
  const travelDuration = distance.replace(/^Di chuyển dự kiến\s*/u, '')

  return (
    <div className="flex min-h-full flex-col bg-background pb-6">
      <AppHeader
        title="Lộ trình di chuyển"
        subtitle={`${origin} → ${destination}`}
        onBack={onBack}
        onForward={() => setShowCompletionConfirmation(true)}
        forwardLabel="Tôi đã khám xong"
      />

      <div className="flex flex-col gap-3 px-4 pt-4">
        <div className="overflow-hidden rounded-xl bg-primary text-primary-foreground">
          <div className="grid grid-cols-[1fr_auto] gap-4 p-4">
            <div>
              <p className="text-white/70" style={{ fontSize: 11 }}>
                DI CHUYỂN DỰ KIẾN
              </p>
              <p className="mt-1 text-white" style={{ fontSize: 19 }}>
                {travelDuration}
              </p>
            </div>
            <div className="border-l border-white/20 pl-4 text-right">
              <p className="text-white/70" style={{ fontSize: 11 }}>
                ĐỔI TẦNG
              </p>
              <p className="mt-1 text-white" style={{ fontSize: 19 }}>
                {floorChanges} lần
              </p>
            </div>
          </div>
          <div className="border-t border-white/15 bg-black/5 px-4 py-2.5">
            <p className="text-white/80" style={{ fontSize: 13 }}>
              Điểm đến: <strong className="text-white">{destination}</strong> ·{' '}
              {floor}
            </p>
          </div>
        </div>

        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <div className="flex items-center gap-2">
              <ListChecks size={16} className="text-primary" />
              <p style={{ fontSize: 14 }} className="text-foreground">
                Các chặng cần đi
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
                Chưa có dữ liệu để lập các chặng di chuyển cho điểm đến này.
              </p>
            </div>
          )}
        </div>

        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <Navigation size={15} className="text-primary" />
            <p style={{ fontSize: 14 }} className="text-foreground">
              Bản đồ tuyến đường
            </p>
          </div>
          <div className="p-3">
            <IndoorNavigationPanel
              originName={origin}
              originRoomCode={originRoomCode}
              originFloor={originFloor}
              destinationName={destination}
              destinationRoomCode={roomCode}
              destinationFloor={floor}
              navigationGraph={navigationGraph}
              compact
            />
          </div>
        </div>

        <div className="flex items-start gap-2 rounded-xl border border-primary/20 bg-secondary px-3 py-3">
          <Accessibility size={16} className="mt-0.5 flex-shrink-0 text-primary" />
          <p style={{ fontSize: 13 }} className="text-primary">
            Nếu cần xe lăn hoặc không sử dụng được cầu thang, hãy liên hệ quầy
            hỗ trợ trước khi di chuyển.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setShowCompletionConfirmation(true)}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary py-4 text-primary-foreground transition-all active:scale-[0.98]"
          style={{ fontSize: 17, minHeight: 56 }}
        >
          <CheckCircle2 size={20} />
          Tôi đã khám xong
        </button>
      </div>

      {showCompletionConfirmation && (
        <ServiceCompletionDialog
          destination={destination}
          onCancel={() => setShowCompletionConfirmation(false)}
          onConfirm={() => {
            setShowCompletionConfirmation(false)
            onServiceCompleted()
          }}
        />
      )}
    </div>
  )
}
