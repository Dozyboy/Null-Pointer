# FRONTEND REACT

Ứng dụng sản xuất được tổ chức theo tính năng. Giao diện trong `../giaodien/` là nguồn đối chiếu để chuyển dần, không nhập trực tiếp dữ liệu mô phỏng vào mã sản xuất.

## Chạy

```powershell
npm install
npm run dev
```

## Kiểm tra

```powershell
npm run typecheck
npm run lint
npm run test
npm run build
```

## Quy tắc phụ thuộc

```text
app → features → entities → shared
```

Xem [cấu trúc dự án](../docs/architecture/project-structure.md) và [quy tắc AI](../AGENTS.md) trước khi thêm tính năng.
