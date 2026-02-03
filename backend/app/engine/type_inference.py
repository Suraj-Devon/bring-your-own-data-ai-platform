# app/engine/type_inference.py
import pandas as pd


def infer_types(df: pd.DataFrame) -> dict:
    inferred = {}

    for col in df.columns:
        series = df[col]

        if pd.api.types.is_numeric_dtype(series):
            inferred[col] = "number"
        elif pd.api.types.is_bool_dtype(series):
            inferred[col] = "boolean"
        elif pd.api.types.is_datetime64_any_dtype(series):
            inferred[col] = "datetime"
        elif series.nunique() / max(len(series), 1) < 0.2:
            inferred[col] = "categorical"
        else:
            inferred[col] = "string"

    return inferred
