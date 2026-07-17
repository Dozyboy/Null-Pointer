# NHỊP VIỆN

## Hệ thống điều phối hành trình khám bệnh và giảm thời gian chờ

**Đề tài:** Optimizing the care pathway & reducing wait times - Tối ưu hành trình chăm sóc và giảm thời gian chờ

**Đơn vị đề bài:** VNPT IT

**Phiên bản tài liệu:** 1.0

**Ngôn ngữ và bảng mã:** Tiếng Việt có dấu, Unicode UTF-8. Unicode là tiêu chuẩn gán mã thống nhất cho ký tự của nhiều ngôn ngữ. UTF-8 là cách lưu các mã đó trên máy tính để tiếng Việt không bị lỗi dấu.

---

## 1. Tài liệu này dành cho ai?

Tài liệu này dành cho người mới, chưa có kiến thức về:

- Vận hành bệnh viện.
- Trí tuệ nhân tạo.
- Tối ưu hóa.
- Kiến trúc phần mềm.
- Phân tích dữ liệu.
- Thiết kế sản phẩm.

Bạn không cần hiểu hết thuật ngữ ngay từ đầu. Hãy đọc theo thứ tự từ trên xuống.

Quy ước của tài liệu:

- Mỗi thuật ngữ chuyên ngành được dịch sang tiếng Việt và giải thích ở lần xuất hiện đầu tiên hoặc trong bảng thuật ngữ.
- Sau khi đã giải thích, tài liệu ưu tiên dùng tên tiếng Việt để dễ đọc.
- Các con số về hiệu quả chỉ là ví dụ hoặc kết quả mô phỏng. Không được trình bày chúng như số liệu thật của bệnh viện.
- Giải pháp chỉ hỗ trợ điều phối vận hành. Giải pháp không chẩn đoán và không thay bác sĩ quyết định chuyên môn.

---

## 2. Kết luận ngắn gọn

Không nên chỉ làm một ứng dụng xem số thứ tự. Không nên chỉ làm bảng theo dõi. Không nên chỉ dự đoán thời gian chờ.

Nên xây dựng một hệ thống điều phối theo vòng kín:

```text
Nhận dữ liệu
-> Hiểu trạng thái hiện tại
-> Dự báo điểm nghẽn
-> Lọc các phương án an toàn
-> Đề xuất hành động
-> Nhân viên xác nhận
-> Thông báo cho bệnh nhân
-> Đo kết quả
-> Điều chỉnh lại khi có thay đổi
```

Tên giải pháp đề xuất:

### NHỊP VIỆN

**Thông điệp ngắn:** Mỗi phút chờ thành một bước tiến.

Thông điệp trên là khẩu hiệu, không phải lời cam kết rằng mọi phút chờ đều được loại bỏ.

Định vị giải pháp:

> NHỊP VIỆN là một lớp điều phối đặt trên các phần mềm bệnh viện đang có. Hệ thống kết nối lịch hẹn, trạng thái xác nhận bệnh nhân đã đến, phòng khám, xét nghiệm, chẩn đoán hình ảnh và trạng thái nguồn lực để đề xuất bước tiếp theo an toàn, khả dụng và hiệu quả cho từng bệnh nhân.

---

## 3. Bảng thuật ngữ dành cho người mới

Bạn nên đọc bảng này một lần. Không cần học thuộc.

