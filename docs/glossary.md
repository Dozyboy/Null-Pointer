# BẢNG GIẢI THÍCH THUẬT NGỮ

| Thuật ngữ | Giải thích cơ bản |
|---|---|
| Frontend – phần giao diện phía người dùng | Mã chạy trong trình duyệt và hiển thị màn hình để người dùng thao tác. |
| Backend – phần xử lý phía máy chủ | Mã kiểm tra quyền, thực hiện nghiệp vụ, lưu dữ liệu và cung cấp API. |
| API, Application Programming Interface – giao diện lập trình ứng dụng | Hợp đồng về địa chỉ và dữ liệu để các phần mềm trao đổi với nhau. |
| Endpoint – điểm cuối API | Một địa chỉ API cụ thể, ví dụ `GET /health`. |
| React – thư viện xây dựng giao diện theo thành phần | Cho phép ghép các thành phần nhỏ thành màn hình web. |
| TypeScript – JavaScript có kiểm tra kiểu | Giúp phát hiện dữ liệu sai kiểu trước khi chạy giao diện. |
| FastAPI – khung Python xây dựng API | Tạo API nhanh, kiểm tra dữ liệu và sinh tài liệu API tự động. |
| Pydantic – thư viện kiểm tra dữ liệu Python | Chuyển và xác minh dữ liệu đầu vào, đầu ra theo cấu trúc khai báo. |
| Router – bộ định tuyến | Ánh xạ địa chỉ web hoặc API với trang hay hàm xử lý tương ứng. |
| State – trạng thái | Dữ liệu hiện tại quyết định giao diện hoặc nghiệp vụ đang ở bước nào. |
| Feature-first – tổ chức theo tính năng | Đặt trang, thành phần và API của một tính năng gần nhau. |
| Entity – thực thể nghiệp vụ | Đối tượng có ý nghĩa trong hệ thống như bệnh nhân, lộ trình hoặc hành trình. |
| Shared – phần dùng chung | Mã nền không phụ thuộc một tính năng cụ thể, ví dụ nút và bộ gọi API. |
| Hook – hàm React tái sử dụng logic | Hàm bắt đầu bằng `use`, dùng để chia sẻ xử lý trạng thái hoặc dữ liệu. |
| Provider – thành phần cung cấp dữ liệu chung | Bọc ứng dụng để các thành phần con dùng cùng cấu hình hoặc trạng thái. |
| TanStack Query – thư viện quản lý dữ liệu máy chủ | Lưu bộ nhớ đệm, chống gọi API lặp và làm mới dữ liệu. |
| Zod – thư viện kiểm tra dữ liệu khi chạy | Xác nhận dữ liệu API đúng cấu trúc trước khi giao diện sử dụng. |
| Modular monolith – ứng dụng đơn chia mô-đun | Một backend triển khai chung nhưng mã được tách theo miền nghiệp vụ. |
| Domain – miền nghiệp vụ | Nhóm khái niệm và quy tắc của một phần hệ thống, ví dụ giữ chỗ. |
| Repository – lớp truy cập dữ liệu | Giao diện đọc và ghi dữ liệu, tách khỏi quy tắc nghiệp vụ. |
| Adapter – bộ chuyển đổi tích hợp | Mã nối một giao diện chung với công nghệ hoặc hệ thống cụ thể. |
| Use case – ca sử dụng | Một thao tác nghiệp vụ hoàn chỉnh như xác nhận lộ trình. |
| AI, Artificial Intelligence – trí tuệ nhân tạo | Phần phân tích dữ liệu để dự báo hoặc xếp hạng đề xuất. |
| Model – mô hình | Thuật toán hoặc cấu hình dùng để tạo dự báo hay xếp hạng. |
| Fallback – phương án dự phòng | Cách xử lý an toàn khi thành phần chính bị lỗi. |
| Fail closed – thất bại an toàn | Khi kiểm tra lỗi, hệ thống từ chối hành động thay vì tự cho phép. |
| Governance policy – chính sách quản trị | Danh sách hành động được phép, bị chặn và cần con người duyệt. |
| Audit log – nhật ký kiểm toán | Bản ghi ai đã làm gì, lúc nào và dựa trên dữ liệu nào. |
| YAML – định dạng cấu hình dễ đọc | Tệp văn bản dùng để lưu chính sách và cấu hình theo khóa, giá trị. |
| HTTP/HTTPS – giao thức trao đổi web | HTTPS là HTTP có mã hóa để bảo vệ dữ liệu khi truyền. |
| JSON – định dạng dữ liệu khóa và giá trị | Dạng dữ liệu phổ biến khi API gửi và nhận thông tin. |
| SSE, Server-Sent Events – sự kiện máy chủ gửi | Kết nối một chiều giúp máy chủ cập nhật trình duyệt liên tục. |
| Docker – công cụ đóng gói ứng dụng | Đặt mã và thư viện vào môi trường chạy nhất quán gọi là container. |
| Docker Compose – công cụ chạy nhiều container | Khởi động frontend, backend và AI từ một tệp `compose.yaml`. |
| Build – đóng gói | Chuyển mã nguồn thành phiên bản sẵn sàng chạy hoặc triển khai. |
| Lint – kiểm tra quy tắc mã | Phát hiện lỗi định dạng, nhập sai và mẫu mã không an toàn. |
| Test – kiểm thử | Chạy tình huống tự động để xác nhận mã hoạt động đúng. |
| Migration – thay đổi cấu trúc dữ liệu có phiên bản | Các bước nâng cấp cơ sở dữ liệu từ phiên bản cũ sang mới. |
| GitNexus – công cụ lập bản đồ mã nguồn | Phân tích thành phần, quan hệ, luồng thực thi và phạm vi ảnh hưởng. |
| Impact analysis – phân tích ảnh hưởng | Tìm phần có thể bị hỏng khi một thành phần thay đổi. |
| QR – mã phản hồi nhanh | Mã hình vuông dùng để xác nhận phòng hoặc mở thông tin. |
| SMS – tin nhắn văn bản | Kênh thông báo không yêu cầu điện thoại thông minh. |
| HIS – hệ thống thông tin bệnh viện | Hệ thống quản lý lượt khám và dữ liệu vận hành bệnh viện. |
| LIS – hệ thống thông tin xét nghiệm | Hệ thống quản lý mẫu và kết quả xét nghiệm. |
| RIS/PACS – hệ thống chẩn đoán hình ảnh | Hệ thống quản lý quy trình và ảnh X-quang, CT, MRI. |
