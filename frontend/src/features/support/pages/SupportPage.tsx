import { FeaturePlaceholder } from '../../../shared/ui/FeaturePlaceholder'

export function SupportPage() {
  return (
    <FeaturePlaceholder
      eyebrow="Hỗ trợ"
      title="Yêu cầu nhân viên hỗ trợ"
      description="Yêu cầu sản xuất phải trả mã theo dõi, trạng thái tiếp nhận và thời gian phản hồi dự kiến."
      actions={[{ label: 'Về Hôm nay', to: '/' }]}
    />
  )
}
