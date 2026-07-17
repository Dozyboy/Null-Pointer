from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_demo_route_proposal() -> None:
    response = client.post(
        "/api/v1/encounters/TM-2026-00847/route-proposals",
        json={
            "priority": "fastest",
            "accessibility": {
                "wheelchair": False,
                "avoid_stairs": False,
                "visual_assistance": False,
            },
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["encounter_id"] == "TM-2026-00847"
    assert data["is_demo"] is True
    assert len(data["options"]) == 3
    assert data["options"][0]["steps"][0]["is_locked"] is True
