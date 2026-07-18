import {
  Accessibility,
  ArrowLeft,
  ChevronRight,
  HeadphonesIcon,
} from "lucide-react";
import { useState } from "react";
import {
  createSupportRequest,
  type SupportType,
} from "../api/patient-flow-api";

interface SupportScreenProps {
  encounterId: string;
  location: string;
  onBack?: () => void;
}

export function SupportScreen({ encounterId, location, onBack }: SupportScreenProps) {
  const [isRequesting, setIsRequesting] = useState(false);
  const [requestMessage, setRequestMessage] = useState<string | null>(null);

  async function handleSupportRequest(type: SupportType) {
    setIsRequesting(true);
    setRequestMessage(null);
    try {
      const response = await createSupportRequest(type, encounterId, location);
      setRequestMessage(
        `Đã lưu yêu cầu ${response.id.slice(0, 12)}. Nhân viên dự kiến phản hồi trong ${response.estimated_response_minutes_min}–${response.estimated_response_minutes_max} phút.`,
      );
    } catch {
      setRequestMessage("Không thể gửi yêu cầu. Vui lòng thử lại hoặc liên hệ quầy hỗ trợ gần nhất.");
    } finally {
      setIsRequesting(false);
    }
  }

  return (
    <div className="flex flex-col min-h-full bg-background pb-24">
      <div className="bg-card border-b border-border px-4 pt-10 pb-4">
        <div className="flex items-center gap-3">
          {onBack ? (
            <button
              type="button"
              onClick={onBack}
              className="flex h-11 w-11 items-center justify-center rounded-xl border border-border bg-card"
              aria-label="Quay lại"
            >
              <ArrowLeft size={20} />
            </button>
          ) : null}
          <div>
            <h1 style={{ fontSize: 20 }} className="text-foreground">Hỗ trợ</h1>
            <p style={{ fontSize: 14 }} className="text-muted-foreground">
              Vị trí gửi yêu cầu: {location}
            </p>
          </div>
        </div>
      </div>

      <div className="mx-4 mt-4 bg-primary rounded-xl p-5">
        <p style={{ fontSize: 13 }} className="text-primary-foreground/80 mb-2">Cần giúp đỡ ngay?</p>
        <button
          type="button"
          onClick={() => handleSupportRequest("staff")}
          disabled={isRequesting}
          className="w-full py-4 rounded-xl bg-white text-primary flex items-center justify-center gap-2 active:scale-[0.98] transition-all"
          style={{ fontSize: 17, minHeight: 56 }}
        >
          <HeadphonesIcon size={20} />
          {isRequesting ? "Đang gửi yêu cầu..." : "Gọi nhân viên hỗ trợ"}
        </button>
        {requestMessage ? (
          <p
            role="status"
            style={{ fontSize: 12 }}
            className="text-primary-foreground bg-white/10 rounded-lg p-2 mt-3"
          >
            {requestMessage}
          </p>
        ) : null}
      </div>

      <div className="mx-4 mt-4 bg-card rounded-xl border border-border overflow-hidden">
        <div className="px-4 py-3 border-b border-border flex items-center gap-2">
          <Accessibility size={16} className="text-primary" />
          <p style={{ fontSize: 14 }} className="text-foreground">Nhu cầu hỗ trợ</p>
        </div>
        <div className="p-4 flex flex-col gap-3">
          {[
            { label: "Hỗ trợ xe lăn", desc: "Yêu cầu nhân viên mang xe lăn đến vị trí hiện tại", type: "wheelchair" as const },
            { label: "Hướng dẫn đường đi", desc: "Yêu cầu nhân viên hướng dẫn đến đúng phòng", type: "directions" as const },
            { label: "Hỗ trợ thị giác", desc: "Yêu cầu hướng dẫn trực tiếp hoặc bản in chữ lớn", type: "visual_assistance" as const },
          ].map((item) => (
            <button
              key={item.type}
              type="button"
              onClick={() => handleSupportRequest(item.type)}
              disabled={isRequesting}
              className="flex items-center gap-3 py-2 text-left w-full"
              style={{ minHeight: 48 }}
            >
              <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                <Accessibility size={15} className="text-primary" />
              </div>
              <div className="flex-1">
                <p style={{ fontSize: 14 }} className="text-foreground">{item.label}</p>
                <p style={{ fontSize: 12 }} className="text-muted-foreground">{item.desc}</p>
              </div>
              <ChevronRight size={16} className="text-muted-foreground" />
            </button>
          ))}
        </div>
      </div>

    </div>
  );
}
