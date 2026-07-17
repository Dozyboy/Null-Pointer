# DỊCH VỤ AI NHỊP VIỆN

Thư mục này chứa bộ xếp hạng lộ trình, dự báo chờ, hợp đồng dữ liệu và chính sách quản trị AI.

Phiên bản đầu dùng bộ quy tắc xác định được để có thể kiểm thử. Có thể thay bằng mô hình học máy sau, nhưng hợp đồng API và bộ kiểm tra an toàn không được bỏ.

## Chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn nhip_vien_ai.main:app --reload --port 8010
```

## Kiểm tra

```powershell
pytest
ruff check .
```

## Endpoint

- `GET /health`.
- `POST /v1/route-options`: xếp hạng ứng viên đã kiểm tra.
- `POST /v1/wait-estimates`: ước lượng khoảng chờ.

Không gọi endpoint AI trực tiếp từ frontend. Backend là nơi kiểm tra quyền, ràng buộc và lưu quyết định.
