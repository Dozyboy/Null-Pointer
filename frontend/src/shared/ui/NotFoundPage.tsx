import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <main className="standalone-error">
      <h1>Không tìm thấy màn hình</h1>
      <p>Đường dẫn không tồn tại hoặc màn hình chưa được đăng ký trong bộ định tuyến.</p>
      <Link className="button button--primary" to="/demo/simulator">
        Mở hệ thống giả lập
      </Link>
    </main>
  )
}
