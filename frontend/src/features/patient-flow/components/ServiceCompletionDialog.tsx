import { CheckCircle2, X } from "lucide-react";

interface ServiceCompletionDialogProps {
  destination: string;
  onCancel: () => void;
  onConfirm: () => void;
}

export function ServiceCompletionDialog({
  destination,
  onCancel,
  onConfirm,
}: ServiceCompletionDialogProps) {
  return (
    <div
      className="fixed inset-0 z-50 flex flex-col justify-end bg-black/50"
      style={{ maxWidth: 430, margin: "0 auto" }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="service-completion-title"
      aria-describedby="service-completion-description"
    >
      <div className="rounded-t-2xl bg-card p-5 shadow-xl">
        <div className="mb-4 flex items-start gap-3">
          <div className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full bg-emerald-100">
            <CheckCircle2 size={24} className="text-emerald-600" />
          </div>
          <div className="min-w-0 flex-1">
            <h2 id="service-completion-title" className="text-foreground" style={{ fontSize: 18 }}>
              Xác nhận đã khám xong?
            </h2>
            <p
              id="service-completion-description"
              className="mt-1 text-muted-foreground"
              style={{ fontSize: 14 }}
            >
              Bạn xác nhận đã hoàn thành dịch vụ tại {destination}. Hệ thống sẽ chuyển sang bước tiếp theo trong lịch trình.
            </p>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-muted"
            aria-label="Đóng hộp xác nhận"
          >
            <X size={18} className="text-foreground" />
          </button>
        </div>

        <div className="flex flex-col gap-2">
          <button
            type="button"
            onClick={onConfirm}
            className="w-full rounded-xl bg-primary py-4 text-primary-foreground active:scale-[0.98]"
            style={{ fontSize: 16, minHeight: 52 }}
          >
            Xác nhận đã khám xong
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="w-full rounded-xl border border-border bg-card py-3.5 text-foreground"
            style={{ fontSize: 15, minHeight: 48 }}
          >
            Chưa, quay lại
          </button>
        </div>
      </div>
    </div>
  );
}
