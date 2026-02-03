# app/engine/chart_mapper.py

from typing import List, Dict


def map_insights_to_charts(
    insights: List[Dict],
    column_profiles: List[Dict],
    time_series: Dict = None,
) -> List[Dict]:
    """
    Insight → Chart Mapper v3 (Evidence-Grade)

    Guarantees:
    - Backward compatible categorical charts
    - Chart-ready numeric time-series data
    - Explicit x/y keys
    - No frontend inference required
    """

    charts: List[Dict] = []

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def get_col(col_name: str):
        for c in column_profiles:
            if c["name"] == col_name:
                return c
        return None

    # --------------------------------------------------
    # CATEGORICAL CHARTS (UNCHANGED)
    # --------------------------------------------------
    for insight in insights:
        code = insight["code"]

        # CATEGORY DOMINANCE
        if code == "CATEGORY_DOMINANCE":
            col_name = insight["message"].split("'")[1]
            col = get_col(col_name)

            if col and col["metrics"].get("stats"):
                charts.append({
                    "insight_code": code,
                    "title": f"Category dominance in {col_name}",
                    "type": "bar",
                    "data": col["metrics"]["stats"]["top_values"],
                    "xKey": "value",
                    "yKey": "count",
                    "caption": (
                        f"{int(col['metrics']['stats']['dominant_ratio'] * 100)}% "
                        f"of records fall into a single category."
                    ),
                })

        # HIGH MISSINGNESS
        if code == "HIGH_MISSINGNESS":
            col_name = insight["message"].split("'")[1]
            col = get_col(col_name)

            if col:
                total = col["metrics"]["null_count"] + col["metrics"]["unique_count"]
                charts.append({
                    "insight_code": code,
                    "title": f"Missing data in {col_name}",
                    "type": "bar",
                    "data": [
                        {"label": "Missing", "count": col["metrics"]["null_count"]},
                        {"label": "Present", "count": total - col["metrics"]["null_count"]},
                    ],
                    "xKey": "label",
                    "yKey": "count",
                    "caption": (
                        f"{col['metrics']['null_percentage']:.1f}% "
                        f"of values are missing."
                    ),
                })

        # NUMERIC OUTLIERS
        if code == "REVENUE_OUTLIERS":
            col_name = insight["message"].split("'")[1]
            col = get_col(col_name)

            if col and col["metrics"].get("stats"):
                charts.append({
                    "insight_code": code,
                    "title": f"Outliers in {col_name}",
                    "type": "boxplot",
                    "data": col["metrics"]["stats"],
                    "caption": (
                        f"{col['metrics']['stats']['outlier_count']} values "
                        f"fall outside the normal range."
                    ),
                })

    # --------------------------------------------------
    # TIME-SERIES CHARTS (EVIDENCE-GRADE)
    # --------------------------------------------------
    if (
        time_series
        and time_series.get("series")
        and time_series.get("signals")
    ):
        series_data = time_series["series"]

        for sig in time_series["signals"]:
            code = sig["code"]

            # Sudden Drop / Spike → Line Chart
            if code in {"SUDDEN_DROP", "SUDDEN_SPIKE"}:
                annotation = None
                if sig.get("period"):
                    annotation = {
                        "x": sig["period"],
                        "label": sig["message"],
                    }

                charts.append({
                    "insight_code": code,
                    "title": f"Activity trend over time ({time_series.get('frequency')})",
                    "type": "line",
                    "data": series_data,
                    "xKey": "period",
                    "yKey": "count",
                    "annotations": [annotation] if annotation else [],
                    "caption": sig["message"],
                })

            # Missing Periods → Bar Chart
            if code == "MISSING_PERIODS":
                missing_count = 0
                if sig.get("evidence"):
                    try:
                        missing_count = int(sig["evidence"][0].split("=")[1])
                    except Exception:
                        missing_count = 0

                charts.append({
                    "insight_code": code,
                    "title": "Missing time periods detected",
                    "type": "bar",
                    "data": [
                        {"label": "Missing periods", "count": missing_count}
                    ],
                    "xKey": "label",
                    "yKey": "count",
                    "caption": "Data gaps detected that may distort trend analysis.",
                })

    return charts