| Thuật ngữ | Dịch và giải thích cơ bản |
|---|---|
| **Care pathway - Hành trình chăm sóc** | Toàn bộ các bước một bệnh nhân phải đi qua, ví dụ đăng ký, khám, xét nghiệm, chụp X-quang, quay lại bác sĩ và nhận thuốc. |
| **Check-in - Xác nhận đã đến** | Thao tác ghi nhận bệnh nhân đã có mặt tại bệnh viện và sẵn sàng bắt đầu lượt khám. |
| **Slot - Khung lịch phục vụ** | Một khoảng thời gian được dành cho một cuộc hẹn hoặc một lượt sử dụng nguồn lực. |
| **Kiosk - Máy tự phục vụ** | Thiết bị đặt tại bệnh viện để bệnh nhân tự xác nhận đã đến, tra cứu trạng thái hoặc in vé mà không cần dùng điện thoại riêng. |
| **Queue - Hàng đợi** | Danh sách người hoặc công việc đang chờ được phục vụ. |
| **Queueing network - Mạng hàng đợi** | Nhiều hàng đợi có liên hệ với nhau. Ví dụ phòng khám tạo chỉ định cho xét nghiệm, sau đó xét nghiệm lại ảnh hưởng thời điểm bệnh nhân quay về phòng khám. |
| **Bottleneck - Điểm nghẽn** | Công đoạn có năng lực thấp hơn nhu cầu, làm chậm toàn bộ hành trình. |
| **Workload - Khối lượng công việc** | Tổng lượng việc còn phải xử lý. Mười ca ngắn có thể có khối lượng thấp hơn ba ca rất phức tạp. |
| **Capacity - Năng lực phục vụ** | Số người hoặc số việc một khoa, phòng, bác sĩ hay thiết bị có thể xử lý trong một khoảng thời gian. |
| **Utilization - Mức sử dụng nguồn lực** | Tỷ lệ thời gian bác sĩ, phòng hoặc thiết bị thực sự bận làm việc. Mức quá cao có thể làm hàng chờ mất ổn định. |
| **Capacity buffer - Phần năng lực dự phòng** | Một phần công suất được giữ trống để xử lý ca cấp cứu, sự cố hoặc thời gian phục vụ kéo dài bất thường. |
| **X-ray hoặc X-quang - Chụp bằng tia X** | Kỹ thuật dùng tia X để tạo hình ảnh bên trong cơ thể, thường dùng cho xương và lồng ngực. |
| **CT, Computed Tomography - Chụp cắt lớp vi tính** | Kỹ thuật dùng nhiều ảnh tia X và máy tính để tạo hình ảnh cắt lớp chi tiết của cơ thể. |
| **MRI, Magnetic Resonance Imaging - Chụp cộng hưởng từ** | Kỹ thuật dùng từ trường và sóng vô tuyến để tạo hình ảnh chi tiết, không dùng tia X. |
| **Triage - Phân loại mức độ khẩn cấp** | Quy trình nhân viên y tế đánh giá ai cần được xử lý trước dựa trên mức nguy hiểm, không dựa đơn thuần vào thời điểm đến. |
| **HIS, Hospital Information System - Hệ thống thông tin bệnh viện** | Phần mềm quản lý bệnh nhân, lượt khám, viện phí, hồ sơ và các hoạt động chung của bệnh viện. |
| **LIS, Laboratory Information System - Hệ thống thông tin xét nghiệm** | Phần mềm quản lý chỉ định xét nghiệm, mẫu bệnh phẩm, quá trình xử lý và kết quả xét nghiệm. |
| **RIS, Radiology Information System - Hệ thống thông tin chẩn đoán hình ảnh** | Phần mềm quản lý lịch, chỉ định và báo cáo của X-quang, CT, MRI, siêu âm và các dịch vụ hình ảnh khác. |
| **PACS, Picture Archiving and Communication System - Hệ thống lưu trữ và truyền hình ảnh y tế** | Hệ thống lưu ảnh X-quang, CT, MRI và cho phép bác sĩ xem ảnh. |
| **HL7 - Chuẩn trao đổi dữ liệu y tế HL7** | Bộ quy tắc giúp các phần mềm y tế trao đổi thông tin với nhau. HL7 phiên bản 2 thường dùng dạng thông điệp trong các bệnh viện cũ. |
| **FHIR, Fast Healthcare Interoperability Resources - Chuẩn tài nguyên liên thông y tế nhanh** | Chuẩn hiện đại biểu diễn dữ liệu y tế thành các tài nguyên như bệnh nhân, lịch hẹn, lượt khám và chỉ định để hệ thống dễ kết nối hơn. |
| **API, Application Programming Interface - Giao diện lập trình ứng dụng** | Cách để hai phần mềm gửi yêu cầu và nhận dữ liệu từ nhau theo quy tắc đã thống nhất. |
| **Adapter - Bộ chuyển đổi kết nối** | Thành phần nhận dữ liệu từ một hệ thống cũ rồi chuyển thành định dạng chung mà NHỊP VIỆN hiểu được. |
| **Event - Sự kiện** | Một việc đã xảy ra, ví dụ bệnh nhân đã được xác nhận có mặt, máy X-quang vừa hỏng hoặc kết quả xét nghiệm đã sẵn sàng. |
| **Event-driven architecture - Kiến trúc hướng sự kiện** | Cách thiết kế hệ thống trong đó mỗi sự kiện mới sẽ kích hoạt việc cập nhật trạng thái và tính toán lại. |
| **Event bus - Kênh truyền sự kiện** | Thành phần trung gian chuyển sự kiện từ hệ thống phát tới các thành phần cần nhận. Có thể hiểu như một bưu điện nội bộ cho dữ liệu. |
| **State machine - Máy trạng thái** | Mô hình liệt kê các trạng thái hợp lệ và cách chuyển giữa chúng. Ví dụ: đã lên kế hoạch, sẵn sàng, đang chờ, đang phục vụ và hoàn tất. |
| **DAG, Directed Acyclic Graph - Đồ thị có hướng không vòng lặp** | Cách biểu diễn các công việc và quan hệ trước sau. Không vòng lặp nghĩa là không thể đi mãi trong một chu trình không có điểm kết thúc. |
| **Prerequisite - Điều kiện tiên quyết** | Điều kiện phải hoàn thành trước khi làm bước khác. Ví dụ phải có chỉ định hợp lệ trước khi chụp X-quang. |
| **Hard constraint - Ràng buộc bắt buộc** | Quy tắc tuyệt đối không được vi phạm, thường liên quan an toàn, chỉ định, nhân lực hoặc khả năng thiết bị. |
| **Soft constraint - Ràng buộc mong muốn** | Quy tắc nên cố gắng đáp ứng nhưng có thể thay đổi nếu cần, ví dụ ưu tiên phòng gần hơn hoặc bác sĩ bệnh nhân mong muốn. |
| **Operations Research - Khoa học tối ưu vận hành** | Nhóm phương pháp toán học giúp chọn phương án tốt trong nhiều lựa chọn có ràng buộc. |
| **Optimization - Tối ưu hóa** | Quá trình tìm phương án tốt nhất hoặc đủ tốt theo mục tiêu đã định, ví dụ giảm thời gian chờ nhưng vẫn giữ an toàn. |
| **Optimizer - Bộ máy tối ưu** | Thành phần phần mềm thực hiện việc so sánh và chọn phương án điều phối. |
| **Heuristic - Phương pháp kinh nghiệm có quy tắc** | Cách tìm phương án tốt nhanh chóng nhưng không cam kết đó là phương án tốt nhất tuyệt đối. Phù hợp khi cần phản ứng trong vài giây. |
| **Rolling horizon - Cửa sổ lập kế hoạch cuốn chiếu** | Hệ thống chỉ lập kế hoạch cho khoảng thời gian gần, sau đó tính lại khi có dữ liệu mới. |
| **Reservation - Giữ chỗ tạm thời** | Khóa tạm một vị trí ở phòng hoặc thiết bị mới trước khi chuyển bệnh nhân, nhằm tránh nhiều người cùng được gửi tới một chỗ. |
| **Freeze window - Khoảng đóng băng kế hoạch** | Khoảng thời gian ngay trước lượt phục vụ mà hệ thống không được tự ý đổi kế hoạch để tránh gây hỗn loạn. |
| **Hysteresis - Ngưỡng chống dao động** | Chỉ đổi phương án khi lợi ích mới đủ lớn. Cơ chế này tránh việc bệnh nhân bị chuyển qua lại vì chênh lệch vài phút. |
| **ETA, Estimated Time of Arrival hoặc Estimated Time to Service - Thời gian dự kiến được phục vụ** | Khoảng thời gian hệ thống dự báo bệnh nhân sẽ được gọi hoặc hoàn tất một bước. Trong đề tài này nên hiểu là thời gian dự kiến được phục vụ. |
| **P50 - Mốc dự báo 50 phần trăm** | Nếu dự báo đúng, khoảng một nửa trường hợp sẽ hoàn tất trước mốc này và một nửa hoàn tất sau mốc này. Có thể hiểu gần giống giá trị trung vị. |
| **P90 - Mốc dự báo 90 phần trăm** | Nếu dự báo được hiệu chỉnh tốt, khoảng 90 phần trăm trường hợp sẽ hoàn tất trước mốc này. Mốc này giúp thể hiện trường hợp chậm hơn bình thường. |
| **TAT, Turnaround Time - Thời gian trả kết quả** | Thời gian từ lúc nhận mẫu hoặc bắt đầu dịch vụ đến khi kết quả sẵn sàng. |
| **SLA, Service Level Agreement - Mức cam kết dịch vụ** | Mốc thời gian hoặc chất lượng mà đơn vị đặt mục tiêu phải đáp ứng, ví dụ 90 phần trăm bệnh nhân được gọi trong 30 phút. |
| **Digital twin - Bản sao số** | Mô hình số liên tục đồng bộ với trạng thái thực tế để mô phỏng, dự báo và kiểm tra phương án. Một mô phỏng dùng dữ liệu giả chưa được gọi là bản sao số hoàn chỉnh. |
| **Discrete-event simulation - Mô phỏng sự kiện rời rạc** | Mô phỏng hệ thống bằng các sự kiện xảy ra tại từng thời điểm, ví dụ bệnh nhân đến, bắt đầu khám, hoàn tất xét nghiệm hoặc máy hỏng. |
| **Baseline - Phương án đối chứng** | Cách vận hành hiện tại hoặc một quy tắc đơn giản dùng để so sánh với giải pháp mới. |
| **FIFO, First In First Out - Đến trước phục vụ trước** | Quy tắc người đến trước được phục vụ trước. Quy tắc này đơn giản nhưng không đủ an toàn nếu bỏ qua ưu tiên lâm sàng. |
| **FCFS, First Come First Served - Đến trước được phục vụ trước** | Cách gọi khác của quy tắc FIFO trong bài toán hàng đợi. |
| **Random seed - Hạt giống ngẫu nhiên** | Con số dùng để tạo lại cùng một chuỗi dữ liệu ngẫu nhiên. Nó giúp các phương án được so sánh công bằng trên cùng tình huống. |
| **Confidence interval - Khoảng tin cậy** | Khoảng thể hiện mức không chắc chắn của kết quả đo. Khoảng càng hẹp thì kết quả thường càng ổn định. |
| **MAE, Mean Absolute Error - Sai số tuyệt đối trung bình** | Trung bình độ lệch tuyệt đối giữa thời gian dự báo và thời gian thực tế. Ví dụ dự báo sai 8 phút trung bình. |
| **Calibration - Độ hiệu chỉnh của dự báo** | Mức độ lời dự báo phù hợp với thực tế. Ví dụ mốc P90 tốt cần bao phủ gần 90 phần trăm trường hợp. |
| **KPI, Key Performance Indicator - Chỉ số hiệu quả chính** | Số đo dùng để biết giải pháp có đạt mục tiêu hay không. |
| **MVP, Minimum Viable Product - Sản phẩm khả dụng tối thiểu** | Phiên bản nhỏ nhất có đủ chức năng cốt lõi để chứng minh ý tưởng hoạt động. |
| **Human in the loop - Con người tham gia vòng quyết định** | Cơ chế yêu cầu nhân viên xem, xác nhận hoặc từ chối đề xuất trước khi hành động có rủi ro được thực hiện. |
| **Audit log - Nhật ký kiểm toán** | Bản ghi ai đã xem, đề xuất, phê duyệt hoặc thay đổi điều gì và vào thời điểm nào. |
| **RBAC, Role-Based Access Control - Kiểm soát truy cập theo vai trò** | Mỗi người chỉ được xem và làm những việc phù hợp với vai trò của mình, ví dụ nhân viên vận chuyển không cần xem toàn bộ bệnh án. |
| **Stale data - Dữ liệu quá hạn** | Dữ liệu đã quá cũ nên không còn đủ tin cậy để ra quyết định. |
| **Fallback - Phương án dự phòng** | Cách vận hành thay thế khi bộ máy tối ưu hoặc dữ liệu gặp lỗi. |
| **Fail-safe - Chuyển về trạng thái an toàn khi lỗi** | Khi không chắc chắn, hệ thống giảm tự động hóa hoặc dừng đề xuất thay vì tiếp tục bằng dữ liệu đáng ngờ. |
| **Idempotency - Tính xử lý lặp không gây tác dụng phụ** | Cùng một sự kiện được gửi lại nhiều lần nhưng hệ thống chỉ ghi nhận tác động một lần. |
| **Reconciliation - Đối soát dữ liệu** | So sánh dữ liệu giữa các hệ thống để tìm sự kiện bị thiếu, trùng hoặc sai trạng thái. |
| **PWA, Progressive Web App - Ứng dụng web có khả năng hoạt động gần giống ứng dụng điện thoại** | Người dùng mở bằng đường liên kết, có thể nhận thông báo và không nhất thiết phải cài từ kho ứng dụng. |
| **SSE, Server-Sent Events - Cơ chế máy chủ gửi cập nhật liên tục tới trình duyệt** | Máy chủ chủ động đẩy trạng thái mới tới màn hình mà người dùng không cần bấm tải lại. |
| **Python - Ngôn ngữ lập trình Python** | Ngôn ngữ dùng để viết phần mềm, phổ biến trong xử lý dữ liệu, mô phỏng và trí tuệ nhân tạo. |
| **Web - Môi trường trang mạng** | Cách cung cấp giao diện qua trình duyệt như Chrome, Edge hoặc Safari mà người dùng không nhất thiết phải cài ứng dụng riêng. |

---

