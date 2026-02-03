from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ingest import router as ingest_router
import os

app = FastAPI(title="BYOD AI Platform – Data Engine")

# --------------------------------------------------
# CORS CONFIG (UPDATED FOR RENDER + VERCEL)
# --------------------------------------------------

# We include both Production and Development URLs in one list.
# This ensures it works on Render and locally without needing to toggle ENV vars.
allowed_origins = [
    "https://bring-your-own-data-ai-platform.vercel.app", # Your specific Vercel URL
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers (important for file uploads)
)

app.include_router(ingest_router)

@app.get("/")
def root():
    return {"message": "BYOD Backend is Live"}