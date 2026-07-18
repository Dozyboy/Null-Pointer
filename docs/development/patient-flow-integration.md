# TÍCH HỢP GIAO DIỆN BỆNH NHÂN VỚI BACKEND

## 1. Nguồn giao diện chuẩn

Thư mục `giaodien/` là mốc đối chiếu trực quan, không phải mã chạy. Mã sản xuất nằm trong:

- `frontend/src/features/patient-flow/`: toàn bộ luồng bệnh nhân.
- `frontend/src/features/demo-simulation/`: màn hình máy tính dùng tạo dữ liệu demo.
- `frontend/src/entities/`: hợp đồng bệnh nhân, chỉ định và nhật ký dùng chung.

**API — giao diện lập trình ứng dụng** là hợp đồng để frontend gửi yêu cầu và nhận dữ liệu từ backend.

## 2. Chức năng đã kết nối

| Chức năng | Nguồn backend | Trạng thái |
|---|---|---|
| Quét QR và đọc hồ sơ bệnh nhân | `GET /api/v1/patients/{patient_id}` | Hoạt động, dữ liệu SQLite |
| Nhận chỉ định mới nhất | `GET /api/v1/simulation/patients/{patient_code}/clinical-orders/latest` | Hoạt động, tự tải lại 3 giây/lần |
| Tạo chỉ định từ hệ thống giả lập | `POST /api/v1/simulation/clinical-orders` | Hoạt động, lưu SQLite |
| Chọn bệnh nhân, dịch vụ và phòng phù hợp | Danh mục, phòng và hàng chờ mô phỏng | Hoạt động |
| Tính ba phương án lộ trình | `POST /api/v1/encounters/{encounter_id}/route-proposals` | Hoạt động bằng thuật toán xác định |
| Tính lại phần chưa hoàn thành | `POST .../latest/route-proposals` | Hoạt động theo phòng, hàng chờ và chế độ hiện tại |
| Giữ chỗ, gia hạn và xác nhận | `/api/v1/route-reservations/*` | Hoạt động, chống xác nhận lặp |
| Khôi phục hành trình sau khi tải lại | `GET .../patients/{patient_code}/latest` | Hoạt động, lưu SQLite |
| Bấm “Tôi đã khám xong” | `PATCH .../{reservation_id}/progress` | Hoạt động, có hộp thoại xác nhận |
| Hoạt động hôm nay và thông báo | `GET /api/v1/patients/{patient_code}/activities/today` | Dùng nhật ký thật của thao tác trong hệ thống |
| Gửi yêu cầu nhân viên, xe lăn, chỉ đường | `POST /api/v1/support-requests` | Hoạt động, lưu SQLite |

**SQLite — cơ sở dữ liệu dạng tệp** là nơi backend lưu dữ liệu demo để không mất khi khởi động lại.

## 3. Phần cố ý mô phỏng

- Danh sách bệnh nhân ban đầu là dữ liệu mẫu được nạp vào SQLite.
- Bệnh nhân tạm, sự kiện và đồng hồ của kịch bản “Tiến mô phỏng 5 phút” chỉ nằm trong bộ nhớ tiến trình.
- Bản đồ là sơ đồ minh họa; chưa có định vị trong nhà hoặc sơ đồ từng phòng thật.
- Nút “Tôi đã khám xong” ghi nhận tiến độ do bệnh nhân xác nhận; không thay thế kết quả chuyên môn.
- Thuật toán backend là bộ quy tắc xác định, chưa gọi dịch vụ trong thư mục `ai/`.

## 4. Phần chưa triển khai

- Kết nối HIS/LIS/RIS/PACS thật.
- Nội dung và trạng thái sẵn sàng của kết quả xét nghiệm/chẩn đoán hình ảnh.
- Xác thực người dùng và phân quyền truy cập hồ sơ.
- Thông báo đẩy, SMS và số điện thoại thật của bệnh viện.
- Màn hình nhân viên tiếp nhận và cập nhật trạng thái yêu cầu hỗ trợ.
- Tự động đổi phòng khi có sự cố và quy trình duyệt phương án mới.
- Hàng chờ trực tiếp theo từng bệnh nhân sau khi đã xác nhận lộ trình.

## 5. Quy tắc an toàn

- Frontend không tự thêm chỉ định hoặc phòng.
- Backend loại phòng tạm dừng và kiểm tra đủ dịch vụ bắt buộc trước khi trả lộ trình.
- Không hiển thị câu “kết quả đã sẵn sàng” khi chưa có dữ liệu từ hệ thống chuyên môn.
- Yêu cầu hỗ trợ phải gắn với mã lượt khám và vị trí hiện tại.
