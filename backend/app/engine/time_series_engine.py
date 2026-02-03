# app/engine/time_series_engine.py

from typing import Dict, List, Optional
import pandas as pd

DATE_PARSE_THRESHOLD = 0.7   # 70% must parse to accept as datetime
DROP_SPIKE_THRESHOLD = 0.3   # 30% change triggers risk


def _try_parse_datetime(series: pd.Series) -> Optional[pd.Series]:
    """
    Attempt to safely parse a column into datetime.
    Only accept if parsing success rate crosses threshold.
    """
    parsed = pd.to_datetime(
        series,
        errors="coerce",
        infer_datetime_format=True,
    )
    success_ratio = parsed.notna().mean()
    if success_ratio >= DATE_PARSE_THRESHOLD:
        return parsed
    return None


def detect_time_series(
    df: pd.DataFrame,
    column_profiles: List[Dict],
) -> Dict:
    """
    Detect time-series structure, aggregate activity,
    and surface temporal risks with numeric evidence.

    BACKWARD COMPATIBLE:
    - Existing keys preserved
    - Adds `series` for chart-ready data
    """

    result = {
        "date_column": None,
        "frequency": None,
        "series": [],      # 🔥 NEW: numeric evidence for charts
        "signals": [],
    }

    # --------------------------------------------------
    # Step 1: Identify candidate date columns
    # --------------------------------------------------
    date_candidates = []
    for col in column_profiles:
        if col["metrics"]["inferred_type"] in {"categorical", "string"}:
            date_candidates.append(col["name"])

    parsed_dates = None
    date_col = None

    for col_name in date_candidates:
        parsed = _try_parse_datetime(df[col_name])
        if parsed is not None:
            parsed_dates = parsed
            date_col = col_name
            break

    if parsed_dates is None:
        return result  # No safe datetime column found

    df_ts = df.copy()
    df_ts["_parsed_date"] = parsed_dates
    df_ts = df_ts.dropna(subset=["_parsed_date"])

    if df_ts.empty:
        return result

    result["date_column"] = date_col

    # --------------------------------------------------
    # Step 2: Determine frequency (daily vs monthly)
    # --------------------------------------------------
    df_ts = df_ts.sort_values("_parsed_date")
    date_diffs = df_ts["_parsed_date"].diff().dropna()

    median_diff_days = date_diffs.dt.days.median()

    if median_diff_days is not None and median_diff_days >= 25:
        frequency = "monthly"
        df_ts["period"] = df_ts["_parsed_date"].dt.to_period("M").astype(str)
    else:
        frequency = "daily"
        df_ts["period"] = df_ts["_parsed_date"].dt.date.astype(str)

    result["frequency"] = frequency

    # --------------------------------------------------
    # Step 3: Aggregate counts per period (CORE DATA)
    # --------------------------------------------------
    counts = (
        df_ts
        .groupby("period")
        .size()
        .sort_index()
    )

    if len(counts) < 3:
        return result  # Not enough data for trend analysis

    # 🔥 NEW: Persist numeric series for charts
    result["series"] = [
        {"period": period, "count": int(count)}
        for period, count in counts.items()
    ]

    # --------------------------------------------------
    # Step 4: Detect sudden drops / spikes
    # --------------------------------------------------
    pct_change = counts.pct_change()

    for period, change in pct_change.items():
        if pd.isna(change):
            continue

        if change <= -DROP_SPIKE_THRESHOLD:
            result["signals"].append({
                "type": "RISK",
                "code": "SUDDEN_DROP",
                "severity": "high",
                "message": f"Sudden drop detected in period {period}.",
                "evidence": [f"change = {change:.0%}"],
                "impact": "Business activity may have declined sharply.",
                "period": period,   # 🔥 precise anchor for annotations
            })

        elif change >= DROP_SPIKE_THRESHOLD:
            result["signals"].append({
                "type": "SIGNAL",
                "code": "SUDDEN_SPIKE",
                "severity": "medium",
                "message": f"Sudden spike detected in period {period}.",
                "evidence": [f"change = +{change:.0%}"],
                "impact": "Business activity may have spiked unusually.",
                "period": period,
            })

    # --------------------------------------------------
    # Step 5: Detect missing periods
    # --------------------------------------------------
    expected_periods = pd.period_range(
        start=pd.to_datetime(df_ts["_parsed_date"].min()),
        end=pd.to_datetime(df_ts["_parsed_date"].max()),
        freq="M" if frequency == "monthly" else "D",
    ).astype(str)

    missing_periods = set(expected_periods) - set(counts.index)

    if missing_periods:
        result["signals"].append({
            "type": "WARNING",
            "code": "MISSING_PERIODS",
            "severity": "medium",
            "message": "Missing time periods detected in the data.",
            "evidence": [f"missing_count = {len(missing_periods)}"],
            "impact": "Trends may be misleading due to data gaps.",
            "missing_periods": sorted(list(missing_periods))[:10],  # cap for safety
        })

    return result
