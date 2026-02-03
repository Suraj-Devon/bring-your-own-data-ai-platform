# app/engine/insight_engine.py
from typing import List, Dict
from app.engine.confidence_engine import compute_confidence


def generate_insights(
    dataset_profile: Dict,
    column_profiles: List[Dict],
    dataset_issues: List[Dict],
    time_series_result: Dict = None,
    ingestion_meta: Dict = None,
) -> List[Dict]:

    insights = []

    # --- High Missingness ---
    for col in column_profiles:
        if col["metrics"]["null_percentage"] > 50:
            insights.append({
                "type": "RISK",
                "code": "HIGH_MISSINGNESS",
                "severity": "medium",
                "message": f"Column '{col['name']}' has very high missing values.",
                "evidence": [
                    f"null_percentage = {col['metrics']['null_percentage']:.1f}%"
                ],
                "impact": "Decisions using this column may be unreliable.",
                "recommendation": "Exclude this column or fix upstream data collection.",
            })

    # --- Category Dominance ---
    for col in column_profiles:
        stats = col["metrics"].get("stats")
        if stats and "dominant_ratio" in stats and stats["dominant_ratio"] > 0.8:
            insights.append({
                "type": "RISK",
                "code": "CATEGORY_DOMINANCE",
                "severity": "high",
                "message": f"Column '{col['name']}' is dominated by a single category.",
                "evidence": [
                    f"dominant_ratio = {stats['dominant_ratio']:.2f}"
                ],
                "impact": "Business outcomes may be overly dependent on a single segment.",
                "recommendation": "Investigate diversification or segment-specific risks.",
            })

    # --- Dataset Quality Summary ---
    if dataset_issues:
        insights.append({
            "type": "WARNING",
            "code": "DATA_QUALITY_ISSUES",
            "severity": "medium",
            "message": "Dataset contains multiple quality warnings.",
            "evidence": [
                f"warnings_count = {len(dataset_issues)}"
            ],
            "impact": "Insights may be affected by underlying data issues.",
            "recommendation": "Review data quality warnings before making decisions.",
        })

    # --- Time-Series Signals ---
    if time_series_result and time_series_result.get("signals"):
        for sig in time_series_result["signals"]:
            insights.append({
                "type": sig["type"],
                "code": sig["code"],
                "severity": sig["severity"],
                "message": sig["message"],
                "evidence": sig.get("evidence", []),
                "impact": sig.get("impact"),
                "recommendation": "Investigate root causes for temporal anomalies.",
            })

    # --- Attach confidence (ADD-ONLY) ---
    for insight in insights:
        insight["confidence"] = compute_confidence(
            insight=insight,
            ingestion_meta=ingestion_meta or {},
            dataset_profile=dataset_profile,
        )

    severity_order = {"high": 0, "medium": 1, "low": 2}
    insights.sort(key=lambda x: severity_order.get(x["severity"], 3))

    return insights
