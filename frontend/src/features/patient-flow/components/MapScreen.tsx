import { useState } from 'react'
import {
  Accessibility,
  CheckCircle2,
  ChevronRight,
  MapPin,
  Navigation,
} from 'lucide-react'
import { AppHeader } from './AppHeader'
import { IndoorNavigationPanel } from './IndoorNavigationPanel'
import { ServiceCompletionDialog } from './ServiceCompletionDialog'

interface MapScreenProps {
  origin?: string
  originRoomCode?: string
  originFloor?: string
  destination: string
  destinationRoomCode?: string
  floor: string
  travelMinutes: number
  onServiceCompleted: () => void
  onBack: () => void
}
export function MapScreen({
  origin = 'Vị trí hiện tại',
  originRoomCode,
  originFloor,
  destination,
  destinationRoomCode,
  floor,
  travelMinutes,
  onServiceCompleted,
  onBack,
}: MapScreenProps) {
  const [directionsOpen, setDirectionsOpen] = useState(true)
  const [showCompletionConfirmation, setShowCompletionConfirmation] =
    useState(false)
  const directionSteps = [
    `Tìm chấm xanh tại ${origin} và đi theo tuyến màu xanh trên bản đồ.`,
    `Nếu tuyến đổi tầng, đi đến Cầu thang A và xác nhận tầng tiếp theo trên màn hình.`,
    `Đến chấm đỏ tại ${destination} và đối chiếu mã phòng ${
      destinationRoomCode ?? destination
    }.`,
  ]

  return (
    <div className="flex min-h-full flex-col bg-background pb-8">
      <AppHeader
        title="Bản đồ bệnh viện"
        subtitle={`Đến ${destination} — ${floor}`}
        onBack={onBack}
      />

      <div className="flex flex-col gap-3 px-4 pt-4">
        <IndoorNavigationPanel
          originName={origin}
          originRoomCode={originRoomCode}
          originFloor={originFloor}
          destinationName={destination}
          destinationRoomCode={destinationRoomCode}
          destinationFloor={floor}
        />

        <div className="rounded-xl border border-border bg-card p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl bg-primary/10">
              <MapPin size={18} className="text-primary" />
            </div>
            <div className="flex-1">
              <p style={{ fontSize: 16 }} className="text-foreground">
                {destination}
              </p>
              <p style={{ fontSize: 13 }} className="text-muted-foreground">
                {floor} · Di chuyển dự kiến {travelMinutes} phút
              </p>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 rounded-lg bg-secondary px-3 py-2">
            <Accessibility size={14} className="flex-shrink-0 text-primary" />
            <p style={{ fontSize: 13 }} className="text-primary">
              Nếu cần xe lăn hoặc không sử dụng được cầu thang, hãy liên hệ quầy
              hỗ trợ trước khi di chuyển.
            </p>
          </div>
        </div>

        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <button
            type="button"
            onClick={() => setDirectionsOpen((isOpen) => !isOpen)}
            className="flex w-full items-center gap-3 px-4 py-3.5 text-left"
            style={{ minHeight: 52 }}
          >
            <Navigation size={17} className="flex-shrink-0 text-primary" />
            <p style={{ fontSize: 15 }} className="flex-1 text-foreground">
              Hướng dẫn từng bước
            </p>
            <ChevronRight
              size={18}
              className={`text-muted-foreground transition-transform duration-200 ${
                directionsOpen ? 'rotate-90' : ''
              }`}
            />
          </button>

          {directionsOpen && (
            <div className="flex flex-col gap-3 border-t border-border px-4 py-3">
              {directionSteps.map((step, index) => (
                <div key={step} className="flex gap-3">
                  <div className="mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary">
                    <span className="text-white" style={{ fontSize: 12 }}>
                      {index + 1}
                    </span>
                  </div>
                  <p
                    style={{ fontSize: 14 }}
                    className="leading-relaxed text-foreground"
                  >
                    {step}
                  </p>
                </div>
              ))}
            </div>
          )}
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
