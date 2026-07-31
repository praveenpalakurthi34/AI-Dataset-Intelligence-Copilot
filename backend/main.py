from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api import (
    upload,
    analyze,
    history,
    report,
    autofix,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Dataset Intelligence Copilot REST API",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(report.router)
app.include_router(autofix.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
