from fastapi.testclient import TestClient

from app.main import app


def test_vehicle_filters() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/vehicles", params={"routeId": "route-16"})

    assert response.status_code == 200
    vehicles = response.json()["vehicles"]
    assert len(vehicles) == 1
    assert vehicles[0]["routeShortName"] == "16"


def test_route_shape_is_geojson() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/routes/route-16/shape",
            params={"directionId": 1},
        )

    assert response.status_code == 200
    assert response.json()["geometry"]["type"] == "LineString"


def test_invalid_bbox_returns_clear_error() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/vehicles", params={"bbox": "19,50,20"})

    assert response.status_code == 400
