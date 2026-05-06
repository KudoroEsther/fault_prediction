from langchain_core.messages import SystemMessage


def build_system_prompt() -> SystemMessage:
    return SystemMessage(
        content=(
            "You are PowerBot, an electrical fault diagnosis assistant for "
            "power transmission systems. The machine learning fault label is "
            "authoritative. Explain the fault, outline common causes, list "
            "practical mitigation steps, and include safety precautions. "
            "Use the retrieved engineering context when present, but paraphrase "
            "it instead of quoting standards verbatim."
        )
    )


def build_diagnosis_prompt(fault_label: str, confidence: float, retrieved_docs: str) -> str:
    return f"""
Fault detected by the ML system:
- Fault label: {fault_label}
- Confidence: {confidence * 100:.1f}%

Retrieved engineering context:
{retrieved_docs or "No supporting documents were retrieved."}

Please provide:
1. A short explanation of the detected fault
2. Common causes
3. Step-by-step mitigation or response actions
4. Safety precautions

If the fault label is "No fault", state briefly that the line appears to be operating normally.
""".strip()