## 4. Hiểu đề bài bằng một ví dụ đơn giản

Một bệnh nhân cần:

1. Gặp bác sĩ.
2. Lấy máu.
3. Chụp X-quang.
4. Siêu âm.
5. Quay lại gặp bác sĩ khi có đủ kết quả.

### Cách vận hành chưa tốt

```text
Bệnh nhân tự hỏi từng quầy
-> Xếp hàng lấy máu
-> Ngồi chờ kết quả máu dù chưa cần ngồi yên
-> Xếp hàng X-quang
-> Xếp hàng siêu âm
-> Quay lại bác sĩ khi kết quả chưa đủ
-> Tiếp tục chờ
```

Vấn đề:

- Bệnh nhân không biết bước nào nên làm trước.
- Mỗi khoa chỉ biết hàng đợi của mình.
- Không ai nhìn thấy toàn bộ hành trình.
- Thời gian xử lý mẫu máu không được tận dụng.
- Bệnh nhân phải quay lại nhiều lần.

### Cách NHỊP VIỆN đề xuất

```text
08:30  Lấy máu
08:38  Mẫu máu bắt đầu được xử lý
08:40  Bệnh nhân đi tới khu X-quang
08:55  Hoàn tất X-quang
09:00  Thực hiện siêu âm
09:25  Các kết quả bắt buộc gần hoàn tất
09:35  Bệnh nhân quay lại bác sĩ
```

Điểm quan trọng:

- Hệ thống không thay đổi chỉ định của bác sĩ.
- Hệ thống chỉ sắp xếp lại các bước được phép đổi thứ tự.
- Mọi điều kiện an toàn phải được kiểm tra trước.
- Nếu dữ liệu không đủ tin cậy, hệ thống chuyển cho nhân viên xử lý.

---

## 5. Bản chất thật của bài toán

### 5.1. Đây không phải một hàng đợi

Bệnh viện là mạng nhiều hàng đợi liên kết:

```text
Lịch hẹn
-> Tiếp nhận
-> Phòng khám
-> Xét nghiệm
-> Chẩn đoán hình ảnh
-> Trả kết quả
-> Tái khám
-> Thanh toán
-> Nhà thuốc
```

Nếu chỉ làm phòng khám nhanh hơn, bệnh nhân có thể bị dồn sang xét nghiệm. Điểm nghẽn chỉ bị chuyển chỗ, không biến mất.

### 5.2. Tối ưu từng khoa có thể làm toàn hệ thống tệ hơn

Ví dụ:

- Khoa khám gọi thật nhanh nhiều bệnh nhân.
- Tất cả bệnh nhân cùng được chỉ định xét nghiệm.
- Khu xét nghiệm quá tải.
- Bệnh nhân chờ lâu hơn dù phòng khám có vẻ hoạt động tốt.

Vì vậy cần tối ưu toàn hành trình, không tối ưu một quầy riêng lẻ.

### 5.3. Đếm số người là chưa đủ

Một hàng có ba ca phức tạp có thể lâu hơn hàng có tám ca đơn giản.

Thời gian dự báo phải xét:

- Loại dịch vụ.
- Thời gian phục vụ dự kiến.
- Công việc của ca đang được phục vụ.
- Số bác sĩ hoặc thiết bị đang hoạt động.
- Thời gian vệ sinh và chuẩn bị máy.
- Ca ưu tiên đang chờ.
- Thiết bị tạm dừng.
- Kết quả còn đang xử lý.

### 5.4. Mức sử dụng 100 phần trăm không phải mục tiêu tốt

Khi bác sĩ hoặc thiết bị luôn kín lịch:

- Không còn chỗ cho ca cấp cứu.
- Một ca kéo dài sẽ làm chậm toàn bộ ca sau.
- Nhân viên dễ phải làm thêm giờ.
- Hàng chờ tăng nhanh.

Mục tiêu đúng là mức sử dụng hữu ích nhưng vẫn có phần năng lực dự phòng.

---

## 6. Mục tiêu và phạm vi

### 6.1. Mục tiêu chính

1. Giảm tổng thời gian bệnh nhân ở bệnh viện.
2. Giảm thời gian chờ không tạo giá trị.
3. Giảm số lần đi sai khu vực hoặc quay lại.
4. Giảm số người tập trung tại khu chờ.
5. Cân bằng tải giữa các phòng và thiết bị tương đương.
6. Cung cấp thời gian dự kiến minh bạch.
7. Giúp nhân viên xử lý sự cố theo thời gian gần thực.
8. Không làm xấu đi an toàn, công bằng hoặc quyền riêng tư.

### 6.2. Những việc không thuộc phạm vi

NHỊP VIỆN không được:

- Chẩn đoán bệnh.
- Tự tạo hoặc hủy chỉ định.
- Tự thay đổi mức ưu tiên lâm sàng.
- Tự bỏ qua điều kiện nhịn ăn hoặc chống chỉ định.
- Tự cho bệnh nhân xuất viện.
- Trì hoãn cấp cứu để làm đẹp chỉ số.
- Ưu tiên bệnh nhân dựa trên khả năng chi trả.
- Thay thế phần mềm bệnh viện hiện có.

---

## 7. Các ý tưởng đổi mới

| Ý tưởng | Giải thích đơn giản | Giá trị chính | Nên làm khi nào? |
|---|---|---|---|
| **Bộ biên dịch hành trình** | Chuyển danh sách chỉ định thành đồ thị trước sau, sau đó chọn bước hợp lệ tiếp theo | Giảm chờ và đi lại | Chức năng cốt lõi |
| **Bộ mô phỏng luồng bệnh nhân** | Chạy thử dòng bệnh nhân và sự cố trên máy tính | Chứng minh hiệu quả trước khi triển khai | Chức năng cốt lõi |
| **Hàng đợi kéo bệnh nhân sẵn sàng** | Phòng đang rảnh gọi người đã đủ điều kiện thay vì chỉ nhìn thứ tự đến | Giảm thời gian phòng hoặc máy bị trống | Chức năng cốt lõi |
| **Làn sóng lịch hẹn xanh** | Dự báo tải ngày mai và đề xuất dời giờ đến tự nguyện | Giảm dồn bệnh nhân đầu buổi | Giai đoạn sau |
| **Chuẩn bị song song** | Bệnh nhân hoàn tất giấy tờ, sinh hiệu hoặc hướng dẫn trong lúc chờ | Biến chờ thành tiến triển | Có thể làm sớm |
| **Kiểm tra trước 24 giờ** | Kiểm tra giấy tờ, nhịn ăn và hướng dẫn trước ngày khám | Tránh thiếu điều kiện khi đã tới viện | Có thể làm sớm |
| **Chờ ở nơi phù hợp** | Cho phép bệnh nhân rời khu chờ và quay lại trước một giờ an toàn | Giảm đông và giảm căng thẳng | Giai đoạn sau |
| **Cứu khung lịch bị bỏ trống** | Mời bệnh nhân tự nguyện nhận chỗ vừa bị hủy | Tăng sử dụng lịch trống | Giai đoạn sau |
| **Bộ bảo vệ công bằng** | Giới hạn chờ tối đa và chống bỏ quên ca dài hoặc người khó di chuyển | Giữ công bằng | Bắt buộc |
| **Hợp đồng thời gian dự kiến** | Hiển thị khoảng thời gian, độ tin cậy và lý do thay đổi | Tăng niềm tin | Bắt buộc |
| **Kịch bản xử lý quá tải** | Khi vượt ngưỡng, đề xuất một kịch bản đã được duyệt trước | Phản ứng nhanh | Có thể làm sớm |
| **Dịch vụ đi tới bệnh nhân** | Thực hiện một số bước đơn giản ngay tại khu chờ | Giảm di chuyển | Giai đoạn sau |

Ba ý tưởng nên hợp nhất thành giải pháp chính:

1. Bộ biên dịch hành trình.
2. Bộ mô phỏng luồng bệnh nhân.
3. Hàng đợi kéo bệnh nhân sẵn sàng.

---

## 8. Cơ chế hoạt động của NHỊP VIỆN

### Bước 1: Nhận dữ liệu

Hệ thống nhận thông tin từ:

- Lịch hẹn.
- Check-in, nghĩa là xác nhận bệnh nhân đã đến.
- Phòng khám.
- Hệ thống xét nghiệm.
- Hệ thống chẩn đoán hình ảnh.
- Trạng thái bác sĩ, phòng và thiết bị.
- Thao tác xác nhận của nhân viên.

### Bước 2: Tạo hành trình

Mỗi dịch vụ là một công việc.

Mỗi công việc có:

