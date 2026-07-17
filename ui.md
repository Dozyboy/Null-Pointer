# UI/UX Specification - MediFlow AI

## 1. Tổng quan vai trò trong hệ thống

MediFlow AI được thiết kế như một **lớp điều phối thông minh** kết nối với các hệ thống bệnh viện đã có sẵn như hệ thống đặt lịch, check-in, HIS/EMR, LIS, RIS/PACS, hệ thống số thứ tự và trạng thái phòng khám/thiết bị.

Hệ thống không thay thế hoàn toàn phần mềm đặt lịch hiện tại. Thay vào đó, MediFlow AI sử dụng dữ liệu lịch hẹn và vận hành để phân tích tải, dự báo thời gian chờ, gợi ý đổi lịch, điều phối luồng bệnh nhân và hỗ trợ bệnh viện ra quyết định theo thời gian thực.

Trong phiên bản MVP/hackathon, hệ thống có 2 role chính:

1. **Customer / Patient / Bệnh nhân**
   - Người sử dụng app/web để theo dõi lịch khám, nhận cảnh báo khung giờ đông, xác nhận đổi lịch, xem lộ trình khám và thời gian chờ.

2. **Admin / Hospital Operator / Quản trị vận hành bệnh viện**
   - Người quản lý dashboard vận hành, theo dõi tải từng khu vực, cấu hình năng lực phục vụ, xử lý cảnh báo và xem đề xuất điều phối từ AI.

## 2. Role Customer - Bệnh nhân

### 2.1. Mục tiêu của Customer

Customer cần có một trải nghiệm đơn giản, rõ ràng và chủ động. Bệnh nhân không cần hiểu thuật toán phía sau, chỉ cần biết:

- Lịch khám hiện tại của mình là khi nào.
- Khung giờ đó có đông hay không.
- Có khung giờ nào tốt hơn để đổi lịch không.
- Khi đến bệnh viện, mình cần đi đâu trước.
- Mình đang ở bước nào trong hành trình khám.
- Còn chờ bao lâu nữa.
- Khi nào cần di chuyển sang khu vực tiếp theo.

### 2.2. Các chức năng chính của Customer

#### 2.2.1. Xem lịch khám đã có

Vì hệ thống đặt lịch đã tồn tại bên ngoài, MediFlow AI chỉ nhận dữ liệu lịch hẹn từ hệ thống đó.

Bệnh nhân có thể xem:

- Ngày khám.
- Giờ khám.
- Chuyên khoa.
- Bác sĩ hoặc phòng khám nếu có.
- Mục đích khám.
- Trạng thái lịch hẹn: sắp tới, cần xác nhận, đã đổi lịch, đã check-in, đã hoàn tất.
- Dự báo mức độ đông tại khung giờ đó.

#### 2.2.2. Nhận cảnh báo khung giờ đông

Khi AI phát hiện lịch hẹn của bệnh nhân nằm trong khung giờ có nguy cơ quá tải, hệ thống gửi thông báo.

Ví dụ thông báo:

> Khung giờ 08:00 - 09:00 tại Khoa Tim mạch đang có lượng bệnh nhân cao. Nếu chuyển sang 10:00, thời gian chờ dự kiến có thể giảm khoảng 25 phút.

Bệnh nhân có thể chọn:

- Đổi sang khung giờ được gợi ý.
- Xem thêm khung giờ khác.
- Giữ lịch hiện tại.

#### 2.2.3. Gợi ý đổi lịch thông minh

MediFlow AI không tự động đổi lịch nếu chưa có sự đồng ý của bệnh nhân.

Hệ thống chỉ gợi ý các khung giờ tốt hơn dựa trên:

- Mật độ bệnh nhân theo khung giờ.
- Năng lực bác sĩ/phòng khám.
- Lịch trống từ hệ thống đặt lịch gốc.
- Dự báo thời gian chờ.
- Dịch vụ cận lâm sàng có thể cần thực hiện trước.

Sau khi bệnh nhân chọn khung giờ mới, MediFlow AI gửi yêu cầu cập nhật về hệ thống đặt lịch hiện có.

#### 2.2.4. Check-in và nhận lộ trình khám

Khi bệnh nhân đến bệnh viện và check-in, hệ thống tạo một hành trình khám cá nhân.

