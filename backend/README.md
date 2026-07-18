# BACKEND FASTAPI

Backend là nguồn quyết định nghiệp vụ và cổng API duy nhất của frontend. Dịch vụ AI chỉ tạo đề xuất; backend kiểm tra lại trước khi trả cho người dùng.

## Chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Kiểm tra

```powershell
pytest
ruff check .
```

## Endpoint hiện có

- `GET /health`.
- `GET /api/v1/patients` và `GET /api/v1/patients/{patient_id}`.
- `GET /api/v1/patients/{patient_code}/activities/today`.
- `POST /api/v1/encounters/{encounter_id}/route-proposals`.
- `POST /api/v1/route-reservations`.
- `POST /api/v1/route-reservations/{reservation_id}/extend`.
- `POST /api/v1/route-reservations/{reservation_id}/confirm`.
- `GET /api/v1/route-reservations/patients/{patient_code}/latest`.
- `PATCH /api/v1/route-reservations/{reservation_id}/progress`.
- `POST /api/v1/support-requests` và `GET /api/v1/support-requests/{request_id}`.
- `GET /api/v1/simulation/snapshot`.
- `POST /api/v1/simulation/advance`.
- `POST /api/v1/simulation/reset`.
- `POST /api/v1/simulation/rooms`.
- `PATCH /api/v1/simulation/rooms/{room_code}`.
- `PATCH /api/v1/simulation/rooms/{room_code}/queue`.
- `GET`, `POST`, `PUT`, `DELETE /api/v1/simulation/clinical-services`.
- `POST /api/v1/simulation/clinical-orders`.
- `GET /api/v1/simulation/patients/{patient_code}/clinical-orders/latest`.
- `POST /api/v1/simulation/patients/{patient_code}/clinical-orders/latest/route-proposals`.

Endpoint tạo lộ trình dùng bộ tối ưu xác định để đọc trạng thái phòng và hàng chờ mô phỏng, sinh các thứ tự hợp lệ rồi trả tối đa ba phương án. Kết quả vẫn có cờ `is_demo=true` và không được sử dụng để điều phối bệnh nhân thật.

Dữ liệu bệnh nhân, danh mục, phòng, chỉ định, đề xuất, giữ chỗ, tiến độ, nhật ký và yêu cầu hỗ trợ được lưu trong SQLite. Đồng hồ, sự kiện và các bệnh nhân tạm của kịch bản mô phỏng chỉ tồn tại trong bộ nhớ tiến trình.

Xem [thuật toán phân luồng](../docs/development/routing-algorithm.md) và [kiến trúc hệ thống](../docs/architecture/system-architecture.md) trước khi sửa mô-đun.
