# app/models/schemas.py
from typing import List, Optional, Any
from pydantic import BaseModel


class DataIssue(BaseModel):
    severity: str  # "warning" | "critical"
    code: str
    message: str
    column: Optional[str] = None


class ColumnMetrics(BaseModel):
    inferred_type: str
    null_count: int
    null_percentage: float
    unique_count: int
    stats: Optional[dict] = None


class ColumnProfile(BaseModel):
    name: str
    metrics: ColumnMetrics
    issues: List[DataIssue]


class DatasetProfile(BaseModel):
    rows: int
    columns: int
    duplicate_rows: int
    missing_cells_percentage: float


class IngestionResponse(BaseModel):
    dataset: DatasetProfile
    columns: List[ColumnProfile]
    quality_summary: dict