| Trường thông tin | Ý nghĩa |
|---|---|
| Mã công việc | Mã duy nhất để phân biệt |
| Loại dịch vụ | Khám, lấy mẫu, X-quang, siêu âm hoặc bước khác |
| Điều kiện tiên quyết | Những việc phải hoàn tất trước |
| Nguồn lực yêu cầu | Bác sĩ, phòng hoặc thiết bị phù hợp |
| Trạng thái | Đã lên kế hoạch, sẵn sàng, đang chờ, đang làm hoặc hoàn tất |
| Mức ưu tiên | Lấy từ quy trình lâm sàng đã được phê duyệt |
| Thời hạn | Thời điểm không nên bị trễ |
| Thời gian dự kiến | Khoảng thời gian chờ và thực hiện |
| Lý do bị chặn | Thiếu chỉ định, thiếu giấy tờ, máy hỏng hoặc lý do khác |

### Bước 3: Xác định công việc sẵn sàng

Một công việc chỉ được đánh dấu sẵn sàng khi:

- Có chỉ định hợp lệ.
- Bệnh nhân đã có mặt.
- Các bước bắt buộc trước đó đã hoàn tất.
- Điều kiện an toàn đã được xác nhận.
- Có loại nguồn lực phù hợp.
- Dữ liệu nguồn chưa quá hạn.

### Bước 4: Lọc phương án không an toàn

Các phương án sau phải bị loại:

- Thiết bị đang hỏng.
- Phòng không có đúng chức năng.
- Bệnh nhân chưa đủ điều kiện chuẩn bị.
- Bệnh nhân đang được phục vụ ở nơi khác.
- Dữ liệu không xác định hoặc mâu thuẫn.
- Lệnh dịch vụ đã bị hủy.
- Bệnh nhân thuộc nhóm cần cách ly nhưng nơi đến không phù hợp.

### Bước 5: Chấm điểm phương án còn lại

Công thức khái niệm:

```text
Điểm chi phí
= thời gian chờ dự kiến
+ thời gian thực hiện
+ thời gian còn lại của toàn hành trình
+ thời gian di chuyển
+ rủi ro trễ thời hạn
+ chi phí do thay đổi kế hoạch
```

Phương án có điểm chi phí thấp hơn thường được ưu tiên, nhưng chỉ sau khi đã đáp ứng an toàn và ưu tiên lâm sàng.

### Bước 6: Giữ chỗ và đề xuất

Trước khi đề xuất đổi tuyến:

1. Kiểm tra lại trạng thái nơi đến.
2. Giữ một chỗ tạm thời.
3. Tính lợi ích dự kiến.
4. Hiển thị lý do cho nhân viên.
5. Chờ xác nhận nếu hành động cần người duyệt.

### Bước 7: Thông báo

Sau khi kế hoạch được xác nhận:

- Cập nhật màn hình bệnh nhân.
- Gửi thông báo ứng dụng hoặc tin nhắn nếu được đồng ý.
- Cập nhật bảng điều phối.
- Cập nhật danh sách chờ tại khoa nhận.

### Bước 8: Đo và tính lại

Mỗi sự kiện mới có thể làm hệ thống tính lại:

- Ca cấp cứu xuất hiện.
- Máy hỏng.
- Bác sĩ đến muộn.
- Một ca kéo dài hơn dự kiến.
- Bệnh nhân đến trễ.
- Kết quả xét nghiệm chậm.
- Nơi đến từ chối tiếp nhận.

---

## 9. Thứ tự ưu tiên bắt buộc

Không nên cộng tất cả mục tiêu thành một điểm duy nhất rồi để máy tự cân bằng tùy ý.

Nên dùng thứ tự phân cấp:

1. An toàn.
2. Ca cấp cứu và mức ưu tiên lâm sàng.
3. Điều kiện có thời hạn như nhịn ăn hoặc mẫu bệnh phẩm.
4. Chống bệnh nhân bị chờ quá lâu.
5. Giảm thời gian hoàn tất toàn hành trình.
6. Giảm di chuyển.
7. Cân bằng nguồn lực.
8. Hạn chế thay đổi kế hoạch đã thông báo.

Điều này có nghĩa:

- Không được làm bệnh nhân cấp cứu chờ để giảm thời gian trung bình.
- Không được trì hoãn ca dài mãi chỉ vì các ca ngắn giúp tăng số lượng hoàn tất.
- Không được chuyển bệnh nhân nhiều lần chỉ để tiết kiệm vài phút.

---

## 10. Phối hợp lịch hẹn

### 10.1. Vấn đề

Lịch hẹn thường chỉ nhìn vào lịch bác sĩ. Nó chưa nhìn thấy:

- Năng lực tiếp nhận.
- Năng lực xét nghiệm.
- Năng lực chẩn đoán hình ảnh.
- Số bệnh nhân không hẹn trước.
- Khả năng có ca cấp cứu.

### 10.2. Giải pháp

Mỗi khung giờ cần xét tải của toàn hành trình.

Ví dụ:

- 08:00 có nhiều bác sĩ rảnh nhưng khu xét nghiệm đã dự kiến quá tải.
- 09:00 số bác sĩ ít hơn nhưng xét nghiệm và X-quang còn năng lực.
- Hệ thống có thể đề xuất một số bệnh nhân linh hoạt tới lúc 09:00.

### 10.3. Quy tắc an toàn

- Việc đổi giờ cần bệnh nhân đồng ý.
- Không làm mất quyền lợi nếu bệnh nhân từ chối.
- Giữ phần năng lực dự phòng cho ca khẩn và ca kéo dài.
- Không đặt lịch vượt quá khả năng của bước phía sau.

---

## 11. Định tuyến bệnh nhân

Định tuyến ở đây nghĩa là chọn đúng khu vực phục vụ trong số các nơi đã được xác nhận phù hợp.

Hệ thống không được tự suy đoán chẩn đoán từ triệu chứng rồi gửi bệnh nhân tới khoa.

Quy trình đúng:

1. Nhân viên y tế hoặc quy trình phân loại đã phê duyệt xác định mức ưu tiên.
2. Hệ thống tìm các địa điểm đủ năng lực chuyên môn.
3. Loại các địa điểm không an toàn hoặc dữ liệu quá hạn.
4. So sánh thời gian chờ, thời gian đi bộ và ảnh hưởng toàn hành trình.
5. Đề xuất phương án.
6. Giữ chỗ trước khi giải phóng chỗ cũ.

---

## 12. Dự báo thời gian chờ

### 12.1. Không nên chỉ đếm số người

Ví dụ:

- Phía trước có hai bệnh nhân, mỗi người cần 30 phút.
- Một hàng khác có năm bệnh nhân, mỗi người cần 5 phút.
- Hàng năm người có thể nhanh hơn hàng hai người.

### 12.2. Dữ liệu cần dùng

- Khối lượng công việc phía trước.
- Thời gian còn lại của ca đang phục vụ.
- Số nguồn lực hoạt động song song.
- Thời gian chuẩn bị và vệ sinh.
- Trạng thái tạm dừng.
- Mức ưu tiên của người chờ.
- Thời gian trả kết quả.
- Độ mới của dữ liệu.

### 12.3. Cách hiển thị

Không nên hiển thị:

> Bạn sẽ được gọi chính xác lúc 10:23.

Nên hiển thị:

> Bạn dự kiến được gọi từ 10:20 đến 10:35. Cập nhật lúc 10:01. Bạn vẫn được giữ lượt.

Nếu chưa đủ dữ liệu:

> Hiện chưa thể ước tính đáng tin cậy. Bạn vẫn đang trong hàng chờ. Hệ thống sẽ cập nhật lại trước 10:25.

---

## 13. Sắp xếp chuỗi dịch vụ

Hệ thống cần phân biệt ba loại quan hệ:

| Quan hệ | Ví dụ | Cách xử lý |
|---|---|---|
| Bắt buộc trước sau | Phải có chỉ định trước khi chụp | Không được đổi |
| Có thể thực hiện độc lập | X-quang có thể thực hiện khi mẫu máu đang xử lý | Có thể đổi thứ tự |
| Phải chờ nhiều kết quả | Tái khám cần cả xét nghiệm và báo cáo hình ảnh | Chỉ quay lại khi đủ kết quả bắt buộc |

Mục tiêu là giảm khoảng thời gian bệnh nhân không làm gì nhưng vẫn phải ở bệnh viện.

---

## 14. Điều chỉnh theo thời gian gần thực

### 14.1. Các sự kiện kích hoạt

- Khoa quá tải.
- Thiết bị hỏng.
- Bác sĩ đổi lịch.
- Ca cấp cứu tới.
- Kết quả bị chậm.
- Bệnh nhân bỏ lỡ lời gọi.
- Nhân viên từ chối đề xuất.

### 14.2. Cách tránh điều phối hỗn loạn

- Không đổi những lượt sắp được gọi.
- Không đổi khi lợi ích quá nhỏ.
- Giới hạn số lần đổi mỗi bệnh nhân.
- Giữ chỗ ở nơi mới trước.
- Gộp các thay đổi nhỏ trước khi gửi thông báo.
- Phạt điểm các phương án làm kế hoạch dao động.

---

## 15. Kiến trúc hệ thống

Sơ đồ đơn giản:

