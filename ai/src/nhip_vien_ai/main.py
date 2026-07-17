from fastapi import FastAPI

from nhip_vien_ai.api.router import router
from nhip_vien_ai.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="NHỊP VIỆN AI",
        version="0.1.0",
        description=(
            "Dịch vụ nội bộ chỉ xếp hạng ứng viên đã được backend kiểm tra; "
            "không đưa ra quyết định lâm sàng."
        ),
    )
    application.include_router(router)
    application.state.model_provider = settings.model_provider
    return application


app = create_app()
