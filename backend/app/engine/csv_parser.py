# app/engine/csv_parser.py
import pandas as pd
from fastapi import UploadFile

MAX_ROWS = 50_000
SAMPLE_SEED = 42


def parse_csv(file: UploadFile):
    """
    Parse CSV with encoding fallback and large-data sampling.
    Returns: (df, metadata)
    """

    file.file.seek(0)

    try:
        df = pd.read_csv(file.file, encoding="utf-8")
    except UnicodeDecodeError:
        file.file.seek(0)
        df = pd.read_csv(file.file, encoding="latin1")

    total_rows = len(df)

    metadata = {
        "total_rows": total_rows,
        "sampled": False,
        "sample_size": total_rows,
        "sampling_ratio": 1.0,
    }

    if total_rows > MAX_ROWS:
        df = df.sample(n=MAX_ROWS, random_state=SAMPLE_SEED)
        metadata.update({
            "sampled": True,
            "sample_size": MAX_ROWS,
            "sampling_ratio": MAX_ROWS / total_rows,
        })

    if df.empty:
        raise ValueError("CSV is empty after sampling")

    return df, metadata