Lộ trình có thể gồm:

- Đến quầy tiếp nhận.
- Gặp bác sĩ.
- Lấy máu.
- Chụp X-quang.
- Siêu âm.
- Chờ kết quả.
- Quay lại phòng khám.
- Thanh toán/nhận thuốc.

Hệ thống hiển thị bước tiếp theo rõ ràng để bệnh nhân không phải tự hỏi hoặc đi nhầm khu vực.

#### 2.2.5. Xem thời gian chờ dự kiến

Ở mỗi bước, bệnh nhân thấy:

- Số người đang chờ trước mình.
- Thời gian chờ dự kiến.
- Thời gian phục vụ dự kiến.
- Trạng thái khu vực: bình thường, hơi đông, quá tải, tạm dừng.
- Thông báo khi gần đến lượt.

#### 2.2.6. Nhận chỉ đường trong bệnh viện

Sau khi AI xác định điểm đến tiếp theo, bệnh nhân được hướng dẫn di chuyển.

MVP có thể hỗ trợ:

- Bản đồ tầng/khu vực.
- Hướng dẫn dạng text: "Đi thẳng 20m, rẽ trái tại thang máy, phòng lấy máu ở bên phải."
- Mã QR tại các vị trí để xác nhận bệnh nhân đang ở đúng khu vực.

Phiên bản mở rộng có thể tích hợp:

- AI Vision để nhận diện vị trí qua ảnh.
- Bluetooth Beacon nếu bệnh viện có hạ tầng.

#### 2.2.7. Theo dõi trạng thái kết quả

Với các dịch vụ như xét nghiệm hoặc chẩn đoán hình ảnh, bệnh nhân có thể xem trạng thái:

- Đã lấy mẫu.
- Đang xử lý.
- Đang chờ bác sĩ đọc kết quả.
- Kết quả đã sẵn sàng.
- Có thể quay lại phòng khám.

Hệ thống không cần hiển thị chi tiết y khoa nếu chưa được bác sĩ xác nhận. Chỉ cần hiển thị trạng thái phục vụ cho điều phối hành trình.

### 2.3. Danh sách màn hình Customer

#### Màn hình 1: Đăng nhập / Xác thực bệnh nhân

Mục đích:

- Cho phép bệnh nhân truy cập hành trình khám cá nhân.

Thành phần chính:

- Nhập số điện thoại/mã bệnh nhân.
- Nhập OTP.
- Chọn hồ sơ bệnh nhân nếu một tài khoản có nhiều người thân.

Luồng hoạt động:

1. Bệnh nhân nhập số điện thoại hoặc mã bệnh nhân.
2. Hệ thống gửi OTP.
3. Bệnh nhân xác thực.
4. Hệ thống tải lịch hẹn và hành trình khám liên quan.

#### Màn hình 2: Trang chủ Customer

Mục đích:

- Hiển thị tổng quan lịch khám và trạng thái hiện tại.

Thành phần chính:

- Thẻ lịch hẹn sắp tới.
- Cảnh báo nếu khung giờ đông.
- Nút xem gợi ý đổi lịch.
- Trạng thái hành trình nếu đã check-in.
- Thông báo gần đây.

Luồng hoạt động:

1. Bệnh nhân mở app.
2. Hệ thống lấy dữ liệu lịch hẹn từ hệ thống đặt lịch.
3. AI phân tích mức độ đông.
4. Nếu lịch hẹn bình thường, hiển thị lịch và thời gian dự kiến.
5. Nếu lịch hẹn đông, hiển thị cảnh báo và đề xuất đổi lịch.

#### Màn hình 3: Chi tiết lịch hẹn

Mục đích:

- Cho bệnh nhân xem thông tin chi tiết về lịch khám hiện tại.

Thành phần chính:

- Ngày, giờ, chuyên khoa, bác sĩ/phòng khám.
- Địa điểm khám.
- Mức độ đông của khung giờ.
- Thời gian chờ dự kiến.
- Các lưu ý trước khi đến bệnh viện.
- Nút xem khung giờ thay thế.

Luồng hoạt động:

1. Bệnh nhân chọn lịch hẹn.
2. Hệ thống hiển thị thông tin lịch hiện tại.
3. AI hiển thị đánh giá tải: thấp, trung bình, cao.
4. Nếu tải cao, hệ thống gợi ý đổi lịch.