```text
Ứng dụng bệnh nhân / Tin nhắn / Kiosk / Màn hình công cộng
                            |
                    Cổng giao tiếp dữ liệu
                            |
                  Lõi điều phối NHỊP VIỆN
      -------------------------------------------------
      | Hành trình | An toàn | Hàng đợi | Dự báo      |
      | Nguồn lực  | Tối ưu  | Thông báo | Kiểm toán |
      -------------------------------------------------
                            |
                    Kênh truyền sự kiện
                            |
                   Cổng tích hợp bệnh viện
          -----------------------------------------
          | Lịch hẹn | HIS | LIS | RIS/PACS | Máy |
          -----------------------------------------
```

### 15.1. Nguyên tắc kiến trúc

- NHỊP VIỆN không sở hữu hồ sơ bệnh án gốc.
- Phần mềm nguồn vẫn là nơi xác nhận dữ liệu lâm sàng.
- NHỊP VIỆN sở hữu kế hoạch điều phối, thời gian dự kiến và trạng thái hành trình.
- Mọi dữ liệu phải có nguồn và thời điểm cập nhật.
- Dữ liệu quá hạn phải chuyển sang trạng thái không xác định.
- Sự kiện gửi lặp không được tạo hành động lặp.
- Cần đối soát định kỳ để tìm sự kiện bị thiếu.

### 15.2. Không cần chia quá nhiều dịch vụ trong bản thử nghiệm

Đối với cuộc thi, nên làm một ứng dụng máy chủ có các mô-đun, tức các phần chức năng tách rõ bên trong. Cách này đơn giản hơn việc tạo nhiều dịch vụ nhỏ và vẫn đủ để trình bày kiến trúc.

---

## 16. Dữ liệu tối thiểu

### 16.1. Dữ liệu bệnh nhân

- Mã bệnh nhân đã được che hoặc mã giả lập.
- Mã lượt khám.
- Nhóm ưu tiên do nguồn chính thức cung cấp.
- Nhu cầu hỗ trợ di chuyển hoặc ngôn ngữ.
- Kênh thông báo đã đồng ý.

### 16.2. Dữ liệu công việc

- Mã dịch vụ.
- Trạng thái.
- Điều kiện tiên quyết.
- Thời điểm bắt đầu và kết thúc.
- Nguồn lực yêu cầu.
- Thời hạn.
- Lý do bị chặn.

### 16.3. Dữ liệu nguồn lực

- Mã phòng, bác sĩ hoặc thiết bị.
- Chức năng có thể phục vụ.
- Trạng thái hoạt động.
- Số vị trí đang khả dụng.
- Độ dài hàng đợi.
- Tốc độ phục vụ ước tính.
- Thời điểm cập nhật cuối.

### 16.4. Các trạng thái công việc

```text
Đã lên kế hoạch
-> Sẵn sàng
-> Đang chờ
-> Đã được gọi
-> Đang thực hiện
-> Hoàn tất
```

Trạng thái ngoại lệ:

```text
Bị chặn
Đã hủy
Không xác định
Cần nhân viên xác minh
```

---

## 17. Dùng trí tuệ nhân tạo đúng chỗ

Không phải phần nào cũng cần trí tuệ nhân tạo.

| Thành phần | Nên dùng cho | Không nên dùng cho |
|---|---|---|
| Quy tắc xác định trước | An toàn, điều kiện tiên quyết, trạng thái và quyền hạn | Dự báo phức tạp |
| Khoa học tối ưu vận hành | Phân bổ, sắp xếp và cân bằng tải | Chẩn đoán |
| Mô phỏng sự kiện rời rạc | So sánh cách vận hành và thử sự cố | Khẳng định hiệu quả thật khi chưa có dữ liệu thật |
| Machine Learning - Học máy | Dự báo thời gian và khả năng không đến sau khi có dữ liệu đủ tốt. Học máy là cách phần mềm học quy luật từ dữ liệu quá khứ | Tạo mức ưu tiên lâm sàng |
| Large Language Model - Mô hình ngôn ngữ lớn | Tóm tắt sự cố hoặc giải thích bảng điều hành. Đây là loại mô hình tạo và hiểu văn bản | Ra lệnh điều phối hoặc chẩn đoán |

Khuyến nghị cho cuộc thi:

- Dùng quy tắc cho an toàn.
- Dùng phương pháp kinh nghiệm hoặc bộ tối ưu cho điều phối.
- Dùng mô phỏng để chứng minh.
- Chưa cần mô hình ngôn ngữ lớn.
- Chưa cần học máy nếu không có dữ liệu lịch sử đáng tin cậy.

---

## 18. Giao diện bệnh nhân

Màn hình chính phải trả lời bốn câu:

1. Tôi đang ở bước nào?
2. Tôi cần làm gì tiếp theo?
3. Tôi phải chờ khoảng bao lâu?
4. Tôi cần hỏi ai nếu có vấn đề?

Ví dụ:

```text
HÀNH TRÌNH KHÁM HÔM NAY

BƯỚC TIẾP THEO
Chờ gọi tại Phòng X-quang 02
Tầng 2, Tòa B

Dự kiến: 10:20-10:35
Còn khoảng: 20-35 phút
Cập nhật lúc: 10:01

Bạn có thể rời khu chờ.
Vui lòng quay lại trước 10:15.

[Chỉ đường]       [Tôi cần hỗ trợ]

Đã hoàn tất: Đăng ký, khám ban đầu, lấy máu
Đang thực hiện: Xử lý mẫu máu
Chưa thực hiện: X-quang, tái khám
```

### 18.1. Khi đề xuất đổi tuyến

Phải hiển thị:

- Lý do.
- Lợi ích dự kiến.
- Quãng đường thêm.
- Xác nhận dịch vụ tương đương.
- Quyền giữ phương án hiện tại nếu còn khả dụng.
- Nút hỏi nhân viên.

Ví dụ:

```text
Phòng X-quang B đang ít chờ hơn.

Bạn có thể được phục vụ sớm hơn khoảng 20-30 phút.
Bạn cần đi thêm khoảng 80 mét, có thang máy.
Đây không phải thay đổi về chẩn đoán hoặc mức độ bệnh.

[Đổi sang phòng B]
[Giữ phòng hiện tại]
[Hỏi nhân viên]
```

---

## 19. Hỗ trợ người không có điện thoại thông minh

Không được tạo hai mức chất lượng phục vụ khác nhau giữa người dùng ứng dụng và người không có ứng dụng.

Giải pháp thay thế:

- Vé giấy chữ lớn.
- Mã lượt ngắn.
- Màn hình công cộng.
- Gọi bằng âm thanh.
- Thiết bị rung nếu cần.
- Tin nhắn cho người chăm sóc sau khi được đồng ý.
- Máy tự phục vụ có nút gọi nhân viên.
- Chỉ đường theo mốc dễ nhận biết.

Màn hình công cộng chỉ nên hiển thị:

- Mã lượt.
- Cửa hoặc phòng.
- Mũi tên chỉ hướng.

Không hiển thị:

- Họ tên đầy đủ.
- Số điện thoại.
- Chẩn đoán.
- Kết quả.
- Số căn cước.

---

## 20. Bảng điều hành cho nhân viên

Bảng điều hành không nên chỉ có biểu đồ đẹp. Nó phải chỉ ra việc cần làm.

### 20.1. Thông tin quan trọng

- Số bệnh nhân đang chờ.
- Thời gian chờ trung vị và mốc chậm P90.
- Khoa hoặc phòng sắp quá tải.
- Thiết bị đang dừng.
- Bệnh nhân bị kẹt giữa hai bước.
- Bệnh nhân có dữ liệu thiếu.
- Đề xuất cân bằng tải.
- Người chịu trách nhiệm xử lý.
- Thời hạn xác nhận.
- Trạng thái thông báo cho bệnh nhân.

### 20.2. Ví dụ cảnh báo tốt

> Phòng X-quang 02 tạm dừng 12 phút. Có 8 bệnh nhân bị ảnh hưởng. Đề xuất chuyển 3 bệnh nhân đủ điều kiện sang Phòng X-quang 03. Điều phối viên cần xác nhận trước 10:10.

Ví dụ cảnh báo không tốt:

> Lỗi hàng đợi.

Cảnh báo phải nói rõ vấn đề, tác động và hành động cần làm.

---

## 21. An toàn và quyền quyết định

Thông điệp quan trọng:

> Hệ thống an toàn xác định các phương án được phép. Bộ máy tối ưu chỉ xếp hạng các phương án đã được xác nhận là hợp lệ.

### 21.1. Ba mức quyền tự động

| Mức | Hành động |
|---|---|
| Tự động | Đồng bộ trạng thái, gửi nhắc việc, cập nhật thời gian dự kiến và giữ chỗ tạm có thời hạn |
| Chỉ đề xuất | Đổi thứ tự dịch vụ, chuyển phòng tương đương hoặc điều chỉnh giờ đến |
| Bắt buộc con người quyết định | Phân loại mức độ khẩn cấp; thay đổi chỉ định; thay đổi điều trị; xuất viện; thay đổi mức chăm sóc |

### 21.2. Quy tắc bắt buộc

