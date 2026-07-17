# QUY TRÌNH GITNEXUS BẮT BUỘC

## 1. Khi nào phải dùng

Phải dùng GitNexus khi:

- Sửa hàm, lớp hoặc phương thức.
- Thêm tính năng mới.
- Đổi API hoặc cấu trúc dữ liệu.
- Di chuyển, tách hoặc đổi tên mã nguồn.
- Sửa lỗi có thể liên quan nhiều mô-đun.

Không bắt buộc dùng khi chỉ sửa Markdown hoặc tài liệu trong `docs/`.

## 2. Trước khi sửa

```powershell
npx gitnexus status
```

Nếu chưa lập chỉ mục hoặc đã cũ:

```powershell
npx gitnexus analyze
```

Tìm luồng liên quan:

```powershell
npx gitnexus query -r Null-Pointer "route reservation confirmation"
```

Xem quan hệ một thành phần:

```powershell
npx gitnexus context -r Null-Pointer ConfirmRoute
```

Kiểm tra phạm vi ảnh hưởng:

```powershell
npx gitnexus impact -r Null-Pointer "Function:path/to/file.py:ConfirmRoute"
```

**Blast radius – phạm vi ảnh hưởng** là các thành phần hoặc luồng có thể hỏng khi một thành phần bị sửa.

## 3. Quy tắc rủi ro

| Mức GitNexus | Hành động |
|---|---|
| LOW | Có thể sửa và chạy kiểm thử liên quan |
| MEDIUM | Đọc thêm luồng gọi và mở rộng kiểm thử |
| HIGH | Báo người phụ trách trước khi sửa |
| CRITICAL | Dừng; chỉ sửa sau khi có kế hoạch và phê duyệt |

## 4. Sau khi sửa

```powershell
npx gitnexus detect-changes -r Null-Pointer --scope unstaged
```

Chạy kiểm thử, sau đó cập nhật chỉ mục:

```powershell
npx gitnexus analyze
npx gitnexus status
```

## 5. Khi thêm tệp hoàn toàn mới

Tệp mới chưa có mã thành phần trong chỉ mục cũ. Vẫn phải:

1. Chạy `status` và `query` để chọn đúng mô-đun.
2. Không tạo thư mục ngoài cấu trúc chuẩn.
3. Sau khi thêm, chạy `detect-changes` và `analyze`.
4. Dùng `context` cho thành phần mới sau khi lập chỉ mục để kiểm tra phụ thuộc.

## 6. Khi công cụ MCP không có

**MCP, Model Context Protocol – giao thức cho phép AI gọi công cụ bên ngoài** có thể chưa được cấu hình trong một số môi trường. Khi đó dùng các lệnh `npx gitnexus` trong tài liệu này; không bỏ qua GitNexus.
