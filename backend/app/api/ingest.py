# app/api/ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion_service import ingest_csv

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])


@router.post("/csv")
async def ingest_csv_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    return await ingest_csv(file)
