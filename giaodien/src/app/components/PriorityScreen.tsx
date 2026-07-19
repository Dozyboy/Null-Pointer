import { ChevronRight, Check, Zap, Sliders } from "lucide-react";
import { useState } from "react";
import { AppHeader } from "./AppHeader";

export type Priority = "system" | "fastest" | "lessWalk" | "lessCrowd" | "accessible";

interface PriorityScreenProps {
  onBack: () => void;
  onContinue: (priority: Priority) => void;
  onUpdateAccessibility: () => void;
}

const options: {
  id: Priority;
  label: string;
  description: string;
  icon: React.ReactNode;
}[] = [
  {
    id: "system",
    label: "Cân bằng",
    description: "Cân bằng thời gian chờ, thời điểm có kết quả và việc di chuyển",
    icon: <Sliders size={22} />,
  },
  {
    id: "fastest",
    label: "Ưu tiên vào khám – làm dịch vụ sớm",
    description: "Ưu tiên được tiếp nhận và hoàn thành các dịch vụ sớm; có thể chờ gặp lại bác sĩ lâu hơn",
    icon: <Zap size={22} />,
  },
  {
    id: "lessCrowd",
    label: "Ưu tiên làm xong, có kết quả đến tay bác sĩ sớm để gặp lại bác sĩ",
    description: "Sắp xếp để hoàn thành dịch vụ, có đủ kết quả và gặp lại bác sĩ sớm nhất",
    icon: <Check size={22} />,
  },
];

export function PriorityScreen({ onBack, onContinue }: PriorityScreenProps) {
  const [selected, setSelected] = useState<Priority>("fastest");

  return (
    <div className="flex flex-col min-h-full bg-background">
      <AppHeader
        title="Chọn điều ưu tiên"
        subtitle="Bước 2/4"
        progress={{ current: 2, total: 4 }}
        onBack={onBack}
        onForward={() => onContinue(selected)}
        forwardLabel="Tạo phương án"
      />

      <div className="flex flex-col gap-3 px-4 pt-4 pb-6">
        <p style={{ fontSize: 15 }} className="text-foreground">Bạn muốn hệ thống sắp lịch trình theo cách nào?</p>

        {options.map((opt) => {
          const isSelected = selected === opt.id;
          return (
            <button
              key={opt.id}
              onClick={() => setSelected(opt.id)}
              className={`w-full text-left rounded-xl border-2 p-4 flex items-start gap-4 transition-all active:scale-[0.99] ${
                isSelected ? "border-primary bg-secondary" : "border-border bg-card"
              }`}
              style={{ minHeight: 72 }}
            >
              <div className={`w-11 h-11 rounded-lg flex items-center justify-center flex-shrink-0 ${
                isSelected ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
              }`}>
                {opt.icon}
              </div>
              <div className="flex-1 min-w-0">
                <p style={{ fontSize: 16 }} className={isSelected ? "text-primary" : "text-foreground"}>
                  {opt.label}
                </p>
                <p style={{ fontSize: 13 }} className="text-muted-foreground mt-0.5 leading-snug">
                  {opt.description}
                </p>
              </div>
              <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-0.5 ${
                isSelected ? "border-primary bg-primary" : "border-border"
              }`}>
                {isSelected && <Check size={14} className="text-white" strokeWidth={3} />}
              </div>
            </button>
          );
        })}

        {/* Primary action */}
        <button
          onClick={() => onContinue(selected)}
          className="w-full py-4 rounded-xl bg-primary text-primary-foreground flex items-center justify-center gap-2 active:scale-[0.98] transition-all"
          style={{ fontSize: 17, minHeight: 56 }}
        >
          Tạo phương án
          <ChevronRight size={20} />
        </button>

        <button
          onClick={onUpdateAccessibility}
          className="w-full py-3 rounded-xl border border-border bg-card text-foreground text-center"
          style={{ fontSize: 15, minHeight: 48 }}
        >
          Cập nhật nhu cầu hỗ trợ
        </button>
      </div>
    </div>
  );
}
