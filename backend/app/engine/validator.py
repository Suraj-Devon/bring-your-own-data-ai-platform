# app/engine/validator.py
import pandas as pd


def validate_dataset(df: pd.DataFrame):
    issues = []

    for col in df.columns:
        series = df[col]

        # High null ratio
        null_ratio = series.isna().mean()
        if null_ratio > 0.5:
            issues.append({
                "severity": "warning",
                "code": "HIGH_NULL_RATIO",
                "message": f"Column '{col}' has {null_ratio:.0%} missing values",
                "column": col,
            })

        # Constant or near-constant column
        if series.nunique(dropna=True) <= 1:
            issues.append({
                "severity": "warning",
                "code": "CONSTANT_COLUMN",
                "message": f"Column '{col}' has constant or near-constant values",
                "column": col,
            })

        # Numeric outliers (IQR)
        if pd.api.types.is_numeric_dtype(series):
            clean = series.dropna()
            if not clean.empty:
                q1 = clean.quantile(0.25)
                q3 = clean.quantile(0.75)
                iqr = q3 - q1

                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr

                outlier_ratio = ((clean < lower) | (clean > upper)).mean()

                if outlier_ratio > 0.05:
                    issues.append({
                        "severity": "warning",
                        "code": "EXTREME_OUTLIERS",
                        "message": f"Column '{col}' has {outlier_ratio:.0%} values outside IQR bounds",
                        "column": col,
                    })

        # Categorical dominance risk
        if series.dtype == "object":
            value_counts = series.value_counts(dropna=True)
            if not value_counts.empty:
                dominant_ratio = value_counts.iloc[0] / value_counts.sum()

                if dominant_ratio > 0.8:
                    issues.append({
                        "severity": "warning",
                        "code": "CATEGORY_DOMINANCE",
                        "message": f"Column '{col}' is dominated by a single category ({dominant_ratio:.0%})",
                        "column": col,
                    })

    return issues