- Xác minh ít nhất hai thông tin định danh khi thực hiện dịch vụ.
- Không dùng số phòng làm định danh bệnh nhân.
- Không dùng dữ liệu quá hạn để tự động đổi tuyến.
- Không tự động hạ mức ưu tiên.
- Ca cấp cứu phải vượt lên trên mục tiêu vận hành.
- Mọi đề xuất phải có lý do.
- Mọi thay đổi phải có nhật ký.
- Nhân viên phải có quyền từ chối.
- Khi không chắc chắn, hệ thống phải dừng hoặc giảm tự động hóa.

### 21.3. Phương án dự phòng

Không dùng quy tắc đến trước phục vụ trước một cách thuần túy.

Thứ tự dự phòng nên là:

```text
Ưu tiên lâm sàng
-> Thời hạn bắt buộc
-> Thời gian đã chờ
-> Giữ ổn định kế hoạch hiện tại
```

---

## 22. Quyền riêng tư và bảo mật

Dữ liệu sức khỏe là dữ liệu nhạy cảm.

Yêu cầu tối thiểu:

- Chỉ thu thập dữ liệu cần thiết.
- Mã hóa dữ liệu, tức biến dữ liệu thành dạng người không có khóa giải mã không thể đọc được, khi gửi và khi lưu.
- Phân quyền theo vai trò.
- Ghi nhật ký cả việc đọc và thay đổi dữ liệu nhạy cảm.
- Không ghi thông tin bệnh nhân đầy đủ vào nhật ký kỹ thuật.
- Không gửi chẩn đoán trong tin nhắn thông thường.
- Không hiển thị họ tên đầy đủ trên màn hình công cộng.
- Liên kết trong tin nhắn phải có thời hạn.
- Quyền chia sẻ cho người chăm sóc phải có sự đồng ý.
- Dữ liệu cuộc thi phải là dữ liệu giả lập.
- Cần đội pháp chế và bệnh viện xác nhận quy định áp dụng trước khi triển khai thật.

---

## 23. Chế độ khi hệ thống gặp lỗi

| Sự cố | Hành vi an toàn |
|---|---|
| Mất kết nối hệ thống trung tâm | Giữ kế hoạch đã xác nhận, dùng hàng đợi cục bộ và ghi nhận để đồng bộ sau |
| HIS không phản hồi | Hiển thị đang chờ xác nhận, không tự tạo chỉ định |
| LIS hoặc RIS không phản hồi | Không giả định dịch vụ đã hoàn tất; chuyển nhân viên xác minh |
| Bộ máy tối ưu lỗi | Chuyển sang quy tắc ưu tiên lâm sàng, thời hạn và thời gian đã chờ |
| Dự báo thời gian lỗi | Dùng khoảng thời gian lịch sử và công thức hàng đợi đơn giản |
| Dữ liệu nguồn lực quá hạn | Chuyển trạng thái nguồn lực thành không xác định |
| Kênh tin nhắn lỗi | Dùng màn hình, vé giấy hoặc gọi tại chỗ |
| Có nghi ngờ sai danh tính | Dừng hành động liên quan và yêu cầu xác minh |

Giao diện phải hiển thị rõ hệ thống đang ở chế độ nào. Không được giả vờ dữ liệu cũ là dữ liệu mới.

---

## 24. Chỉ số đánh giá

### 24.1. Chỉ số bệnh nhân

| Chỉ số | Cách hiểu |
|---|---|
| Tổng thời gian hành trình | Từ lúc xác nhận bệnh nhân đã đến đến lúc hoàn tất các bước trong phạm vi đo |
| Thời gian chờ trung vị | Một nửa bệnh nhân chờ ít hơn và một nửa chờ lâu hơn |
| Thời gian chờ P90 | 90 phần trăm bệnh nhân chờ không quá mốc này nếu số liệu được hiệu chỉnh tốt |
| Tỷ lệ hoàn tất trong ngày | Phần trăm bệnh nhân hoàn tất hành trình trong ngày |
| Số lần quay lại không cần thiết | Số lần phải quay lại vì kết quả hoặc điều kiện chưa sẵn sàng |
| Quãng đường di chuyển | Tổng khoảng cách bệnh nhân phải đi |
| Tỷ lệ bỏ về | Phần trăm bệnh nhân rời bệnh viện trước khi hoàn tất |

### 24.2. Chỉ số nguồn lực

| Chỉ số | Cách hiểu |
|---|---|
| Mức sử dụng hữu ích | Thời gian nguồn lực thực sự phục vụ |
| Thời gian rảnh do thiếu bệnh nhân sẵn sàng | Nguồn lực có thể làm việc nhưng không có ca đủ điều kiện |
| Thời gian bị chặn | Không thể tiếp tục vì bước phía sau quá tải hoặc thiếu điều kiện |
| Làm thêm giờ | Thời gian vượt quá ca làm dự kiến |
| Số lượt hoàn tất | Số bệnh nhân hoặc công việc hoàn thành trong một khoảng thời gian |

### 24.3. Chỉ số dự báo

- Sai số tuyệt đối trung bình.
- Tỷ lệ trường hợp nằm trong khoảng P90.
- Độ rộng khoảng dự báo.
- Số lần thời gian dự kiến thay đổi.
- Sai số theo từng khoa và khung giờ.

### 24.4. Chỉ số an toàn và công bằng

- Số lần vi phạm ràng buộc bắt buộc. Mục tiêu là bằng không.
- Tỷ lệ ca ưu tiên bị trễ.
- Chênh lệch thời gian chờ giữa nhóm có và không có điện thoại thông minh.
- Chênh lệch theo tuổi, mức ưu tiên và nhu cầu hỗ trợ.
- Số lần nhân viên từ chối hoặc ghi đè đề xuất.
- Số sự cố sai danh tính hoặc lộ dữ liệu.

---

## 25. Cách chứng minh giải pháp hiệu quả

### 25.1. Các phương án đối chứng

Phải so sánh ít nhất bốn cách:

1. Quy trình hiện tại được mô phỏng.
2. Đến trước phục vụ trước.
3. Chọn hàng đợi ngắn nhất.
4. Chính sách điều phối của NHỊP VIỆN.

### 25.2. Cách so sánh công bằng

- Dùng cùng số bệnh nhân.
- Dùng cùng thời điểm đến.
- Dùng cùng loại dịch vụ.
- Dùng cùng thời gian phục vụ.
- Dùng cùng sự cố.
- Dùng cùng hạt giống ngẫu nhiên.

### 25.3. Số lần chạy

Nên chạy 30 đến 50 lần với các hạt giống khác nhau.

Không được chọn một lần chạy đẹp nhất.

### 25.4. Tình huống kiểm thử

- Nhu cầu tăng 20 phần trăm.
- Một thiết bị hỏng.
- Một bác sĩ đến muộn.
- Một ca cấp cứu xuất hiện.
- 15 phần trăm sự kiện bị trễ hoặc thiếu.
- Nhân viên từ chối một số đề xuất.
- Thời gian phê duyệt bị chậm.

### 25.5. Kiểm thử tách thành phần

Kiểm thử tách thành phần nghĩa là lần lượt tắt từng chức năng để biết chức năng nào thật sự tạo giá trị.

Nên so sánh:

- Chỉ theo dõi trạng thái.
- Theo dõi cộng dự báo thời gian.
- Theo dõi cộng đề xuất.
- Toàn bộ vòng điều phối.

---

## 26. Phạm vi sản phẩm khả dụng tối thiểu

Không nên làm toàn bệnh viện trong cuộc thi.

Phạm vi đề xuất:

- Một cơ sở ngoại trú.
- Hai phòng khám.
- Một khu lấy mẫu và xét nghiệm.
- Một phòng X-quang.
- Hành trình cốt lõi: khám, xét nghiệm hoặc X-quang, quay lại bác sĩ.
- Siêu âm là mục tiêu mở rộng nếu còn thời gian.
- Dữ liệu hoàn toàn giả lập.

### 26.1. Chức năng bắt buộc

1. Bộ tạo bệnh nhân và sự kiện giả lập.
2. Đồ thị hành trình.
3. Máy trạng thái công việc.
4. Quy tắc an toàn.
5. Ba phương án đối chứng.
6. Bộ điều phối động.
7. Dự báo khoảng thời gian.
8. Màn hình bệnh nhân.
9. Bảng điều hành nhân viên.
10. Nhật ký quyết định.
11. Nút giả lập sự cố.
12. Bảng so sánh trước và sau.

### 26.2. Không nên đưa vào bản thử nghiệm

- Chẩn đoán tự động.
- Phân loại mức độ khẩn cấp tự động.
- Dữ liệu bệnh nhân thật.
- Tích hợp ghi trực tiếp vào phần mềm bệnh viện thật.
- Mô hình ngôn ngữ lớn.
- Học máy khi chưa có dữ liệu lịch sử.
- Tối ưu toàn bệnh viện.
- Theo dõi vị trí chính xác của bệnh nhân nếu không cần thiết.

