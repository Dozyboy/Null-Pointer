import { useState } from 'react'
import {
  Accessibility,
  CheckCircle2,
  MapPin,
  Navigation,
} from 'lucide-react'
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
  onServiceCompleted: () => void
  onBack: () => void
}
export function DirectionsScreen({
  origin,
  originRoomCode,
  originFloor,
  destination,
  roomCode,
  floor,
  distance,
  onServiceCompleted,
  onBack,
}: DirectionsScreenProps) {
  const [showCompletionConfirmation, setShowCompletionConfirmation] =
    useState(false)
  const directionSteps = [
    `Xác định chấm xanh tại ${origin}.`,
    'Đi theo tuyến màu xanh; dùng nút phóng to nếu cần xem rõ hành lang.',
    `Nếu đổi tầng, đến Cầu thang A và bấm xác nhận để xem tiếp đoạn đường trên tầng mới.`,
    `Đến chấm đỏ tại ${destination} và đối chiếu mã phòng ${
      roomCode ?? destination
    }.`,
  ]

  return (
    <div className="flex min-h-full flex-col bg-background pb-6">
      <AppHeader
        title={`Đến ${destination}`}
        subtitle={`Từ ${origin} · ${floor} · ${distance}`}
        onBack={onBack}
        onForward={() => setShowCompletionConfirmation(true)}
        forwardLabel="Tôi đã khám xong"
      />

      <div className="flex flex-col gap-3 px-4 pt-4">
        <IndoorNavigationPanel
          originName={origin}
          originRoomCode={originRoomCode}
          originFloor={originFloor}
          destinationName={destination}
          destinationRoomCode={roomCode}
          destinationFloor={floor}
          compact
        />

        <div className="rounded-xl border border-border bg-card p-4">
          <div className="mb-3 flex items-center gap-3">
            <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
              <MapPin size={18} className="text-primary" />
            </div>
            <div>
              <p style={{ fontSize: 16 }} className="text-foreground">
                {destination}
              </p>
              <p style={{ fontSize: 13 }} className="text-muted-foreground">
                {floor} · {distance}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-lg bg-secondary px-3 py-2">
            <Accessibility size={15} className="text-primary" />
            <p style={{ fontSize: 13 }} className="text-primary">
              Nếu cần xe lăn hoặc không sử dụng được cầu thang, hãy liên hệ quầy
              hỗ trợ trước khi di chuyển.
            </p>
          </div>
        </div>

        <div className="overflow-hidden rounded-xl border border-border bg-card">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <Navigation size={15} className="text-primary" />
            <p style={{ fontSize: 14 }} className="text-foreground">
              Hướng dẫn từng bước
            </p>
          </div>
          <div className="flex flex-col gap-3 p-4">
            {directionSteps.map((step, index) => (
              <div key={step} className="flex gap-3">
                <div className="mt-0.5 flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-primary">
                  <span className="text-white" style={{ fontSize: 13 }}>
                    {index + 1}
                  </span>
                </div>
                <p
                  style={{ fontSize: 14 }}
                  className="flex-1 leading-relaxed text-foreground"
                >
                  {step}
                </p>
              </div>
            ))}
          </div>
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
