import '@testing-library/jest-dom/vitest'
import { render, screen } from '@testing-library/react'
import { RouterProvider, createMemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { NotFoundPage } from '../shared/ui/NotFoundPage'

describe('bộ định tuyến ứng dụng', () => {
  it('hiển thị trang không tìm thấy với đường dẫn về hệ thống giả lập', () => {
    const testRouter = createMemoryRouter([
      { path: '*', element: <NotFoundPage /> },
    ], { initialEntries: ['/duong-dan-khong-ton-tai'] })

    render(<RouterProvider router={testRouter} />)

    expect(screen.getByRole('heading', { name: 'Không tìm thấy màn hình' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Mở hệ thống giả lập' })).toHaveAttribute(
      'href',
      '/demo/simulator',
    )
  })
})