#### Màn hình 4: Gợi ý đổi lịch

Mục đích:

- Giúp bệnh nhân chọn khung giờ ít đông hơn.

Thành phần chính:

- Lịch hiện tại.
- Danh sách khung giờ gợi ý.
- Mức độ đông từng khung giờ.
- Thời gian chờ dự kiến từng khung giờ.
- Nút xác nhận đổi lịch.
- Nút giữ lịch cũ.

Luồng hoạt động:

1. Hệ thống nhận lịch hẹn hiện tại.
2. AI phân tích các khung giờ còn trống từ hệ thống đặt lịch gốc.
3. Hệ thống sắp xếp các khung giờ theo mức độ tối ưu.
4. Bệnh nhân chọn một khung giờ.
5. Hệ thống gửi yêu cầu đổi lịch về hệ thống đặt lịch gốc.
6. Nếu thành công, trạng thái lịch được cập nhật.
7. Nếu thất bại, hệ thống thông báo và gợi ý chọn khung giờ khác.

#### Màn hình 5: Check-in

Mục đích:

- Xác nhận bệnh nhân đã đến bệnh viện và bắt đầu hành trình điều phối.

Thành phần chính:

- Mã QR check-in hoặc nút check-in.
- Thông tin lịch hẹn.
- Trạng thái check-in.
- Điểm đến đầu tiên sau check-in.

Luồng hoạt động:

1. Bệnh nhân đến bệnh viện.
2. Bệnh nhân quét QR hoặc check-in tại kiosk/quầy.
3. Hệ thống xác nhận bệnh nhân đã đến.
4. AI tạo lộ trình khám cá nhân dựa trên dữ liệu hiện tại.
5. Bệnh nhân được hướng dẫn đến bước đầu tiên.

#### Màn hình 6: Hành trình khám của tôi

Mục đích:

- Hiển thị toàn bộ lộ trình khám theo từng bước.

Thành phần chính:

- Timeline các bước khám.
- Bước hiện tại.
- Bước tiếp theo.
- Thời gian chờ dự kiến.
- Trạng thái từng bước: chưa bắt đầu, đang chờ, đang thực hiện, đã xong.
- Nút xem chỉ đường.

Luồng hoạt động:

1. Sau check-in, hệ thống tạo timeline.
2. Bệnh nhân xem bước hiện tại.
3. Khi một bước hoàn tất, hệ thống cập nhật bước tiếp theo.
4. Nếu có thay đổi tải hoặc sự cố, AI tính lại lộ trình.
5. Bệnh nhân nhận thông báo thay đổi.

#### Màn hình 7: Chỉ đường đến khu vực tiếp theo

Mục đích:

- Giúp bệnh nhân đi đúng khu vực.

Thành phần chính:

- Tên điểm đến.
- Tầng/khu/phòng.
- Bản đồ đơn giản.
- Hướng dẫn từng bước.
- Mã QR xác nhận vị trí nếu có.

Luồng hoạt động:

1. Bệnh nhân bấm "Xem chỉ đường".
2. Hệ thống hiển thị tuyến đường đến điểm tiếp theo.
3. Bệnh nhân di chuyển.
4. Nếu có QR, bệnh nhân quét tại điểm đến để xác nhận.
5. Hệ thống cập nhật trạng thái đã đến khu vực.

#### Màn hình 8: Thông báo

Mục đích:

- Tập trung các cập nhật quan trọng cho bệnh nhân.

Thành phần chính:

- Cảnh báo khung giờ đông.
- Xác nhận đổi lịch.
- Nhắc check-in.
- Thông báo gần đến lượt.
- Thông báo đổi lộ trình.
- Thông báo kết quả đã sẵn sàng.

Luồng hoạt động:

1. Hệ thống tạo thông báo khi có sự kiện.
2. Bệnh nhân nhận push notification/SMS/Zalo.
3. Bệnh nhân mở app để xem chi tiết.
4. Nếu cần hành động, hệ thống hiển thị nút tương ứng.

### 2.4. Luồng Customer tổng quát

#### Luồng A: Nhận cảnh báo và đổi lịch trước ngày khám

