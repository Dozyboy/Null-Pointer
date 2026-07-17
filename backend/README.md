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
- `POST /api/v1/encounters/{encounter_id}/route-proposals`.
- `POST /api/v1/support-requests`.

Endpoint tạo lộ trình hiện trả dữ liệu minh họa có cờ `is_demo=true`. Không được sử dụng như dữ liệu điều phối thật.

Xem [kiến trúc hệ thống](../docs/architecture/system-architecture.md) trước khi thêm mô-đun.
