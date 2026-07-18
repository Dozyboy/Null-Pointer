from app.core.config import get_settings
from app.modules.simulation.clinical_service_repository import sqlite_path_from_url
from app.modules.support.repository import SqliteSupportRequestRepository
from app.modules.support.service import SupportRequestService

support_request_repository = SqliteSupportRequestRepository(
    sqlite_path_from_url(get_settings().database_url)
)
support_request_service = SupportRequestService(support_request_repository)
