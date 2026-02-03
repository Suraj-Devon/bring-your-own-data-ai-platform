from fastapi import UploadFile, HTTPException

from app.engine.csv_parser import parse_csv
from app.engine.type_inference import infer_types
from app.engine.profiler import profile_columns
from app.engine.validator import validate_dataset
from app.engine.insight_engine import generate_insights
from app.engine.chart_mapper import map_insights_to_charts
from app.engine.time_series_engine import detect_time_series
from app.engine.decision_engine import generate_next_steps


async def ingest_csv(file: UploadFile):
    """
    Main ingestion orchestration pipeline.

    Responsibilities:
    - Parse & sample CSV safely
    - Profile dataset & columns
    - Detect deterministic risks & signals
    - Attach numeric evidence for charts
    - Derive prioritized decision actions (Phase 2)
    - Prepare LLM-ready scoped hooks (NO LLM calls)
    """

    # --------------------------------------------------
    # Step 1: Parse CSV (sampling + encoding safety)
    # --------------------------------------------------
    try:
        df, ingestion_meta = parse_csv(file)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # --------------------------------------------------
    # Step 2: Dataset validation & profiling
    # --------------------------------------------------
    dataset_issues = validate_dataset(df)
    column_types = infer_types(df)
    column_profiles = profile_columns(df, column_types)

    dataset_profile = {
        "rows_analyzed": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells_percentage": float(df.isna().mean().mean() * 100),
    }

    # --------------------------------------------------
    # Step 3: Time-series intelligence (deterministic)
    # --------------------------------------------------
    time_series_result = detect_time_series(
        df=df,
        column_profiles=column_profiles,
    )

    # Defensive normalization
    if not time_series_result:
        time_series_result = {
            "date_column": None,
            "frequency": None,
            "series": [],
            "signals": [],
        }

    # --------------------------------------------------
    # Step 4: Insight generation (semantic layer)
    # --------------------------------------------------
    insights = generate_insights(
        dataset_profile=dataset_profile,
        column_profiles=column_profiles,
        dataset_issues=dataset_issues,
        time_series_result=time_series_result,
        ingestion_meta=ingestion_meta,
    )

    # --------------------------------------------------
    # Step 5: Chart generation (evidence → visuals)
    # --------------------------------------------------
    charts = map_insights_to_charts(
        insights=insights,
        column_profiles=column_profiles,
        time_series=time_series_result,
    )

    # --------------------------------------------------
    # 🚀 Step 6: Decision Intelligence (Phase 2)
    # --------------------------------------------------
    next_steps = generate_next_steps(insights)

    # --------------------------------------------------
    # Step 7: Scoped AI hooks (LLM-READY, NOT USED)
    # --------------------------------------------------
    scoped_chat = []
    for idx, insight in enumerate(insights):
        scoped_chat.append({
            "insight_id": idx,
            "insight_code": insight["code"],
            "allowed_questions": [
                "WHY_RISKY",
                "WHAT_TO_DO",
                "WHAT_COULD_GO_WRONG",
                "HOW_TO_MONITOR",
            ],
        })

    # --------------------------------------------------
    # Final response (stable contract)
    # --------------------------------------------------
    return {
        "ingestion": ingestion_meta,
        "dataset": dataset_profile,
        "time_series": time_series_result,
        "columns": column_profiles,
        "quality_summary": {
            "critical_issues": 0,
            "warnings": len(dataset_issues),
        },
        "insights": insights,
        "charts": charts,
        "next_steps": next_steps,  # 🔥 Phase 2 output
        "scoped_chat": scoped_chat,
    }
