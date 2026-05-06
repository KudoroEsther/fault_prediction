from fastapi.testclient import TestClient

from powerbot.app.main import app


client = TestClient(app)


def test_predict_endpoint(monkeypatch):
    monkeypatch.setattr(
        "powerbot.app.api.routes.predict.predict_fault",
        lambda payload: {
            "status": "fault",
            "fault_label": "LG fault",
            "confidence": 0.991,
        },
    )

    response = client.post(
        "/predict",
        json={"Va": 1, "Vb": 2, "Vc": 3, "Ia": 4, "Ib": 5, "Ic": 6},
    )

    assert response.status_code == 200
    assert response.json()["fault_label"] == "LG fault"