1. Bệnh nhân đã đặt lịch trên hệ thống đặt lịch hiện có.
2. MediFlow AI đồng bộ dữ liệu lịch hẹn.
3. AI phát hiện khung giờ của bệnh nhân có nguy cơ đông.
4. Hệ thống gửi thông báo cho bệnh nhân.
5. Bệnh nhân mở app và xem các khung giờ thay thế.
6. Bệnh nhân chọn khung giờ mới.
7. MediFlow AI gửi yêu cầu cập nhật lịch về hệ thống đặt lịch gốc.
8. Hệ thống xác nhận đổi lịch thành công.
9. Bệnh nhân nhận lịch mới.

#### Luồng B: Giữ lịch cũ

1. Bệnh nhân nhận cảnh báo khung giờ đông.
2. Bệnh nhân chọn giữ lịch cũ.
3. Hệ thống ghi nhận lựa chọn.
4. Trước ngày khám, hệ thống vẫn có thể gửi nhắc nhở đến sớm hơn nếu cần.

#### Luồng C: Check-in và nhận lộ trình khám

1. Bệnh nhân đến bệnh viện.
2. Bệnh nhân check-in.
3. Hệ thống lấy trạng thái thực tế của phòng khám, xét nghiệm và chẩn đoán hình ảnh.
4. AI tạo lộ trình tối ưu.
5. Bệnh nhân nhận bước tiếp theo và thời gian chờ.
6. Khi hoàn thành từng bước, hệ thống cập nhật timeline.
7. Bệnh nhân quay lại bác sĩ khi tất cả kết quả cần thiết đã sẵn sàng.

#### Luồng D: Lộ trình bị thay đổi do sự cố

1. Bệnh nhân đang trong hành trình khám.
2. Một thiết bị bị lỗi hoặc khu vực quá tải.
3. Admin cập nhật trạng thái hoặc hệ thống tự nhận sự kiện.
4. AI tính lại lộ trình.
5. Bệnh nhân nhận thông báo: "Lộ trình của bạn đã được cập nhật."
6. App hiển thị điểm đến mới và thời gian chờ mới.

## 3. Role Admin - Quản trị vận hành bệnh viện

### 3.1. Mục tiêu của Admin

Admin cần có một góc nhìn tổng quan và có khả năng can thiệp vận hành nhanh. Admin không chỉ quản lý tài khoản, mà chủ yếu quản lý trạng thái vận hành của bệnh viện.

Admin cần biết:

- Khu vực nào đang đông.
- Khu vực nào còn trống.
- Phòng khám hoặc thiết bị nào đang quá tải.
- Có bao nhiêu bệnh nhân đang chờ.
- Thời gian chờ trung bình là bao lâu.
- AI đang đề xuất điều phối gì.
- Có sự cố nào cần xử lý ngay không.

### 3.2. Các chức năng chính của Admin

#### 3.2.1. Dashboard tổng quan

Admin xem toàn cảnh vận hành của bệnh viện theo thời gian thực.

Thông tin chính:

- Tổng số bệnh nhân đã check-in.
- Số bệnh nhân đang chờ.
- Số bệnh nhân đang thực hiện dịch vụ.
- Số bệnh nhân đã hoàn tất.
- Thời gian chờ trung bình toàn viện.
- Các khu vực quá tải.
- Các cảnh báo đang mở.

#### 3.2.2. Theo dõi tải từng khoa/phòng

Admin có thể xem trạng thái từng khu vực:

- Phòng khám chuyên khoa.
- Khu lấy máu.
- Khu xét nghiệm.
- Siêu âm.
- X-quang.
- CT.
- MRI.
- Quầy thanh toán.
- Nhà thuốc.

Mỗi khu vực hiển thị:

- Số bệnh nhân đang chờ.
- Thời gian chờ trung bình.
- Công suất hiện tại.
- Số nhân sự/thiết bị đang hoạt động.
- Trạng thái: bình thường, gần quá tải, quá tải, tạm dừng.

#### 3.2.3. Theo dõi trạng thái phòng, thiết bị và nhân sự

Trạng thái phòng, thiết bị và lịch làm việc của bác sĩ được quản lý bởi hệ thống vận hành riêng. Màn hình này không yêu cầu Admin cập nhật thủ công các trạng thái đó.

Hệ thống chỉ đồng bộ và hiển thị các trạng thái liên quan để AI điều phối sử dụng, bao gồm:

