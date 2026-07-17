import { useParams } from 'react-router-dom'
import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function TodayJourneyPage() {
  const { journeyId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Hành trình đang thực hiện"
      title={`Hành trình ${journeyId}`}
      description="Trang này sẽ nhận tiến độ từ backend và cập nhật hàng chờ bằng sự kiện máy chủ, không dùng nút hoàn tất mô phỏng."
      actions={[
        { label: 'Xem chỉ đường', to: `/journey/${journeyId}/directions/demo-step` },
        { label: 'Tôi cần hỗ trợ', to: '/support' },
      ]}
    />
  )
}

export function DirectionsPage() {
  const { journeyId = 'unknown', stepId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Chỉ đường"
      title={`Đến bước ${stepId}`}
      description="Bản đồ và hướng dẫn chữ phải cùng dùng một điểm đến động từ hành trình đã xác nhận."
      actions={[{ label: 'Tôi đã đến', to: `/journey/${journeyId}/waiting/${stepId}` }]}
    />
  )
}

export function WaitingPage() {
  const { journeyId = 'unknown', stepId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Hàng chờ"
      title={`Đang chờ tại bước ${stepId}`}
      description="Hiển thị khoảng được gọi, số người phía trước, trạng thái phòng và thời điểm dữ liệu được cập nhật."
      actions={[{ label: 'Về hành trình', to: `/journey/${journeyId}` }]}
    />
  )
}

export function CompletedPage() {
  const { journeyId = 'unknown' } = useParams()

  return (
    <FeaturePlaceholder
      eyebrow="Hoàn tất dịch vụ"
      title={`Đủ kết quả cho hành trình ${journeyId}`}
      description="Hoàn tất dịch vụ và hoàn tất toàn bộ lượt khám là hai trạng thái riêng. Bệnh nhân vẫn cần quay lại bác sĩ."
      actions={[
        { label: 'Chỉ đường quay lại bác sĩ', to: `/journey/${journeyId}/directions/doctor` },
      ]}
    />
  )
}
