import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function DashboardPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Trang chủ bệnh nhân"
      title="Hành trình hôm nay"
      description="Khung dự án đã sẵn sàng để chuyển từng phần của DashboardScreen từ thư mục giaodien sang kiến trúc theo tính năng. Dữ liệu bệnh nhân phải được tải từ backend thay vì ghi cố định."
      status="ready"
      actions={[
        { label: 'Xem chỉ định mới', to: '/routing/prescription' },
        { label: 'Mở bản đồ', to: '/map' },
      ]}
    />
  )
}