- Phòng đang hoạt động hoặc tạm dừng.
- Thiết bị đang hoạt động, lỗi hoặc bảo trì.
- Bác sĩ tạm nghỉ hoặc đổi lịch.

Khi dữ liệu đồng bộ thay đổi, AI tự động tính lại lộ trình cho các bệnh nhân bị ảnh hưởng.

#### 3.2.4. Xem đề xuất điều phối từ AI

AI có thể đề xuất:

- Chuyển một phần bệnh nhân sang phòng cùng chức năng ít đông hơn.
- Gợi ý bệnh nhân đổi lịch trước ngày khám.
- Điều chỉnh thứ tự dịch vụ cho một nhóm bệnh nhân.
- Cảnh báo khu vực sắp quá tải trong 30-60 phút tới.
- Tạm ngừng nhận thêm bệnh nhân vào một khu vực quá tải.

Các đề xuất hợp lệ sẽ được hệ thống tự động áp dụng theo bộ quy tắc điều phối đã cấu hình, không yêu cầu Admin duyệt từng đề xuất.

Admin có thể giám sát các thay đổi đã được áp dụng và chỉ can thiệp trong trường hợp ngoại lệ:

- Tạm dừng tự động áp dụng cho một khu vực hoặc tình huống đặc biệt.
- Điều chỉnh thủ công khi cần ưu tiên nghiệp vụ hoặc chuyên môn.
- Ghi chú lý do khi can thiệp thủ công.
- Xem lịch sử đề xuất, quyết định tự động và các lần can thiệp của Admin.

#### 3.2.5. Quản lý bệnh nhân trong hàng chờ

Admin có thể tìm kiếm và xem trạng thái từng bệnh nhân:

- Thông tin lịch hẹn.
- Trạng thái check-in.
- Bước hiện tại.
- Bước tiếp theo.
- Thời gian chờ dự kiến.
- Lộ trình được AI đề xuất.
- Lịch sử thay đổi lộ trình.

Admin có thể hỗ trợ điều chỉnh thủ công trong các trường hợp đặc biệt.

#### 3.2.6. Cấu hình quy tắc điều phối

Admin cấu hình các thông số nền:

- Thời gian xử lý trung bình của từng dịch vụ.
- Năng lực phục vụ mỗi phòng.
- Số bệnh nhân tối đa mỗi khung giờ.
- Quy tắc ưu tiên: cấp cứu, người cao tuổi, phụ nữ mang thai, trẻ em, người khuyết tật.
- Quy tắc chuyên môn: dịch vụ nào phải làm trước, dịch vụ nào có thể làm song song.
- Thời gian trả kết quả trung bình.

#### 3.2.7. Báo cáo và phân tích

Admin xem báo cáo theo ngày/tuần/tháng:

- Thời gian chờ trung bình.
- Khu vực thường quá tải.
- Tỷ lệ sử dụng thiết bị.
- Số lượt bệnh nhân đổi lịch thành công.
- Số phút chờ giảm được.
- Tỷ lệ đúng hẹn.
- Số lần AI phải tái điều phối.

### 3.3. Danh sách màn hình Admin

#### Màn hình 1: Đăng nhập Admin

Mục đích:

- Bảo vệ quyền truy cập vào dữ liệu vận hành bệnh viện.

Thành phần chính:

- Email/tài khoản nhân viên.
- Mật khẩu.
- OTP hoặc xác thực nội bộ nếu cần.
- Phân quyền: admin tổng, điều phối viên, quản lý khoa.

Luồng hoạt động:

1. Admin đăng nhập.
2. Hệ thống xác thực quyền.
3. Hệ thống điều hướng đến dashboard phù hợp với quyền.

#### Màn hình 2: Dashboard tổng quan bệnh viện

Mục đích:

- Cung cấp góc nhìn nhanh về tình trạng toàn viện.

Thành phần chính:

- KPI tổng: tổng bệnh nhân, đang chờ, đang phục vụ, đã hoàn tất.
- Thời gian chờ trung bình.
- Heatmap mức độ đông theo khu vực.
- Danh sách cảnh báo.
- Biểu đồ tải theo thời gian.
- Đề xuất AI nổi bật.

Luồng hoạt động:

