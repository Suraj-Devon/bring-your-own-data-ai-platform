from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ingest import router as ingest_router
import os

app = FastAPI(title="BYOD AI Platform – Data Engine")

# --------------------------------------------------
# CORS CONFIG (SAFE FOR PROD)
# --------------------------------------------------

ENV = os.getenv("ENV", "development")

if ENV == "production":
    allowed_origins = [
        os.getenv("FRONTEND_URL"),  # e.g. https://byod-ai.vercel.app
    ]
else:
    # Local development
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
