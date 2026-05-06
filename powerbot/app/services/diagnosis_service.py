from functools import lru_cache

from powerbot.app.core.config import get_settings
from powerbot.app.rag.prompt_builder import build_diagnosis_prompt, build_system_prompt
from powerbot.app.services.prediction_service import predict_fault
from powerbot.app.schemas.request import FaultFeaturesRequest


@lru_cache(maxsize=1)
def get_llm():
    from langchain_openai import ChatOpenAI

    settings = get_settings()
    api_key = settings.resolved_openai_api_key
    if not api_key:
        raise RuntimeError("OpenAI API key is not configured.")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)


def diagnose_fault(payload: FaultFeaturesRequest) -> dict:
    prediction = predict_fault(payload)
    if prediction["fault_label"] == "No fault":
        return {
            **prediction,
            "final_answer": "System operating normally. No transmission line fault was detected.",
        }

    from powerbot.app.rag.retriever import retrieve_documents

    query = (
        f"Explain {prediction['fault_label']} in transmission lines, including "
        "causes, mitigation, and safety precautions."
    )
    retrieved_docs = retrieve_documents(query)
    llm = get_llm()
    messages = [
        build_system_prompt(),
        ("human", build_diagnosis_prompt(
            fault_label=prediction["fault_label"],
            confidence=prediction["confidence"],
            retrieved_docs=retrieved_docs,
        )),
    ]
    response = llm.invoke(messages)
    return {
        **prediction,
        "final_answer": getattr(response, "content", str(response)),
    }