1. Admin mở dashboard.
2. Hệ thống tải dữ liệu thời gian thực.
3. Dashboard hiển thị khu vực bình thường và khu vực có nguy cơ quá tải.
4. Admin chọn một cảnh báo hoặc khu vực để xem chi tiết.

#### Màn hình 3: Quản lý khu vực/khoa phòng

Mục đích:

- Theo dõi và quản lý từng khu vực vận hành.

Thành phần chính:

- Danh sách khoa/phòng.
- Trạng thái từng khu vực.
- Số bệnh nhân chờ.
- Thời gian chờ trung bình.
- Công suất hiện tại.
- Nút xem chi tiết.

Luồng hoạt động:

1. Admin vào màn hình khu vực.
2. Chọn một khoa/phòng.
3. Hệ thống hiển thị hàng chờ, nhân sự, thiết bị và cảnh báo liên quan.
4. Admin có thể cập nhật trạng thái hoặc xem đề xuất điều phối.

#### Màn hình 4: Chi tiết khu vực

Mục đích:

- Quản lý sâu một khoa/phòng cụ thể.

Thành phần chính:

- Tên khu vực.
- Trạng thái hoạt động.
- Danh sách phòng/thiết bị.
- Danh sách bệnh nhân đang chờ.
- Dự báo tải 30-60 phút tới.
- Đề xuất của AI.
- Nút cập nhật trạng thái.

Luồng hoạt động:

1. Admin chọn khu vực, ví dụ X-quang.
2. Hệ thống hiển thị số bệnh nhân chờ và thiết bị đang hoạt động.
3. Nếu khu vực quá tải, AI đề xuất phương án.
4. Admin chấp nhận hoặc chỉnh sửa đề xuất.
5. Hệ thống cập nhật lộ trình cho bệnh nhân bị ảnh hưởng.

#### Màn hình 5: Quản lý thiết bị và phòng

Mục đích:

- Cập nhật trạng thái phòng khám và thiết bị y tế.

Thành phần chính:

- Danh sách thiết bị/phòng.
- Loại thiết bị: siêu âm, X-quang, CT, MRI.
- Trạng thái: hoạt động, tạm dừng, lỗi, bảo trì.
- Công suất xử lý.
- Lịch hoạt động.
- Nút cập nhật trạng thái.

Luồng hoạt động:

1. Admin chọn thiết bị/phòng.
2. Admin cập nhật trạng thái.
3. Nếu chuyển sang lỗi/tạm dừng, hệ thống xác định bệnh nhân bị ảnh hưởng.
4. AI tính lại lộ trình.
5. Admin xem danh sách tác động và xác nhận.

#### Màn hình 6: Hàng chờ bệnh nhân

Mục đích:

- Theo dõi danh sách bệnh nhân trong toàn bộ luồng khám.

Thành phần chính:

- Tìm kiếm bệnh nhân.
- Bộ lọc theo khoa/phòng, trạng thái, mức ưu tiên.
- Danh sách bệnh nhân.
- Bước hiện tại.
- Thời gian chờ.
- Lộ trình tiếp theo.

Luồng hoạt động:

1. Admin mở màn hình hàng chờ.
2. Lọc theo khu vực hoặc trạng thái.
3. Chọn một bệnh nhân.
4. Xem chi tiết hành trình.
5. Nếu cần, admin can thiệp điều phối thủ công.

#### Màn hình 7: Chi tiết bệnh nhân

Mục đích:

- Xem và hỗ trợ một bệnh nhân cụ thể.

Thành phần chính:

- Thông tin lịch hẹn.
- Trạng thái check-in.
- Timeline hành trình.
- Bước hiện tại.
- Bước tiếp theo.
- Thời gian chờ dự kiến.
- Lịch sử thay đổi lộ trình.
- Nút gửi thông báo cho bệnh nhân.
- Nút điều chỉnh lộ trình nếu có quyền.

Luồng hoạt động:

1. Admin tìm bệnh nhân.
2. Hệ thống hiển thị hành trình hiện tại.
3. Admin kiểm tra nguyên nhân chờ lâu nếu có.
4. Admin có thể gửi thông báo hoặc điều chỉnh lộ trình.
5. Bệnh nhân nhận cập nhật trên app/SMS/Zalo.

#### Màn hình 8: Đề xuất AI

