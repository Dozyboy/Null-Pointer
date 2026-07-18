# ĐỐI CHIẾU GIAO DIỆN VỚI YÊU CẦU PHÁT TRIỂN

## 1. Nhãn sử dụng

- **HOẠT ĐỘNG**: thao tác đã gọi backend và có kiểm thử.
- **MÔ PHỎNG**: cố ý dùng dữ liệu hoặc quy trình demo, được ghi nhãn rõ.
- **CHƯA CÓ**: chưa được hiển thị như một chức năng đã hoạt động.

**Backend — phần máy chủ xử lý nghiệp vụ** kiểm tra dữ liệu, chạy thuật toán và lưu trạng thái.

## 2. Bảng truy vết hiện tại

| Màn hình | Trạng thái | Nguồn dữ liệu / giới hạn | Yêu cầu |
|---|---|---|---|
| Hệ thống giả lập | HOẠT ĐỘNG | Phòng, hàng chờ, bệnh nhân và chỉ định từ backend | FR-SIM |
| Danh mục cận lâm sàng | HOẠT ĐỘNG | SQLite; thêm, sửa, ngừng dùng | FR-SIM |
| Mở bệnh nhân bằng QR | HOẠT ĐỘNG | Hồ sơ và mã bệnh nhân trong SQLite | FR-HOME |
| Chỉ định mới | HOẠT ĐỘNG | Chỉ hiển thị chỉ định mới nhất do hệ thống giả lập gửi | FR-ORDER |
| Chọn ưu tiên | HOẠT ĐỘNG | Gửi ưu tiên và chiến lược riêng sang backend | FR-PREF |
| Chọn/chi tiết lộ trình | HOẠT ĐỘNG | Phương án từ thuật toán; không cò đổi phòng cục bộ giả | FR-ROUTE, FR-DETAIL |
| Giữ chỗ/xác nhận | HOẠT ĐỘNG | SQLite; có hết hạn, gia hạn và chống gửi lặp | FR-HOLD |
| Lịch trình hôm nay | HOẠT ĐỘNG | Lộ trình và tiến độ đã lưu; thay đổi chế độ sẽ tính lại | FR-JOURNEY |
| Bản đồ/chỉ đường | MÔ PHỎNG | Điểm đến động, nhưng sơ đồ và hướng dẫn chưa phải bản đồ trong nhà thật | FR-MAP |
| Tôi đã khám xong | HOẠT ĐỘNG TRONG DEMO | Có xác nhận, lưu tiến độ; chưa đối chiếu LIS/RIS/PACS | FR-JOURNEY |
| Hoạt động/Thông báo | HOẠT ĐỘNG MỘT PHẦN | Hiển thị nhật ký thật; chưa có đã đọc và thông báo đẩy | FR-NOTIFY |
| Hỗ trợ | HOẠT ĐỘNG MỘT PHẦN | Yêu cầu được lưu; chưa có màn hình nhân viên xử lý | FR-SUPPORT |
| Hoàn tất | HOẠT ĐỘNG | Hiển thị tiến độ đã ghi nhận, không tuyên bố kết quả chuyên môn đã sẵn sàng | FR-COMPLETE |
| Kết quả xét nghiệm | CHƯA CÓ | Chưa có API LIS/RIS/PACS | FR-HOME, FR-NOTIFY |
| Đổi lộ trình tự động khi có sự cố | CHƯA CÓ | Hiện chỉ tính lại khi người dùng đổi chế độ | FR-REROUTE |

## 3. Khoảng trống ưu tiên

1. Kết nối kết quả và trạng thái hoàn tất từ LIS/RIS/PACS.
2. Thêm xác thực, phân quyền và mã truy cập QR có hạn.
3. Thêm giao diện nhân viên xử lý yêu cầu hỗ trợ.
4. Kết nối backend với dịch vụ `ai/` qua bộ kiểm tra an toàn.
5. Tạo quy trình đổi phòng khi sự cố và bảo toàn chỗ cũ.
6. Thay sơ đồ minh họa bằng dữ liệu bản đồ tòa nhà thật.
