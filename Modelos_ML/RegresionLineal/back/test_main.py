from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health_check_reports_loaded_model():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["model_loaded"] is True


def test_predict_returns_numeric_price():
    response = client.post("/predict", json={"area_m2": 82.5})

    assert response.status_code == 200
    body = response.json()
    assert body["area_m2"] == 82.5
    assert isinstance(body["predicted_price"], float)
    assert body["predicted_price"] > 0


def test_predict_grows_with_area():
    small = client.post("/predict", json={"area_m2": 50}).json()["predicted_price"]
    big = client.post("/predict", json={"area_m2": 120}).json()["predicted_price"]

    assert big > small


def test_predict_rejects_invalid_area():
    assert client.post("/predict", json={"area_m2": -10}).status_code == 422
    assert client.post("/predict", json={"area_m2": 0}).status_code == 422
    assert client.post("/predict", json={"area_m2": "mucho"}).status_code == 422
    assert client.post("/predict", json={}).status_code == 422
