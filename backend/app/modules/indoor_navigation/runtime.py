from app.core.config import get_settings
from app.modules.indoor_navigation.repository import (
    SqliteIndoorNavigationRepository,
    sqlite_path_from_url,
)
from app.modules.indoor_navigation.service import IndoorNavigationService

indoor_navigation_repository = SqliteIndoorNavigationRepository(
    sqlite_path_from_url(get_settings().database_url)
)
indoor_navigation_service = IndoorNavigationService(indoor_navigation_repository)
