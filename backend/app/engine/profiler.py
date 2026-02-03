# app/engine/profiler.py
import pandas as pd
import numpy as np
from math import log2


def _iqr_outliers(series: pd.Series):
    clean = series.dropna()

    if clean.empty:
        return {
            "count": 0,
            "lower_bound": None,
            "upper_bound": None,
        }

    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = clean[(clean < lower) | (clean > upper)]

    return {
        "count": int(outliers.count()),
        "lower_bound": float(lower),
        "upper_bound": float(upper),
    }


def _entropy(series: pd.Series) -> float:
    counts = series.value_counts(dropna=True)
    total = counts.sum()

    entropy = 0.0
    for count in counts:
        p = count / total
        entropy -= p * log2(p)

    return float(entropy)


def profile_columns(df: pd.DataFrame, types: dict):
    profiles = []

    for col in df.columns:
        series = df[col]

        metrics = {
            "inferred_type": types[col],
            "null_count": int(series.isna().sum()),
            "null_percentage": float(series.isna().mean() * 100),
            "unique_count": int(series.nunique()),
            "stats": None,
        }

        # NUMERIC COLUMNS
        if types[col] == "number":
            outlier_info = _iqr_outliers(series)

            metrics["stats"] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "outlier_count": outlier_info["count"],
                "iqr_lower_bound": outlier_info["lower_bound"],
                "iqr_upper_bound": outlier_info["upper_bound"],
            }

        # CATEGORICAL COLUMNS
        if types[col] == "categorical":
            value_counts = series.value_counts(dropna=True)
            total = int(value_counts.sum())

            top_values = (
                value_counts.head(5)
                .reset_index()
                .rename(columns={"index": "value", col: "count"})
                .to_dict(orient="records")
            )

            entropy_score = _entropy(series)

            metrics["stats"] = {
                "top_values": top_values,
                "entropy": entropy_score,
                "dominant_ratio": float(value_counts.iloc[0] / total) if total > 0 else 0.0,
            }

        profiles.append({
            "name": col,
            "metrics": metrics,
            "issues": [],
        })

    return profiles
