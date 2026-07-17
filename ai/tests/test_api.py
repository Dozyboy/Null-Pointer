from fastapi.testclient import TestClient

from nhip_vien_ai.main import app

client = TestClient(app)


def test_route_options_endpoint_ranks_prevalidated_candidates() -> None:
    response = client.post(
        "/v1/route-options",
        json={
            "request_id": "request-api-1",
            "encounter_reference": "anonymous-encounter",
            "priority": "fastest",
            "required_service_codes": ["blood_test"],
            "candidates": [
                {
                    "id": "candidate-1",
                    "duration_minutes_min": 60,
                    "duration_minutes_max": 80,
                    "distance_meters": 200,
                    "floor_changes": 1,
                    "is_accessible": True,
                    "steps": [
                        {
                            "service_code": "blood_test",
                            "room_id": "blood-room-1",
                            "room_name": "Lấy máu 01",
                            "floor": "Tầng 1",
                            "wait_minutes_min": 5,
                            "wait_minutes_max": 10,
                        }
                    ],
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["options"][0]["candidate_id"] == "candidate-1"
