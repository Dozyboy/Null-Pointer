# QUY TẮC RIÊNG CHO BACKEND

Quy tắc gốc tại `../AGENTS.md` luôn được áp dụng.

- Mỗi nghiệp vụ nằm trong `app/modules/<domain>`.
- Bộ định tuyến chỉ kiểm tra dữ liệu HTTP và gọi service.
- Quy tắc lâm sàng không đặt trong router hoặc repository.
- Mọi thao tác xác nhận, đổi phòng và hỗ trợ phải có thiết kế nhật ký.
- AI chỉ được gọi qua cổng trong `app/intelligence` và bộ chuyển đổi trong `app/integrations/ai`.
- Không nhập trực tiếp mã từ thư mục `ai/src` vào miền nghiệp vụ; hai phần trao đổi qua hợp đồng API.
- Tệp mới phải có kiểm thử tương ứng nếu chứa nghiệp vụ.
