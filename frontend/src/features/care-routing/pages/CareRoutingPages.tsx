import { useParams } from 'react-router-dom'
import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function PrescriptionPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Bước 1/4"
      title="Chỉ định mới"
      description="Hiển thị chỉ định đã ký, điều kiện nhịn ăn và kết quả kiểm tra dữ liệu trước khi tạo lộ trình."
      actions={[
        { label: 'Chọn điều tôi ưu tiên', to: '/routing/priority' },
        { label: 'Nhờ nhân viên hỗ trợ', to: '/support' },
      ]}
    />
  )
}

export function PriorityPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Bước 2/4"
      title="Chọn điều ưu tiên"
      description="Năm tiêu chí chuẩn gồm hệ thống đề xuất, hoàn tất sớm, ít đi bộ, khu chờ ít đông và hỗ trợ di chuyển."
      actions={[{ label: 'Tạo phương án', to: '/routing/options' }]}
    />
  )
}

export function RouteOptionsPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Bước 3/4"
      title="Chọn lộ trình"
      description="So sánh tối đa ba lộ trình đã qua kiểm tra an toàn, kèm thời gian, quãng đường, hàng chờ và lý do."
      actions={[
        { label: 'Xem phương án minh họa', to: '/routing/options/recommended' },
        { label: 'Giữ phương án', to: '/routing/reservation/recommended' },
      ]}
    />
  )
}

export function RouteDetailPage() {
  const { routeId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Bước 4/4"
      title={`Chi tiết lộ trình: ${routeId}`}
      description="Hiển thị dòng thời gian và chỉ cho đổi sang phòng tương đương. Mọi thay đổi phải được backend tính lại trước khi xác nhận."
      actions={[{ label: 'Xác nhận lộ trình', to: `/routing/reservation/${routeId}` }]}
    />
  )
}

export function ReservationPage() {
  const { routeId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Giữ chỗ"
      title={`Xác nhận phương án: ${routeId}`}
      description="Đồng hồ giữ chỗ phải dùng thời gian hết hạn do backend trả về, không dùng bộ đếm độc lập làm nguồn sự thật."
      actions={[{ label: 'Mở hành trình minh họa', to: '/journey/demo-journey' }]}
    />
  )
}
