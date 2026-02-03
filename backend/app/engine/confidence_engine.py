# app/engine/confidence_engine.py
from typing import Dict


def compute_confidence(
    insight: Dict,
    ingestion_meta: Dict,
    dataset_profile: Dict,
) -> Dict:
    """
    Deterministic confidence scoring for insights.
    Returns a score in [0,1] with an explainable label.
    """

    score = 1.0
    factors = []

    # --- Sampling impact ---
    if ingestion_meta.get("sampled"):
        ratio = ingestion_meta.get("sampling_ratio", 1.0)
        score *= min(1.0, 0.6 + ratio)  # floor confidence at 0.6
        factors.append("sampled_data")
    else:
        factors.append("full_data")

    # --- Dataset size ---
    rows = dataset_profile.get("rows_analyzed", 0)
    if rows < 1000:
        score *= 0.7
        factors.append("small_sample")
    elif rows > 10000:
        factors.append("large_sample")

    # --- Insight severity boosts ---
    if insight["severity"] == "high":
        score *= 1.0
        factors.append("strong_signal")
    elif insight["severity"] == "medium":
        score *= 0.9
        factors.append("moderate_signal")
    else:
        score *= 0.8
        factors.append("weak_signal")

    # Clamp
    score = max(0.3, min(score, 1.0))

    # Label
    if score >= 0.8:
        label = "high"
    elif score >= 0.6:
        label = "medium"
    else:
        label = "low"

    return {
        "score": round(score, 2),
        "label": label,
        "factors": factors,
    }
