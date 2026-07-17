import { Link, useRouteError } from 'react-router-dom'

export function NotFoundPage() {
  const error = useRouteError()

  return (
    <main className="standalone-error">
      <h1>Không tìm thấy màn hình</h1>
      <p>Đường dẫn không tồn tại hoặc màn hình chưa được đăng ký trong bộ định tuyến.</p>
      {error instanceof Error && <p className="standalone-error__detail">{error.message}</p>}
      <Link className="button button--primary" to="/">
        Về trang Hôm nay
      </Link>
    </main>
  )
}