Mục đích:

- Tập trung toàn bộ đề xuất điều phối của AI.

Thành phần chính:

- Danh sách đề xuất.
- Loại đề xuất: đổi lịch, chuyển luồng, đổi thứ tự dịch vụ, cảnh báo quá tải.
- Mức độ ảnh hưởng.
- Số bệnh nhân liên quan.
- Lợi ích dự kiến: giảm thời gian chờ, giảm tải khu vực.
- Nút chấp nhận/từ chối/chỉnh sửa.

Luồng hoạt động:

1. AI tạo đề xuất.
2. Admin nhận cảnh báo.
3. Admin mở chi tiết đề xuất.
4. Hệ thống giải thích lý do đề xuất.
5. Admin chấp nhận, từ chối hoặc chỉnh sửa.
6. Nếu chấp nhận, hệ thống cập nhật lộ trình/lịch/thông báo cho bệnh nhân.

#### Màn hình 9: Cấu hình quy tắc

Mục đích:

- Cho phép bệnh viện thiết lập các tham số vận hành.

Thành phần chính:

- Thời gian xử lý trung bình từng dịch vụ.
- Công suất từng phòng.
- Ngưỡng quá tải.
- Quy tắc ưu tiên.
- Quy tắc thứ tự dịch vụ.
- Thời gian trả kết quả.

Luồng hoạt động:

1. Admin vào cấu hình.
2. Cập nhật thông số.
3. Hệ thống kiểm tra hợp lệ.
4. Admin lưu cấu hình.
5. AI sử dụng cấu hình mới cho các lần tính toán tiếp theo.

#### Màn hình 10: Báo cáo

Mục đích:

- Đánh giá hiệu quả vận hành sau một khoảng thời gian.

Thành phần chính:

- Bộ lọc ngày/tuần/tháng.
- Thời gian chờ trung bình.
- Tải từng khoa/phòng.
- Tỷ lệ sử dụng thiết bị.
- Số lượt đổi lịch.
- Số lượt tái điều phối.
- So sánh trước/sau khi dùng AI.

Luồng hoạt động:

1. Admin chọn khoảng thời gian.
2. Hệ thống tổng hợp dữ liệu.
3. Admin xem biểu đồ và bảng thống kê.
4. Admin xuất báo cáo nếu cần.

### 3.4. Luồng Admin tổng quát

#### Luồng A: Theo dõi quá tải theo thời gian thực

1. Admin mở dashboard.
2. Hệ thống hiển thị heatmap tải từng khu vực.
3. Một khu vực chuyển sang trạng thái gần quá tải.
4. AI tạo cảnh báo và đề xuất điều phối.
5. Admin xem chi tiết.
6. Admin chấp nhận đề xuất.
7. Hệ thống cập nhật lộ trình bệnh nhân liên quan.
8. Bệnh nhân nhận thông báo mới.

#### Luồng B: Cập nhật thiết bị bị lỗi

1. Máy X-quang gặp sự cố.
2. Admin vào màn hình thiết bị.
3. Admin chuyển trạng thái máy từ hoạt động sang lỗi.
4. Hệ thống xác định bệnh nhân đang được điều phối tới máy đó.
5. AI tính lại lộ trình hoặc chuyển sang phòng X-quang khác nếu có.
6. Admin xác nhận.
7. Bệnh nhân nhận thông báo thay đổi điểm đến/thời gian chờ.

#### Luồng C: Gợi ý đổi lịch trước ngày khám

1. Hệ thống đồng bộ dữ liệu lịch hẹn ngày mai.
2. AI phát hiện khung 08:00 - 09:00 của Khoa Tim mạch quá đông.
3. Hệ thống tạo đề xuất gửi thông báo đổi lịch cho một nhóm bệnh nhân phù hợp.
4. Admin xem đề xuất.
5. Admin chấp nhận gửi thông báo.
6. Bệnh nhân nhận gợi ý đổi lịch.
7. Những bệnh nhân đồng ý sẽ được cập nhật lịch mới qua hệ thống đặt lịch gốc.

#### Luồng D: Can thiệp thủ công cho bệnh nhân đặc biệt

