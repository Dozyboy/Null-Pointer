from app.core.config import get_settings
from app.modules.audit.runtime import patient_activity_service
from app.modules.patients.runtime import patient_registry_service
from app.modules.routing.runtime import route_proposal_service
from app.modules.simulation.clinical_order_repository import (
    SqliteClinicalOrderRepository,
)
from app.modules.simulation.clinical_order_service import (
    ClinicalOrderSimulationService,
)
from app.modules.simulation.clinical_service_repository import sqlite_path_from_url
from app.modules.simulation.clinical_service_runtime import (
    clinical_service_catalog_service,
)
from app.modules.simulation.runtime import simulation_service

clinical_order_repository = SqliteClinicalOrderRepository(
    sqlite_path_from_url(get_settings().database_url)
)
clinical_order_simulation_service = ClinicalOrderSimulationService(
    catalog=clinical_service_catalog_service,
    simulation=simulation_service,
    routing=route_proposal_service,
    repository=clinical_order_repository,
    patients=patient_registry_service,
    activities=patient_activity_service,
)
