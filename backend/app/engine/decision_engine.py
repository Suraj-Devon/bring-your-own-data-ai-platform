# app/engine/decision_engine.py

from typing import List, Dict


def generate_next_steps(insights: List[Dict]) -> List[Dict]:
    steps = []

    for ins in insights:
        code = ins["code"]
        severity = ins.get("severity", "low")

        base_priority = {
            "high": 90,
            "medium": 60,
            "low": 30,
        }.get(severity, 30)

        # -------------------------------
        # TIME-SERIES RISKS
        # -------------------------------
        if code == "MISSING_PERIODS":
            steps.append({
                "title": "Fix missing time periods",
                "description": (
                    "Detected gaps in the time series can invalidate trend analysis, "
                    "seasonality detection, and forecasting."
                ),
                "priority": base_priority + 15,
                "derived_from": code,
                "category": "DATA_INTEGRITY",
            })

        if code == "SUDDEN_DROP":
            steps.append({
                "title": "Investigate sudden data drop",
                "description": (
                    "Abrupt drops may indicate system failures, reporting gaps, "
                    "or real-world disruptions that require validation."
                ),
                "priority": base_priority + 20,
                "derived_from": code,
                "category": "ANOMALY_INVESTIGATION",
            })

        # -------------------------------
        # DATA QUALITY
        # -------------------------------
        if code == "HIGH_MISSINGNESS":
            steps.append({
                "title": "Address high missing values",
                "description": (
                    "High missingness reduces analytical confidence and may bias results."
                ),
                "priority": base_priority + 10,
                "derived_from": code,
                "category": "DATA_QUALITY",
            })

        if code == "CATEGORY_DOMINANCE":
            steps.append({
                "title": "Rebalance dominant categories",
                "description": (
                    "Overrepresented categories can skew patterns and predictions."
                ),
                "priority": base_priority + 5,
                "derived_from": code,
                "category": "DATA_DISTRIBUTION",
            })

    # Deduplicate + sort
    unique = {
        (s["derived_from"], s["title"]): s for s in steps
    }

    ranked = sorted(
        unique.values(),
        key=lambda x: x["priority"],
        reverse=True
    )

    return ranked[:5]
