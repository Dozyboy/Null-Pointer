# KIẾN TRÚC HỆ THỐNG NHỊP VIỆN

## 1. Mục tiêu kiến trúc

- Dễ hiểu với nhóm nhỏ và người mới.
- Không trộn giao diện, nghiệp vụ, dữ liệu và AI.
- Có thể thay dữ liệu mô phỏng bằng tích hợp bệnh viện thật theo từng phần.
- Mọi đề xuất AI đều được backend kiểm tra lại.
- Không cần tách thành nhiều dịch vụ phức tạp trong giai đoạn đầu.

## 2. Kiến trúc tổng thể

```text
┌─────────────────────────────┐
│ Frontend React              │
│ Giao diện bệnh nhân         │
└──────────────┬──────────────┘
               │ HTTPS / JSON / SSE
               ▼
┌─────────────────────────────┐
│ Backend FastAPI             │
│ Xác thực, nghiệp vụ, API    │
│ kiểm tra an toàn, nhật ký   │
└───────┬─────────────┬───────┘
        │             │
        ▼             ▼
┌──────────────┐  ┌──────────────────────┐
│ PostgreSQL   │  │ Dịch vụ AI           │
│ Dữ liệu gốc │  │ Đề xuất và dự báo    │
└──────────────┘  └──────────┬───────────┘
                             │
                             ▼
                    Kết quả chỉ là đề xuất
```

**HTTPS – kết nối web có mã hóa** bảo vệ dữ liệu khi truyền.
**JSON – định dạng dữ liệu dạng khóa và giá trị** dùng để frontend, backend và AI trao đổi.
**SSE, Server-Sent Events – luồng sự kiện một chiều từ máy chủ** giúp cập nhật hàng chờ mà không tải lại trang.

## 3. Ranh giới trách nhiệm

### Frontend

- Hiển thị dữ liệu.
- Thu nhận lựa chọn của bệnh nhân.
- Quản lý trạng thái giao diện cục bộ.
- Gọi API và hiển thị đang tải, thành công hoặc lỗi.
- Không tự quyết định phòng nào đủ chuyên môn.
- Không tự đánh dấu dịch vụ hoàn tất.

### Backend

- Là cổng vào duy nhất của frontend.
- Xác thực người dùng và quyền truy cập.
- Kiểm tra chỉ định, ràng buộc, phòng và dữ liệu mới.
- Quản lý giữ chỗ, hành trình và hàng chờ.
- Kiểm tra lại kết quả AI.
- Lưu nhật ký và trạng thái chính thức.

### AI

- Xếp hạng phương án đã hợp lệ.
- Ước lượng khoảng chờ.
- Giải thích yếu tố tạo ra đề xuất bằng dữ liệu đã được cung cấp.
- Không ghi trực tiếp vào cơ sở dữ liệu nghiệp vụ.
- Không tự gọi hệ thống bệnh viện.
- Không tạo kết luận y khoa.

## 4. Kiểu kiến trúc backend

Backend dùng **modular monolith – khối ứng dụng đơn được chia thành mô-đun nghiệp vụ**. Ứng dụng chạy như một FastAPI nhưng mỗi miền có API, kiểu dữ liệu, nghiệp vụ và kho dữ liệu riêng.

```text
API
→ Service / Use case
→ Domain rule
→ Repository interface
→ Database adapter
```

**Use case – ca sử dụng** là một thao tác nghiệp vụ hoàn chỉnh, ví dụ tạo giữ chỗ.
**Repository – lớp truy cập dữ liệu** tách câu lệnh cơ sở dữ liệu khỏi quy tắc nghiệp vụ.
**Adapter – bộ chuyển đổi tích hợp** nối giao diện chung với công nghệ cụ thể như PostgreSQL hoặc HIS.

Các miền:

- `patients`: bệnh nhân và nhu cầu hỗ trợ.
- `encounters`: lượt khám.
- `clinical_orders`: chỉ định.
- `facilities`: phòng, thiết bị và nhân sự.
- `queues`: hàng chờ.
- `routing`: phương án lộ trình.
- `reservations`: giữ chỗ.
- `journeys`: hành trình đã xác nhận.
- `notifications`: thông báo.
- `support`: yêu cầu trợ giúp.
- `audit`: nhật ký quyết định.

## 5. Kiến trúc frontend

Frontend dùng **feature-first – tổ chức theo tính năng**. Mỗi tính năng chứa trang, thành phần, gọi API và trạng thái riêng.

```text
app → features → entities → shared
```

- `app`: lắp ghép toàn ứng dụng, định tuyến và nhà cung cấp trạng thái.
- `features`: trang chủ, tạo tuyến, hành trình, bản đồ, thông báo và hỗ trợ.
- `entities`: kiểu dữ liệu bệnh nhân, lộ trình và hành trình dùng chung.
- `shared`: API client, thành phần giao diện nền, cấu hình và tiện ích.

