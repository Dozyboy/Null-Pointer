import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function NotificationsPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Thông báo"
      title="Cập nhật hành trình"
      description="Thông báo sẽ được lấy theo tài khoản, có trạng thái đã đọc và liên kết đến đúng hành động cần xử lý."
      actions={[{ label: 'Về Hôm nay', to: '/' }]}
    />
  )
}
