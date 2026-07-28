from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db, Base, engine
from backend.models.history import AuditHistoryModel

# Ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api", tags=["History"])

@router.get("/history")
def get_audit_history(db: Session = Depends(get_db)):
    records = db.query(AuditHistoryModel).order_by(AuditHistoryModel.id.desc()).all()
    return [
        {
            "id": r.id,
            "dataset_id": r.dataset_id,
            "filename": r.filename,
            "analyzed_at": r.analyzed_at,
            "total_rows": r.total_rows,
            "total_columns": r.total_columns,
            "readiness_score": r.readiness_score,
            "grade": r.grade,
            "issues_found_count": r.issues_found_count,
            "ai_summary": r.ai_summary
        }
        for r in records
    ]
