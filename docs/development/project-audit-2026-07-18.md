# BÁO CÁO RÀ SOÁT CHỨC NĂNG VÀ DỮ LIỆU

Ngày rà soát: 18/07/2026.

## 1. Kết luận

Luồng demo chính đã hoạt động xuyên suốt từ hệ thống giả lập đến giao diện bệnh nhân. Các trang giữ chỗ cũ, dữ liệu kết quả giả, thông báo cứng và nút không có hành động đã được xóa hoặc nối với backend.

## 2. Tính năng đang hoạt động

| Tính năng | Dữ liệu | Ghi chú |
|---|---|---|
| Quản lý phòng, trạng thái và số người chờ | SQLite | Trạng thái đã lưu được khôi phục sau khi backend khởi động lại |
| Quản lý danh mục dịch vụ | SQLite | Thêm, sửa, ngừng dùng và kiểm tra phiên bản |
| Danh sách bệnh nhân và liên kết QR | SQLite | QR mở thẳng `/demo/patient/{patientCode}` |
| Gửi chỉ định cho bệnh nhân | SQLite | Chọn bệnh nhân và dịch vụ từ dữ liệu backend |
| Ghép phòng và xếp lộ trình | Trạng thái phòng hiện tại | Loại phòng tạm dừng, xét hàng chờ và thời gian thực hiện |
| Ba chế độ sắp xếp | Thuật toán backend | Cân bằng, làm dịch vụ sớm, gặp bác sĩ chẩn đoán sớm |
| Tính lại lộ trình | Dịch vụ chưa xong và phòng hiện tại | Không tính lại các bước đã hoàn thành |
| Giữ chỗ, gia hạn, xác nhận | SQLite | Có mã chống gửi lặp và hạn giữ chỗ |
| Tiến độ hành trình | SQLite | Có xác nhận trước khi chuyển bước |
| Hoạt động hôm nay | Nhật ký backend | Không còn danh sách thông báo viết cứng |
| Yêu cầu hỗ trợ | SQLite | Trả mã yêu cầu và có API đọc lại |

## 3. Phần vẫn là mô phỏng

| Phần | Mức độ mô phỏng |
|---|---|
| Đồng hồ “Tiến mô phỏng 5 phút” | Chỉ tồn tại trong bộ nhớ; không phải thời gian bệnh viện thật |
| Bệnh nhân `DEMO-BN-*` trong hàng chờ | Dùng để sinh tải phòng; không phải hồ sơ bệnh nhân QR |
| Bản đồ | Sơ đồ SVG minh họa, không có định vị trong nhà |
| Hoàn thành dịch vụ | Do bệnh nhân bấm xác nhận; chưa đối chiếu LIS/RIS/PACS |
| Thuật toán | Bộ quy tắc xác định, chưa phải mô hình học máy |

## 4. Tính năng chưa hoạt động hoặc chưa có

- Adapter HIS, LIS, RIS/PACS và nhắn tin mới chỉ là thư mục trống.
- Dịch vụ `ai/` có API và kiểm thử riêng nhưng backend chưa gọi nó.
- Chưa có nội dung kết quả xét nghiệm hoặc trạng thái sẵn sàng từ hệ thống chuyên môn.
- Chưa có đăng nhập, phân quyền và mã QR có hạn sử dụng.
- Chưa có thông báo đẩy, SMS hoặc số điện thoại bệnh viện đã cấu hình.
- Chưa có giao diện nhân viên xử lý yêu cầu hỗ trợ.
- Chưa tự động chuyển phòng và xin phê duyệt khi thiết bị hỏng.
- Chưa có vị trí thời gian thực và bản đồ tòa nhà thật.

## 5. Phần đã xóa hoặc sửa

- Xóa 13 trang giữ chỗ cũ và `FeaturePlaceholder` không nằm trong luồng router hiện tại.
- Xóa `WaitingScreen`, `RouteChangeProposal` và màn hình hộp thư chỉ định cũ.
- Xóa tab Kết quả giả và dữ liệu lịch trình viết cứng.
- Xóa số điện thoại/SMS mẫu vì chưa có cấu hình bệnh viện thật.
- Xóa nhánh tạo lộ trình có mã lượt khám cố định `TM-2026-00847`.
- Nối các nút xe lăn, hỗ trợ, không tìm thấy phòng và hoàn thành dịch vụ vào hành động thật.
- Tuyến gốc `/` chuyển đến hệ thống giả lập; đường dẫn sai hiển thị trang 404 thay vì màn hình bệnh nhân mẫu.

## 6. Kết quả kiểm thử

| Phần | Kết quả |
|---|---|
| Frontend TypeScript | Đạt |
| Frontend ESLint | Đạt |
| Frontend Vitest | 14/14 bài đạt |
| Frontend build sản xuất | Đạt, không cò cảnh báo gói lớn hơn 500 kB |
| Backend Pytest | 46/46 bài đạt |
| Backend Ruff | Đạt |
| AI Pytest | 4/4 bài đạt |
| AI Ruff | Đạt |
| Playwright Chromium | Luồng gửi chỉ định → mở bệnh nhân → gửi hỗ trợ đã đạt trong lần kiểm tra tích hợp |

Còn một cảnh báo từ thư viện kiểm thử Starlette về việc chuyển từ `httpx` sang `httpx2`; cảnh báo không làm thất bại bài kiểm thử.
