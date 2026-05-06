from fastapi.testclient import TestClient

from powerbot.app.main import app


client = TestClient(app)


def test_diagnose_endpoint(monkeypatch):
    monkeypatch.setattr(
        "powerbot.app.services.diagnosis_service.diagnose_fault",
        lambda payload: {
            "status": "fault",
            "fault_label": "LLG fault",
            "confidence": 0.954,
            "final_answer": "Mocked diagnosis output.",
        },
    )

    response = client.post(
        "/diagnose",
        json={"Va": 1, "Vb": 2, "Vc": 3, "Ia": 4, "Ib": 5, "Ic": 6},
    )

    assert response.status_code == 200
    assert response.json()["final_answer"] == "Mocked diagnosis output."