---

## 27. Công nghệ tham khảo cho đội phát triển

Phần này chỉ là gợi ý. Đội nên chọn công nghệ mình đã quen.

| Phần | Công nghệ gợi ý | Giải thích |
|---|---|---|
| Giao diện web | React - Thư viện xây dựng giao diện web | Giúp tạo các màn hình bệnh nhân và bảng điều hành bằng các thành phần tái sử dụng |
| Công cụ tạo dự án giao diện | Vite - Công cụ tạo và chạy dự án web nhanh | Giúp khởi động dự án React và cập nhật giao diện nhanh trong lúc phát triển |
| Máy chủ | FastAPI - Khung xây dựng giao diện lập trình bằng ngôn ngữ Python | Nhận yêu cầu, trả dữ liệu và kết nối mô phỏng với giao diện |
| Mô phỏng | SimPy - Thư viện mô phỏng sự kiện rời rạc bằng ngôn ngữ Python | Mô phỏng bệnh nhân đến, xếp hàng, được phục vụ và gặp sự cố |
| Tối ưu | OR-Tools - Bộ công cụ tối ưu vận hành | Hỗ trợ bài toán phân bổ và sắp xếp có ràng buộc |
| Cơ sở dữ liệu | PostgreSQL - Hệ quản trị cơ sở dữ liệu quan hệ | Lưu hành trình, trạng thái, sự kiện và nhật ký theo bảng có quan hệ |
| Cập nhật gần thời gian thực | SSE - Cơ chế máy chủ gửi cập nhật tới trình duyệt | Giúp bảng điều hành tự cập nhật khi trạng thái thay đổi |

Nếu đội chưa quen các công nghệ trên, có thể dùng một ngôn ngữ và một cơ sở dữ liệu đơn giản hơn. Khả năng hoàn thành quan trọng hơn kiến trúc phức tạp.

---

## 28. Kế hoạch làm trong 72 giờ

| Khoảng thời gian | Công việc | Kết quả cần có |
|---|---|---|
| 0-6 giờ | Chốt một hành trình và các trạng thái | Sơ đồ hành trình rõ ràng |
| 6-12 giờ | Định nghĩa dữ liệu và ràng buộc | Bảng dữ liệu và khoảng 10 quy tắc an toàn |
| 12-24 giờ | Viết mô phỏng và cách vận hành hiện tại | Chạy được phương án đối chứng |
| 24-36 giờ | Viết bộ điều phối động | Có đề xuất bước tiếp theo |
| 36-44 giờ | Tạo dự báo thời gian | Hiển thị khoảng P50 và P90 |
| 44-54 giờ | Làm giao diện bệnh nhân | Xem được hành trình và bước tiếp theo |
| 54-62 giờ | Làm bảng điều hành nhân viên | Xem được hàng đợi, nguồn lực và cảnh báo |
| 62-68 giờ | Thêm sự cố và chế độ dự phòng | Trình diễn được máy hỏng và dữ liệu quá hạn |
| 68-72 giờ | Chạy số liệu, sửa lỗi và luyện thuyết trình | Có bảng kết quả và kịch bản ổn định |

### 28.1. Phân công cho đội bốn người

| Người | Nhiệm vụ |
|---|---|
| Người 1 | Mô phỏng và dữ liệu giả lập |
| Người 2 | Bộ điều phối, quy tắc và dự báo |
| Người 3 | Giao diện bệnh nhân và bảng điều hành |
| Người 4 | Tích hợp, kiểm thử, số liệu và bài thuyết trình |

Mọi người cần thống nhất cấu trúc dữ liệu trước khi làm riêng.

---

## 29. Kịch bản trình diễn

### 29.1. Bố cục

Chia màn hình thành hai phía:

```text
Bên trái: Cách vận hành hiện tại
Bên phải: NHỊP VIỆN
```

Hai bên phải dùng cùng dữ liệu đầu vào.

### 29.2. Kịch bản từng bước

1. Khởi tạo 60 bệnh nhân giả lập.
2. Một số bệnh nhân chỉ khám.
3. Một số cần xét nghiệm.
4. Một số cần X-quang và quay lại bác sĩ.
5. Chạy hai phương án trong cùng điều kiện.
6. Bấm nút làm máy X-quang dừng 30 phút.
7. Cho một ca cấp cứu xuất hiện.
8. Quan sát cách NHỊP VIỆN giữ ưu tiên cấp cứu.
9. Quan sát các bệnh nhân đủ điều kiện được chuyển sang bước độc lập khác.
10. Quan sát giữ chỗ ngăn mọi người cùng dồn sang một phòng.
11. Xem ứng dụng bệnh nhân cập nhật bước tiếp theo.
12. Xem bảng điều hành giao nhiệm vụ cho nhân viên.
13. Làm dữ liệu xét nghiệm bị quá hạn.
14. Quan sát hệ thống dừng đề xuất tự động và chuyển sang chế độ dự phòng.
15. Hiển thị bảng kết quả cuối cùng.

### 29.3. Khoảnh khắc cần nhấn mạnh

> Không thêm bác sĩ hay thiết bị. Hệ thống chỉ giảm thời gian đứng yên bằng cách sử dụng tốt hơn các bước có thể thực hiện song song và điều phối lại khi có sự cố.

---

## 30. Bảng kết quả trình diễn

Các con số dưới đây chỉ là mẫu định dạng. Phải thay bằng kết quả mô phỏng thật của đội.

| Chỉ số | Phương án hiện tại | NHỊP VIỆN | Thay đổi |
|---|---:|---:|---:|
| Thời gian toàn hành trình trung vị | Chưa đo | Chưa đo | Chưa tính |
| Thời gian toàn hành trình P90 | Chưa đo | Chưa đo | Chưa tính |
| Số bệnh nhân chờ trên 60 phút | Chưa đo | Chưa đo | Chưa tính |
| Số người cao nhất tại khu chờ | Chưa đo | Chưa đo | Chưa tính |
| Mức sử dụng hữu ích của X-quang | Chưa đo | Chưa đo | Chưa tính |
| Số lần quay lại không cần thiết | Chưa đo | Chưa đo | Chưa tính |
| Vi phạm ưu tiên lâm sàng | Chưa đo | Chưa đo | Phải bằng 0 |
| Số lần đổi tuyến trung bình | Chưa đo | Chưa đo | Càng thấp càng tốt |

Không điền số liệu do tưởng tượng. Chỉ điền kết quả phần mềm đã chạy.

---

## 31. Cấu trúc thuyết trình 6 phút

| Thời gian | Nội dung |
|---|---|
| 0:00-0:35 | Kể một hành trình bệnh nhân bị chờ và quay lại nhiều lần |
| 0:35-1:10 | Giải thích bệnh viện là mạng hàng đợi, không phải một hàng |
| 1:10-1:50 | Giới thiệu vòng điều phối của NHỊP VIỆN |
| 1:50-3:40 | Trình diễn máy hỏng, ca cấp cứu và điều phối lại |
| 3:40-4:30 | Hiển thị kết quả so sánh và cách chạy mô phỏng |
| 4:30-5:10 | Trình bày an toàn, quyền riêng tư và chế độ dự phòng |
| 5:10-5:45 | Trình bày phạm vi thử nghiệm và lộ trình tích hợp |
| 5:45-6:00 | Kết luận ngắn |

Câu kết đề xuất:

> NHỊP VIỆN không thay bác sĩ quyết định chuyên môn. Hệ thống giúp bệnh viện nhìn thấy toàn hành trình, đề xuất hành động điều phối an toàn và đo xem hành động đó có thật sự giảm thời gian chờ hay không.

---

## 32. Các câu hỏi khó từ giám khảo

### Câu hỏi 1: Nếu bỏ trí tuệ nhân tạo thì giải pháp còn giá trị không?

Trả lời:

> Có. Giá trị cốt lõi đến từ kết nối trạng thái, đồ thị hành trình, quy tắc an toàn, mô phỏng và điều phối có ràng buộc. Học máy chỉ là bước nâng cấp dự báo khi có dữ liệu tốt.

### Câu hỏi 2: Hệ thống có tự thay đổi mức ưu tiên bệnh nhân không?

Trả lời:

> Không. Mức ưu tiên lâm sàng phải đến từ quy trình được bệnh viện phê duyệt hoặc nhân viên y tế có thẩm quyền. Hệ thống chỉ điều phối trong cùng vùng an toàn.

### Câu hỏi 3: Nếu dữ liệu bị chậm thì sao?

Trả lời:

> Dữ liệu có thời hạn sử dụng. Khi quá hạn, hệ thống không tiếp tục tự động đổi tuyến. Hệ thống hiển thị cảnh báo, yêu cầu xác minh và chuyển sang quy tắc dự phòng.

### Câu hỏi 4: Vì sao đây không chỉ là bảng theo dõi?

Trả lời:

> Bảng theo dõi chỉ cho biết đang có vấn đề. NHỊP VIỆN còn tạo phương án, kiểm tra an toàn, giao việc, chờ xác nhận, thông báo cho bệnh nhân và đo kết quả sau hành động.

