from typing import List, Dict

SEVERITY_WEIGHT = {
    "high": 3,
    "medium": 2,
    "low": 1,
}

def derive_actions(insights: List[Dict]) -> List[Dict]:
    """
    Deterministic Decision Engine (Phase 2 – FINAL)

    Principles:
    - No LLM
    - Fully explainable
    - Derived ONLY from detected insights
    - Stable, interview-safe
    """

    actions = []

    for insight in insights:
        code = insight["code"]
        severity = insight["severity"]
        confidence = insight.get("confidence", {}).get("score", 0.7)

        priority = round(
            SEVERITY_WEIGHT.get(severity, 1) * confidence,
            2
        )

        if code == "HIGH_MISSINGNESS":
            actions.append({
                "title": "Fix or remove high-missing columns",
                "description": (
                    "Columns with excessive missing data reduce reliability of "
                    "analysis, modeling, and reporting."
                ),
                "derived_from": code,
                "priority": priority,
                "category": "data_quality",
                "why_now": "Missing values directly impact statistical validity.",
                "risk_if_ignored": (
                    "Models may learn biased patterns or fail silently due to incomplete data."
                ),
                "confidence": confidence,
            })

        elif code == "CATEGORY_DOMINANCE":
            actions.append({
                "title": "Audit dominant categories",
                "description": (
                    "A single category dominates the dataset, limiting signal diversity."
                ),
                "derived_from": code,
                "priority": priority,
                "category": "distribution_risk",
                "why_now": "Dominant categories can hide minority behaviors.",
                "risk_if_ignored": (
                    "Decisions may overfit to one segment and miss emerging risks."
                ),
                "confidence": confidence,
            })

        elif code == "SUDDEN_DROP":
            actions.append({
                "title": "Investigate sudden activity drop",
                "description": (
                    "Abrupt drops often indicate data loss, system failures, or real-world disruption."
                ),
                "derived_from": code,
                "priority": priority,
                "category": "trend_risk",
                "why_now": "Sudden declines are rarely normal in stable systems.",
                "risk_if_ignored": (
                    "Forecasts and operational decisions may become misleading."
                ),
                "confidence": confidence,
            })

        elif code == "SUDDEN_SPIKE":
            actions.append({
                "title": "Validate spike authenticity",
                "description": (
                    "Spikes may be anomalies, one-off events, or ingestion errors."
                ),
                "derived_from": code,
                "priority": priority,
                "category": "trend_signal",
                "why_now": "Unverified spikes can distort averages and trends.",
                "risk_if_ignored": (
                    "False positives may trigger incorrect business responses."
                ),
                "confidence": confidence,
            })

        elif code == "MISSING_PERIODS":
            actions.append({
                "title": "Backfill or flag missing periods",
                "description": (
                    "Gaps in time-series data distort trend analysis and forecasting."
                ),
                "derived_from": code,
                "priority": priority,
                "category": "time_series_integrity",
                "why_now": "Time gaps break continuity assumptions.",
                "risk_if_ignored": (
                    "Trend-based decisions may be inaccurate or misleading."
                ),
                "confidence": confidence,
            })

    # Highest priority first
    actions.sort(key=lambda x: x["priority"], reverse=True)

    return actions
