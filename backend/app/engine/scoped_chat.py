# app/engine/scoped_chat.py
from typing import Dict, List

# Allowed question intents (locked)
ALLOWED_INTENTS = {
    "WHY_RISKY",
    "WHAT_TO_DO",
    "WHAT_COULD_GO_WRONG",
    "HOW_TO_MONITOR",
}

def build_scoped_prompt(
    insight: Dict,
    question_intent: str,
) -> Dict:
    """
    Build a bounded, deterministic prompt payload.
    NOTE: This returns a STRUCTURED payload, not a raw string.
    """

    if question_intent not in ALLOWED_INTENTS:
        raise ValueError("Unsupported question intent")

    base_context = {
        "insight_code": insight["code"],
        "severity": insight["severity"],
        "message": insight["message"],
        "evidence": insight.get("evidence", []),
        "impact": insight.get("impact"),
        "recommendation": insight.get("recommendation"),
    }

    # Intent-specific guidance (no math, no new facts)
    intent_instructions = {
        "WHY_RISKY": "Explain why this insight represents a business risk using the provided evidence only.",
        "WHAT_TO_DO": "Suggest concrete next steps based strictly on the recommendation and impact.",
        "WHAT_COULD_GO_WRONG": "Describe failure scenarios if this insight is ignored. Do not invent numbers.",
        "HOW_TO_MONITOR": "Explain how a business could monitor this risk over time using metrics already mentioned.",
    }

    return {
        "system_rules": [
            "Do not introduce new data.",
            "Do not invent numbers.",
            "Do not contradict the evidence.",
            "Keep the answer concise and actionable.",
        ],
        "context": base_context,
        "instruction": intent_instructions[question_intent],
    }


def generate_scoped_answer(
    prompt_payload: Dict,
) -> Dict:
    """
    v1 implementation WITHOUT LLM.
    We return a deterministic, templated response.
    (LLM can replace this later without changing the contract.)
    """

    instruction = prompt_payload["instruction"]
    context = prompt_payload["context"]

    # Deterministic fallback responses (safe, interview-proof)
    if "WHY" in instruction:
        answer = (
            f"This is risky because {context['message']} "
            f"The evidence indicates {', '.join(context['evidence'])}."
        )
    elif "Suggest" in instruction or "WHAT_TO_DO" in instruction:
        answer = (
            f"Recommended action: {context['recommendation']} "
            f"This helps mitigate the stated impact."
        )
    elif "failure" in instruction:
        answer = (
            "If ignored, this could amplify existing weaknesses and increase exposure "
            "to the stated business impact."
        )
    else:
        answer = (
            "You can monitor this by tracking the same metrics highlighted in the evidence "
            "and watching for further concentration or drift."
        )

    return {
        "answer": answer,
        "confidence": "high",
        "source": "deterministic",
    }
