import { expect, test } from '@playwright/test'

test.describe('Luồng mô phỏng đến ứng dụng bệnh nhân', () => {
  test('gửi chỉ định, mở đúng bệnh nhân và lưu yêu cầu hỗ trợ', async ({ page }) => {
    await page.goto('/demo/simulator?tab=orders')

    await expect(
      page.getByRole('heading', { name: 'Nhập chỉ định như dữ liệu từ hệ thống bệnh viện' }),
    ).toBeVisible()
    await expect(page.getByText('HỒ SƠ ĐÃ LƯU TRONG DB')).toBeVisible()

    await page.getByRole('button', { name: 'Thêm mã vào phiếu chỉ định' }).click()
    await page.getByRole('button', { name: /Bắn 1 chỉ định sang ứng dụng bệnh nhân/ }).click()

    await expect(page.getByText('Đã gửi thành công')).toBeVisible()
    await page.getByRole('link', { name: /Mở ứng dụng bệnh nhân/ }).click()

    await expect(page.getByRole('heading', { name: 'Chỉ định mới' })).toBeVisible()
    await page.getByRole('button', { name: 'Nhờ nhân viên hỗ trợ' }).click()

    await expect(page.getByRole('heading', { name: 'Hỗ trợ' })).toBeVisible()
    await page.getByRole('button', { name: 'Gọi nhân viên hỗ trợ' }).click()
    await expect(page.getByText(/Đã lưu yêu cầu SUP-/)).toBeVisible()
  })
})
