# HƯỚNG DẪN PHÁT TRIỂN

## 1. Yêu cầu máy

- Node.js 22 trở lên để chạy frontend.
- Python 3.12 trở lên để chạy backend và AI.
- Git.
- GitNexus chạy qua `npx`.

**Node.js – môi trường chạy JavaScript ngoài trình duyệt** dùng để cài và xây dựng React.
**Môi trường ảo Python** là thư mục thư viện riêng của dự án, tránh làm thay đổi Python toàn máy.

## 2. Frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Các lệnh:

```powershell
npm run build
npm run lint
npm run test
npm run typecheck
```

- `build`: tạo bản đóng gói dùng để triển khai.
- `lint`: kiểm tra quy tắc mã nguồn.
- `test`: chạy kiểm thử.
- `typecheck`: kiểm tra kiểu TypeScript mà không tạo tệp.

## 3. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

Kiểm tra:

```powershell
pytest
ruff check .
```

Tài liệu API tự động tại `http://localhost:8000/docs`.

## 4. AI

```powershell
cd ai
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn nhip_vien_ai.main:app --reload --port 8010
```

Kiểm tra:

```powershell
pytest
ruff check .
```

## 5. Địa chỉ mặc định

| Thành phần | Địa chỉ |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:8000` |
| Backend API docs | `http://localhost:8000/docs` |
| AI | `http://localhost:8010` |
| AI API docs | `http://localhost:8010/docs` |

## 6. Biến môi trường

Không đưa tệp `.env` lên Git. Chỉ đưa `.env.example` với giá trị mẫu không nhạy cảm.

Frontend:

```text
VITE_API_URL=https://nhip-vien-backend-845428428754.asia-east1.run.app/api/v1
```

Giá trị trên kết nối tới backend cloud của bản demo. Khi phát triển hoàn toàn trên máy cá nhân, có thể ghi đè thành `http://localhost:8000/api/v1` trong tệp `frontend/.env`.

Backend:

```text
APP_ENV=development
DATABASE_URL=sqlite:///./nhip_vien.db
AI_SERVICE_URL=http://localhost:8010
```

AI:

```text
AI_ENV=development
AI_MODEL_PROVIDER=rule_based
AI_REQUEST_TIMEOUT_SECONDS=5
```

## 7. Thứ tự phát triển một tính năng

1. Đọc yêu cầu chức năng và quy tắc nghiệp vụ.
2. Chạy quy trình GitNexus.
3. Xác định API và cấu trúc dữ liệu.
4. Viết kiểm thử thất bại trước cho quy tắc quan trọng.
5. Cài đặt backend hoặc AI.
6. Cài đặt giao diện và trạng thái lỗi.
7. Chạy kiểm thử, lint, build.
8. Chạy GitNexus phát hiện thay đổi.
9. Cập nhật tài liệu nếu hành vi thay đổi.