1. Admin nhận phản ánh một bệnh nhân chờ quá lâu.
2. Admin tìm bệnh nhân trong màn hình hàng chờ.
3. Admin xem timeline và nguyên nhân chờ.
4. Admin kiểm tra đề xuất AI hoặc chọn điều phối thủ công.
5. Hệ thống cập nhật hành trình.
6. Bệnh nhân nhận thông báo mới.

## 4. Phân quyền đề xuất

Trong MVP, có thể chỉ cần 2 role:

- **Customer**: dùng app/web để nhận thông báo, đổi lịch, check-in và theo dõi hành trình.
- **Admin**: quản lý dashboard, cấu hình hệ thống, cập nhật trạng thái và xác nhận đề xuất AI.

Trong phiên bản mở rộng, Admin có thể tách thành:

- **Hospital Manager**: xem báo cáo, cấu hình tổng thể, quản lý toàn viện.
- **Department Operator**: quản lý một khoa/phòng cụ thể.
- **Front Desk Staff**: hỗ trợ check-in và tìm kiếm bệnh nhân.
- **Device Operator**: cập nhật trạng thái thiết bị và hàng chờ thiết bị.

## 5. Luồng dữ liệu tổng quát

### 5.1. Trước khi bệnh nhân đến viện

1. Hệ thống đặt lịch hiện có tạo lịch khám.
2. MediFlow AI đồng bộ dữ liệu lịch.
3. AI dự báo tải theo khung giờ.
4. Nếu khung giờ đông, AI tạo gợi ý đổi lịch.
5. Admin có thể duyệt hoặc hệ thống tự gửi theo cấu hình.
6. Customer nhận thông báo và quyết định đổi hay giữ lịch.
7. Nếu đổi lịch, MediFlow AI gửi yêu cầu cập nhật lại hệ thống đặt lịch gốc.

### 5.2. Khi bệnh nhân đến viện

1. Customer check-in.
2. Hệ thống lấy dữ liệu vận hành thời gian thực.
3. AI tạo lộ trình khám ban đầu.
4. Customer nhận bước tiếp theo.
5. Admin thấy bệnh nhân xuất hiện trong dashboard/hàng chờ.

### 5.3. Trong quá trình khám

1. Customer hoàn thành từng bước.
2. Hệ thống cập nhật trạng thái.
3. AI kiểm tra lại hàng chờ và trạng thái thiết bị.
4. Nếu cần, AI điều chỉnh lộ trình.
5. Customer nhận cập nhật.
6. Admin theo dõi toàn cảnh và xử lý cảnh báo.

### 5.4. Sau khi hoàn tất

1. Customer kết thúc hành trình khám.
2. Hệ thống ghi nhận tổng thời gian thực tế.
3. Dữ liệu được dùng để cải thiện dự báo.
4. Admin xem báo cáo hiệu quả vận hành.

## 6. Gợi ý ưu tiên xây dựng MVP

Nếu thời gian hackathon ngắn, nên ưu tiên các màn hình sau:

### Customer MVP

1. Trang chủ lịch hẹn.
2. Cảnh báo khung giờ đông.
3. Gợi ý đổi lịch.
4. Hành trình khám của tôi.
5. Thời gian chờ dự kiến.

### Admin MVP

1. Dashboard tổng quan.
2. Quản lý tải từng khu vực.
3. Đề xuất AI.
4. Cập nhật trạng thái thiết bị/phòng.
5. Hàng chờ bệnh nhân.

## 7. Kết luận

Với 2 role **Customer** và **Admin**, MediFlow AI có thể thể hiện rõ giá trị của một hệ thống điều phối bệnh viện thông minh.

Customer nhìn thấy lợi ích trực tiếp: biết khi nào nên đi khám, có thể đổi sang khung giờ ít đông, biết phải đi đâu tiếp theo và còn chờ bao lâu.

Admin nhìn thấy lợi ích vận hành: biết khu vực nào đang quá tải, thiết bị nào gặp sự cố, bệnh nhân đang bị kẹt ở đâu và AI đề xuất điều phối như thế nào.

Trong demo hackathon, chỉ cần làm rõ 2 góc nhìn này là hệ thống đã thể hiện đúng trọng tâm đề bài: giảm thời gian chờ, giảm ùn tắc, tăng hiệu suất sử dụng phòng/thiết bị và giúp bệnh nhân chủ động theo dõi hành trình khám bệnh.
