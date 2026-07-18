from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_read_persisted_support_request() -> None:
    response = client.post(
        "/api/v1/support-requests",
        json={
            "encounter_id": "TM-2026-00847",
            "support_type": "wheelchair",
            "location": "Tầng 2, khu A",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "received"
    assert response.json()["is_demo"] is True
    assert response.json()["encounter_id"] == "TM-2026-00847"
    assert response.json()["support_type"] == "wheelchair"

    detail_response = client.get(
        f"/api/v1/support-requests/{response.json()['id']}"
    )

    assert detail_response.status_code == 200
    assert detail_response.json() == response.json()