**React Router – thư viện ánh xạ địa chỉ web với màn hình** thay cho biến điều hướng thủ công.
**TanStack Query – thư viện quản lý dữ liệu lấy từ máy chủ** lưu bộ nhớ đệm, chống gọi lặp và làm mới dữ liệu.
**Zod – thư viện kiểm tra cấu trúc dữ liệu khi ứng dụng đang chạy** ngăn dữ liệu API sai cấu trúc đi sâu vào giao diện.

## 6. Luồng tạo lộ trình

```text
Frontend gửi encounter_id và route_priority
→ Backend đọc chỉ định đã ký
→ Backend lọc phòng và ràng buộc
→ Backend tạo tập ứng viên an toàn
→ AI hoặc bộ quy tắc xếp hạng ứng viên
→ Backend kiểm tra lại toàn bộ kết quả
→ Backend lưu proposal và lý do
→ Frontend hiển thị tối đa ba phương án
```

Nếu AI không phản hồi, backend dùng bộ xếp hạng cố định hoặc báo không thể tạo đề xuất; không được tự bỏ ràng buộc để có kết quả.

## 7. Luồng giữ chỗ

```text
Tạo hold
→ Trả mã và expires_at
→ Bệnh nhân xác nhận
→ Backend khóa nguồn lực liên quan
→ Kiểm tra phiên bản và công suất
→ Tạo journey
→ Xác nhận chỗ mới
→ Giải phóng chỗ cũ
→ Ghi audit log
```

**Transaction – giao dịch cơ sở dữ liệu** là nhóm thao tác phải cùng thành công hoặc cùng được hoàn tác.

## 8. Luồng sự cố

```text
Nhận sự kiện resource.paused
→ Tìm hành trình bị ảnh hưởng
→ Tạo phòng thay thế
→ Kiểm tra an toàn
→ Điều phối viên phê duyệt
→ Giữ tạm chỗ mới
→ Thông báo bệnh nhân
→ Bệnh nhân đồng ý hoặc từ chối
→ Áp dụng hoặc giữ kế hoạch cũ
→ Ghi nhật ký
```

## 9. API chính

Tiền tố: `/api/v1`.

| Nhóm | Endpoint chính |
|---|---|
| Bối cảnh hôm nay | `GET /me/today` |
| Chỉ định | `GET /encounters/{id}/orders` |
| Tạo phương án | `POST /encounters/{id}/route-proposals` |
| Xem phương án | `GET /route-proposals/{id}` |
| Đổi một bước | `POST /route-options/{id}/step-replacements` |
| Giữ chỗ | `POST /route-options/{id}/holds` |
| Xác nhận | `POST /holds/{id}/confirm` |
| Gia hạn | `POST /holds/{id}/extend` |
| Hành trình | `GET /journeys/{id}` |
| Đã đến | `POST /journeys/{id}/steps/{step_id}/arrive` |
| Sự kiện trực tiếp | `GET /journeys/{id}/events` |
| Đổi tuyến | `POST /reroute-proposals/{id}/accept` hoặc `/decline` |
| Thông báo | `GET /notifications` |
| Hỗ trợ | `POST /support-requests` |

## 10. Lưu trữ dữ liệu

Giai đoạn phát triển dùng SQLite nếu cần chạy nhanh; môi trường dùng chung và sản xuất dùng PostgreSQL.

Các bảng chính dự kiến:

- `patients`, `encounters`, `clinical_orders`, `order_constraints`.
- `service_points`, `resources`, `resource_status_events`.
- `queue_entries`, `capacity_snapshots`, `wait_estimates`.
- `route_proposals`, `route_options`, `route_steps`.
- `reservations`, `journeys`, `journey_steps`.
- `reroute_proposals`, `notifications`, `support_requests`.
- `decision_records`, `audit_logs`, `outbox_events`.

**Outbox – hộp sự kiện chờ gửi** giúp không mất thông báo khi dữ liệu đã lưu nhưng hệ thống ngoài tạm thời lỗi.

## 11. Kiểm thử

| Lớp | Nội dung |
|---|---|
| Frontend đơn vị | Thành phần, biểu mẫu, đồng hồ và trạng thái lỗi |
| Frontend tích hợp | Router, API giả lập và luồng người dùng |
| Backend đơn vị | Ràng buộc, giữ chỗ, đổi tuyến và tính trạng thái |
| Backend API | Mã phản hồi, quyền và cấu trúc dữ liệu |
| AI | Phương án vi phạm bị loại, dự báo có giới hạn hợp lệ |
| Hợp đồng | Backend và AI trao đổi đúng cấu trúc |
| Đầu-cuối | Chỉ định → phương án → giữ chỗ → hành trình → quay lại bác sĩ |

## 12. Nguyên tắc mở rộng

- Không tách thêm dịch vụ chỉ vì một thư mục lớn; chỉ tách khi có nhu cầu triển khai, bảo mật hoặc mở rộng độc lập.
- Không để frontend gọi thẳng AI.
- Không để AI gọi thẳng cơ sở dữ liệu bệnh viện.
- Không di chuyển mã nguyên mẫu vào mã sản xuất mà không tách dữ liệu cố định và nút mô phỏng.
- Mọi thay đổi kiến trúc phải cập nhật tài liệu cấu trúc và chạy GitNexus.
