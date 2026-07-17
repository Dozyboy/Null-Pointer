FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY config ./config
COPY src ./src

RUN pip install --no-cache-dir .

EXPOSE 8010

CMD ["uvicorn", "nhip_vien_ai.main:app", "--host", "0.0.0.0", "--port", "8010"]
