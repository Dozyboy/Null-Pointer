import { useMemo, useState } from 'react'
import { ArrowDown, ArrowUp, Layers, MapPin, Navigation } from 'lucide-react'
import { createIndoorNavigationPlan } from '../lib/indoor-map-data'
import type { IndoorFloorNumber } from '../model/indoor-navigation.types'
import { IndoorMapCanvas } from './IndoorMapCanvas'

interface IndoorNavigationPanelProps {
  originName: string
  originRoomCode?: string
  originFloor?: string
  destinationName: string
  destinationRoomCode?: string
  destinationFloor: string
  compact?: boolean
}

export function IndoorNavigationPanel({
  originName,
  originRoomCode,
  originFloor,
  destinationName,
  destinationRoomCode,
  destinationFloor,
  compact = false,
}: IndoorNavigationPanelProps) {
  const plan = useMemo(
    () =>
      createIndoorNavigationPlan({
        originFloorLabel: originFloor,
        originRoomCode,
        destinationFloorLabel: destinationFloor,
        destinationRoomCode,
      }),
    [destinationFloor, destinationRoomCode, originFloor, originRoomCode],
  )
  const routeKey = `${originRoomCode ?? originName}-${
    destinationRoomCode ?? destinationName
  }`
  const [floorSelection, setFloorSelection] = useState<{
    routeKey: string
    floor: IndoorFloorNumber
  }>()
  const activeFloor =
    floorSelection?.routeKey === routeKey
      ? floorSelection.floor
      : plan?.floorSequence[0]
  const selectFloor = (floor: IndoorFloorNumber) =>
    setFloorSelection({ routeKey, floor })

  if (!plan || !activeFloor) {
    return (
      <div
        role="alert"
        className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-800"
      >
        <p style={{ fontSize: 15 }}>Chưa có dữ liệu bản đồ cho điểm đến này.</p>
        <p className="mt-1" style={{ fontSize: 13 }}>
          Vui lòng xem biển chỉ dẫn tại bệnh viện hoặc liên hệ quầy hỗ trợ.
        </p>
      </div>
    )
  }

  const floor = plan.floors.find(
    (candidate) => candidate.floorNumber === activeFloor,
  )!
  const routeOnFloor = plan.route.filter(
    (node) => node.floorNumber === activeFloor,
  )
  const currentNode =
    activeFloor === plan.originNode.floorNumber
      ? plan.originNode
      : routeOnFloor[0]
  const activeRouteFloorIndex = plan.floorSequence.indexOf(activeFloor)
  const nextRouteFloor = plan.floorSequence[activeRouteFloorIndex + 1]
  const transitionDirection =
    nextRouteFloor === undefined
      ? undefined
      : nextRouteFloor > activeFloor
        ? 'lên'
        : 'xuống'

  return (
    <div className="flex flex-col gap-3">
      <div className="flex gap-1 overflow-x-auto rounded-xl bg-primary p-1">
        {plan.floors.map((candidate) => {
          const isOnRoute = plan.floorSequence.includes(candidate.floorNumber)
          return (
            <button
              type="button"
              key={candidate.id}
              onClick={() => selectFloor(candidate.floorNumber)}
              className={`flex min-w-[76px] flex-1 items-center justify-center gap-1 rounded-lg px-2 py-2 transition-colors ${
                activeFloor === candidate.floorNumber
                  ? 'bg-white text-primary'
                  : 'text-white/70'
              }`}
              aria-pressed={activeFloor === candidate.floorNumber}
            >
              <Layers size={13} />
              <span style={{ fontSize: 13 }}>{candidate.name}</span>
              {isOnRoute && (
                <span
                  className="h-1.5 w-1.5 rounded-full bg-current"
                  aria-label="Tầng nằm trên tuyến đi"
                />
              )}
            </button>
          )
        })}
      </div>

      <IndoorMapCanvas
        floor={floor}
        currentNode={currentNode}
        route={routeOnFloor}
        destinationNode={plan.destinationNode}
        compact={compact}
      />

      <div className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 rounded-xl border border-border bg-card p-3">
        <Navigation size={17} className="mt-0.5 text-primary" />
        <div>
          <p style={{ fontSize: 13 }} className="text-muted-foreground">
            Tuyến đang hiển thị tại {floor.name}
          </p>
          <p style={{ fontSize: 14 }} className="mt-1 text-foreground">
            <strong>{originName}</strong> → <strong>{destinationName}</strong>
          </p>
        </div>
      </div>

      {nextRouteFloor !== undefined && (
        <div className="rounded-xl border border-primary/20 bg-secondary p-3">
          <div className="flex items-start gap-2">
            {transitionDirection === 'lên' ? (
              <ArrowUp size={18} className="mt-0.5 text-primary" />
            ) : (
              <ArrowDown size={18} className="mt-0.5 text-primary" />
            )}
            <div className="flex-1">
              <p style={{ fontSize: 14 }} className="text-foreground">
                Đi theo tuyến màu xanh đến Cầu thang A, sau đó đi{' '}
                {transitionDirection} Tầng {nextRouteFloor}.
              </p>
              <button
                type="button"
                onClick={() => selectFloor(nextRouteFloor)}
                className="mt-3 w-full rounded-lg bg-primary px-3 py-2.5 text-primary-foreground"
                style={{ minHeight: 44, fontSize: 14 }}
              >
                Đã {transitionDirection} Tầng {nextRouteFloor}
              </button>
            </div>
          </div>
        </div>
      )}

      {activeFloor === plan.destinationNode.floorNumber && (
        <div className="flex items-start gap-2 rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-emerald-800">
          <MapPin size={17} className="mt-0.5" />
          <p style={{ fontSize: 14 }}>
            Đi theo tuyến màu xanh đến chấm đỏ tại {destinationName}.
          </p>
        </div>
      )}
    </div>
  )
}
