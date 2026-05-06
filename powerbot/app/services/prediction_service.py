from powerbot.app.models.model_loader import load_prediction_pipeline
from powerbot.app.schemas.request import FaultFeaturesRequest
from powerbot.app.utils.helpers import features_to_frame


def predict_fault(payload: FaultFeaturesRequest) -> dict:
    pipeline = load_prediction_pipeline()
    features = features_to_frame(payload)
    prediction = pipeline.predict(features)[0]
    confidence = float(pipeline.predict_proba(features).max())
    status = "no_fault" if prediction == "No fault" else "fault"
    return {
        "status": status,
        "fault_label": prediction,
        "confidence": round(confidence, 3),
    }
