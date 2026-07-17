# QUY TẮC RIÊNG CHO DỊCH VỤ AI

Quy tắc gốc tại `../AGENTS.md` luôn được áp dụng.

- Chỉ nhận ứng viên đã được backend lọc an toàn.
- Không nhận tên bệnh nhân nếu mã tham chiếu ẩn danh là đủ.
- Không tạo, sửa hoặc hủy chỉ định.
- Không ghi trực tiếp cơ sở dữ liệu bệnh viện.
- Chính sách quản trị phải nằm trong `config/governance-policy.yaml`, không viết rải rác.
- Khi chính sách lỗi, phải từ chối xử lý thay vì tự cho phép.
- Mọi thuật toán mới phải có phiên bản, kiểm thử ràng buộc và cách dự phòng.
- Mọi công cụ hoặc nhà cung cấp mô hình mới phải được thêm vào danh sách cho phép trước khi dùng.
