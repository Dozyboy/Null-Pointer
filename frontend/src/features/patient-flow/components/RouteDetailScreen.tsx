import { Lock, ChevronRight } from "lucide-react";
import { useState } from "react";
import { AppHeader } from "./AppHeader";
import type { Route } from "../model/patient-flow.types";

interface Step {
  name: string;
  room: string;
  floor: string;
  waitTime: string;
  duration: string;
  resultTime: string;
  distance: string;
  locked?: boolean;
  lockReason?: string;
}

const buildSteps = (route: Route): Step[] => route.stepDetails.map((step) => ({
  name: step.serviceName,
  room: step.roomName,
  floor: step.floor,
  waitTime: `${step.waitMinutesMin}–${step.waitMinutesMax} phút`,
  duration: `${step.serviceMinutes} phút`,
  resultTime: step.serviceCode === "doctor_return"
    ? "Khi đủ kết quả bắt buộc"
    : "Sau khi phòng hoàn tất xử lý",
  distance: step.travelMinutes === 0
    ? "Đang ở đúng khu vực"
    : `Di chuyển khoảng ${step.travelMinutes} phút`,
  locked: step.isLocked,
  lockReason: step.lockReason,
}));

interface RouteDetailScreenProps {
  route: Route;
  onBack: () => void;
  onConfirm: (route: Route) => void;
}

export function RouteDetailScreen({ route, onBack, onConfirm }: RouteDetailScreenProps) {
  const [steps] = useState<Step[]>(() => buildSteps(route));

  return (
    <div className="flex flex-col min-h-full bg-background">
      <AppHeader
        title="Chi tiết lộ trình"
        subtitle={`Hoàn tất dự kiến ${route.duration}`}
        progress={{ current: 4, total: 4 }}
        onBack={onBack}
        onForward={() => onConfirm(route)}
        forwardLabel="Xác nhận"
      />

      {/* Journey timeline */}
      <div className="px-4 pt-4 pb-32 relative">
        <div className="absolute left-[35px] top-8 bottom-8 w-0.5 bg-border" />

        {steps.map((step, idx) => {
          const isLast = idx === steps.length - 1;
          const displayRoom = `${step.room} — ${step.floor}`;

          return (
            <div key={idx} className="relative flex gap-4 mb-4">
              {/* Dot */}
              <div className="flex-shrink-0 z-10">
                {isLast ? (
                  <div className="w-9 h-9 rounded-full border-2 border-primary bg-card flex items-center justify-center">
                    <div className="w-3 h-3 rounded-full bg-primary" />
                  </div>
                ) : (
                  <div className="w-9 h-9 rounded-full bg-secondary border-2 border-primary/30 flex items-center justify-center">
                    <span style={{ fontSize: 14 }} className="text-primary">{idx + 1}</span>
                  </div>
                )}
              </div>

              {/* Card */}
              <div className="flex-1 bg-card rounded-xl border border-border p-4">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <p style={{ fontSize: 16 }} className="text-foreground">{step.name}</p>
                  {step.locked && (
                    <div className="flex items-center gap-1 bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full flex-shrink-0">
                      <Lock size={11} />
                      <span style={{ fontSize: 11 }}>Khóa</span>
                    </div>
                  )}
                </div>

                <p style={{ fontSize: 13 }} className="text-primary mb-2">{displayRoom}</p>

                {!isLast && (
                  <div className="grid grid-cols-2 gap-x-4 gap-y-1 mb-3">
                    {step.waitTime && (
                      <>
                        <span style={{ fontSize: 12 }} className="text-muted-foreground">Chờ dự kiến</span>
                        <span style={{ fontSize: 12 }} className="text-foreground">{step.waitTime}</span>
                      </>
                    )}
                    {step.duration && (
                      <>
                        <span style={{ fontSize: 12 }} className="text-muted-foreground">Thực hiện</span>
                        <span style={{ fontSize: 12 }} className="text-foreground">{step.duration}</span>
                      </>
                    )}
                    {step.resultTime && (
                      <>
                        <span style={{ fontSize: 12 }} className="text-muted-foreground">Kết quả dự kiến</span>
                        <span style={{ fontSize: 12 }} className="text-foreground">{step.resultTime}</span>
                      </>
                    )}
                    {step.distance && (
                      <>
                        <span style={{ fontSize: 12 }} className="text-muted-foreground">Di chuyển</span>
                        <span style={{ fontSize: 12 }} className="text-foreground">{step.distance}</span>
                      </>
                    )}
                  </div>
                )}

              </div>
            </div>
          );
        })}
      </div>

      {/* Fixed confirm bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-card border-t border-border px-4 py-4 z-30" style={{ maxWidth: 430, margin: "0 auto" }}>
        <button
          onClick={() => onConfirm(route)}
          className="w-full py-4 rounded-xl bg-primary text-primary-foreground flex items-center justify-center gap-2 active:scale-[0.98] transition-all"
          style={{ fontSize: 17, minHeight: 56 }}
        >
          Xác nhận lộ trình
          <ChevronRight size={20} />
        </button>
      </div>
    </div>
  );
}
