# QUY TẮC RIÊNG CHO FRONTEND

Quy tắc gốc tại `../AGENTS.md` luôn được áp dụng.

- Phụ thuộc chỉ đi theo `app → features → entities → shared`.
- Không nhập tệp nội bộ của một feature từ feature khác.
- Kiểu dữ liệu dùng chung đặt trong `entities`, không đặt trong tệp màn hình.
- Dữ liệu API phải được kiểm tra tại ranh giới bằng Zod hoặc bộ kiểm tra tương đương.
- Không ghi dữ liệu bệnh nhân vào `console.log`.
- Mỗi trang phải có trạng thái đang tải, trống, lỗi và thử lại trước khi xem là hoàn thiện.
- Không sao chép dữ liệu cố định từ `giaodien/` vào mã sản xuất; chỉ dùng trong `mocks/` và phải gắn nhãn minh họa.
- Không đổi đồng thời kiến trúc và thiết kế hình ảnh trong cùng một lần sửa lớn.
