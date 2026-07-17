import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function HospitalMapPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Bản đồ bệnh viện"
      title="Chỉ đường theo bước hiện tại"
      description="Màn hình sản xuất sẽ nhận điểm bắt đầu, điểm đến, tầng và nhu cầu tiếp cận từ hành trình đã xác nhận."
      actions={[{ label: 'Quay lại Hôm nay', to: '/' }]}
    />
  )
}