### Câu hỏi 5: Vì sao gọi là đổi mới?

Trả lời:

> Điểm mới nằm ở việc tối ưu toàn hành trình thay vì từng hàng đợi, kết hợp mô phỏng sự cố với điều phối vòng kín và chỉ cho phép tối ưu trong tập phương án đã qua kiểm tra an toàn.

### Câu hỏi 6: Làm sao tích hợp với bệnh viện cũ?

Trả lời:

> Giải pháp dùng bộ chuyển đổi kết nối. Có thể bắt đầu bằng tệp dữ liệu, giao diện đọc hoặc sự kiện giả lập, sau đó nâng cấp dần lên chuẩn HL7 hoặc FHIR mà không thay toàn bộ phần mềm hiện có.

---

## 33. Những tuyên bố không nên dùng

| Không nên nói | Nên nói |
|---|---|
| Bản sao số toàn bệnh viện | Bộ mô phỏng luồng cho một hành trình ngoại trú; sẽ trở thành bản sao số khi có đồng bộ và hiệu chỉnh bằng dữ liệu thật |
| Bảo đảm an toàn | Bản thử nghiệm có quy tắc an toàn, chưa được kiểm định lâm sàng |
| Tìm tuyến tối ưu | Tìm tuyến phù hợp bằng phương pháp có ràng buộc |
| Giảm 30 phần trăm thời gian chờ | Trong mô phỏng, giải pháp tạo ra mức thay đổi so với phương án đối chứng dưới các giả định đã công bố |
| Dự báo chính xác | Cung cấp khoảng dự báo và đo sai số |
| Tích hợp thời gian thực | Đã mô phỏng hợp đồng sự kiện hoặc đã kết nối thử với nguồn cụ thể |
| Bảo đảm công bằng | Có chỉ số và quy tắc theo dõi công bằng, chưa chứng minh đầy đủ trên bệnh viện thật |

Sự trung thực làm giải pháp đáng tin hơn.

---

## 34. Rủi ro và cách giảm rủi ro

| Rủi ro | Hậu quả | Cách giảm |
|---|---|---|
| Sai danh tính | Phục vụ hoặc gửi thông báo sai người | Hai định danh, dừng khi mâu thuẫn, nhật ký đầy đủ |
| Dữ liệu quá hạn | Điều phối tới nơi đã đóng | Thời hạn dữ liệu, trạng thái không xác định và xác minh lại |
| Mọi người cùng chuyển sang hàng ngắn | Tạo điểm nghẽn mới | Giữ chỗ, ngưỡng chống dao động và giới hạn số người chuyển |
| Thời gian dự báo sai | Bệnh nhân mất niềm tin hoặc bỏ lỡ lượt | Hiển thị khoảng, thời điểm cập nhật và độ tin cậy |
| Nhân viên không duyệt kịp | Tạo một hàng đợi phê duyệt mới | Chỉ yêu cầu duyệt thay đổi cần thiết, đo thời gian duyệt và có thời hạn nhắc |
| Tối ưu ca ngắn, bỏ quên ca dài | Thiếu công bằng | Tăng ưu tiên theo thời gian đã chờ và đặt giới hạn chờ tối đa |
| Hệ thống lỗi | Gián đoạn vận hành | Chế độ thủ công, vé giấy, quy tắc dự phòng và hướng dẫn xử lý |
| Lộ thông tin | Vi phạm quyền riêng tư | Giảm dữ liệu, phân quyền, mã hóa và không hiển thị thông tin nhạy cảm công khai |

---

## 35. Lộ trình triển khai sau cuộc thi

### Giai đoạn 1: Khảo sát

- Chọn một hành trình ngoại trú.
- Vẽ quy trình thật.
- Xác định nguồn dữ liệu.
- Thống nhất định nghĩa thời gian chờ.
- Xác định quy tắc an toàn với bệnh viện.

### Giai đoạn 2: Chạy lại dữ liệu lịch sử

- Dùng dữ liệu đã giảm định danh.
- So sánh cách hiện tại với chính sách đề xuất.
- Hiệu chỉnh thời gian phục vụ.

### Giai đoạn 3: Chế độ quan sát

Hệ thống nhận dữ liệu và đưa đề xuất nhưng không tác động vận hành thật.

Mục tiêu:

- Kiểm tra dữ liệu.
- Đo độ chính xác.
- Xem nhân viên có đồng ý với đề xuất không.

### Giai đoạn 4: Chế độ hỗ trợ

- Nhân viên xem và phê duyệt đề xuất.
- Bệnh nhân nhận thời gian dự kiến.
- Mọi hành động có nhật ký.

### Giai đoạn 5: Tự động hóa giới hạn

Chỉ tự động các hành động ít rủi ro và có thể hoàn tác, ví dụ:

- Cập nhật thời gian dự kiến.
- Gửi nhắc việc.
- Giữ chỗ tạm thời.
- Xếp thứ tự trong cùng một nhóm ưu tiên theo chính sách đã duyệt.

### Giai đoạn 6: Mở rộng

- Thêm khoa.
- Thêm loại thiết bị.
- Thêm dự báo học máy.
- Kết nối nhiều cơ sở.

---

## 36. Lợi thế phù hợp với bối cảnh VNPT IT

Nếu đội được phép sử dụng hoặc đề xuất hệ sinh thái VNPT, có thể nhấn mạnh các hướng sau:

- Hạ tầng tại Việt Nam hoặc triển khai tại bệnh viện.
- Kênh tin nhắn và thoại để hỗ trợ người không cài ứng dụng.
- Khả năng kết nối nhiều cơ sở.
- Lớp tích hợp với các hệ thống y tế khác nhau.
- Giám sát vận hành và cảnh báo tập trung.
- Khả năng mở rộng từ một khoa tới nhiều bệnh viện.

Chỉ nên trình bày những năng lực đội có thể chứng minh hoặc có nguồn xác nhận. Không nên tự gán các sản phẩm cụ thể cho VNPT nếu chưa kiểm tra.

---

## 37. Danh sách kiểm tra trước khi nộp

### Bài toán

- [ ] Đã chọn một hành trình cụ thể.
- [ ] Đã xác định điểm bắt đầu và kết thúc thời gian chờ.
- [ ] Đã có sơ đồ trước sau của các bước.
- [ ] Đã phân biệt ràng buộc bắt buộc và mong muốn.

### Sản phẩm

- [ ] Có phương án đối chứng.
- [ ] Có bộ điều phối động.
- [ ] Có dự báo dạng khoảng.
- [ ] Có giao diện bệnh nhân.
- [ ] Có bảng điều hành nhân viên.
- [ ] Có nhật ký quyết định.
- [ ] Có chế độ dự phòng.

### Mô phỏng

- [ ] Dùng cùng dữ liệu cho các phương án.
- [ ] Chạy nhiều lần.
- [ ] Có máy hỏng.
- [ ] Có ca cấp cứu.
- [ ] Có dữ liệu quá hạn hoặc bị thiếu.
- [ ] Có đo thời gian phê duyệt.

### An toàn

- [ ] Không tự động chẩn đoán.
- [ ] Không tự động thay đổi mức phân loại khẩn cấp.
- [ ] Không dùng dữ liệu thật chưa được phép.
- [ ] Màn hình công cộng không lộ thông tin cá nhân.
- [ ] Có quyền từ chối và ghi đè.
- [ ] Vi phạm ràng buộc bắt buộc bằng không trong mô phỏng.

### Thuyết trình

- [ ] Có một câu chuyện bệnh nhân cụ thể.
- [ ] Có trình diễn hành động, không chỉ biểu đồ.
- [ ] Có bảng trước và sau.
- [ ] Ghi rõ số liệu là mô phỏng.
- [ ] Không tuyên bố quá mức.
- [ ] Có lộ trình triển khai thật.

---

## 38. Kết luận cuối cùng

Giải pháp mạnh nhất cho đề tài này là một vòng điều phối nhỏ nhưng hoàn chỉnh:

```text
Sự kiện thật hoặc giả lập
-> Trạng thái hành trình
-> Dự báo điểm nghẽn
-> Lọc phương án an toàn
-> Đề xuất điều phối
-> Nhân viên xác nhận
-> Bệnh nhân được thông báo
-> Kết quả được đo
```

Điểm tạo khác biệt:

1. Tối ưu toàn hành trình thay vì từng hàng đợi.
2. Tận dụng thời gian xử lý song song.
3. Điều chỉnh khi có sự cố.
4. Không cho bộ máy tối ưu vượt qua quy tắc an toàn.
5. Chứng minh bằng phương án đối chứng và nhiều lần mô phỏng.

Câu định vị cuối:

> NHỊP VIỆN không cố ép từng phòng làm việc nhanh hơn. Hệ thống giúp toàn bộ hành trình bệnh nhân ít phải đứng yên hơn, trong khi quyết định lâm sàng vẫn thuộc về nhân viên y tế.
