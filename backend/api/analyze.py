from datetime import datetime
from pathlib import Path
from typing import Dict
from fastapi import APIRouter, HTTPException
from backend.config import settings
from backend.schemas.audit import AuditReport
from backend.schemas.ai import AIAnalysisResponse
from backend.engines.parser import load_csv_dataset
from backend.engines.metadata import extract_metadata
from backend.engines.auditor import (
    detect_missing_values,
    detect_duplicates,
    detect_type_inconsistencies,
    detect_outliers_iqr,
    build_dataset_summary
)
from backend.engines.readiness import calculate_readiness_score
from backend.engines.ai_engine import run_ai_reasoning_service
from backend.database.session import SessionLocal
from backend.models.history import AuditHistoryModel

router = APIRouter(prefix="/api", tags=["Analysis"])

# In-memory cache for audit reports by dataset_id
audit_reports_cache: Dict[str, AuditReport] = {}

@router.post("/analyze/{dataset_id}", response_model=AuditReport)
async def analyze_dataset(dataset_id: str):
    file_path = settings.UPLOAD_FOLDER / f"{dataset_id}.csv"
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset with ID '{dataset_id}' not found or upload expired."
        )

    try:
        df, encoding = load_csv_dataset(file_path)
        file_size_bytes = file_path.stat().st_size
        filename = f"{dataset_id}.csv"

        # 1. Metadata Extraction
        metadata = extract_metadata(df, filename=filename, file_size_bytes=file_size_bytes)

        # 2. Rule-Based Quality Auditing
        missing_issues = detect_missing_values(df)
        dup_issues, dup_count, dup_pct = detect_duplicates(df)
        type_issues = detect_type_inconsistencies(df)
        outlier_issues, total_outliers, outliers_per_col = detect_outliers_iqr(df)

        all_issues = missing_issues + dup_issues + type_issues + outlier_issues

        # 3. Build Summary & Readiness Score
        summary = build_dataset_summary(
            df=df,
            dup_count=dup_count,
            dup_pct=dup_pct,
            total_outliers=total_outliers,
            outliers_per_col=outliers_per_col
        )

        readiness_score = calculate_readiness_score(
            total_missing_pct=summary.total_missing_pct,
            duplicate_pct=dup_pct,
            type_issue_count=len(type_issues),
            total_outliers=total_outliers,
            total_rows=summary.total_rows,
            total_columns=summary.total_columns
        )

        analyzed_at_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        audit_report = AuditReport(
            dataset_id=dataset_id,
            filename=filename,
            analyzed_at=analyzed_at_str,
            metadata=metadata,
            summary=summary,
            readiness_score=readiness_score,
            issues=all_issues
        )

        # Cache in memory
        audit_reports_cache[dataset_id] = audit_report

        # Persist summary record in SQLite DB (no raw CSV storage)
        try:
            db = SessionLocal()
            history_record = db.query(AuditHistoryModel).filter_by(dataset_id=dataset_id).first()
            if not history_record:
                history_record = AuditHistoryModel(
                    dataset_id=dataset_id,
                    filename=filename,
                    analyzed_at=analyzed_at_str,
                    total_rows=summary.total_rows,
                    total_columns=summary.total_columns,
                    readiness_score=readiness_score.overall_score,
                    grade=readiness_score.grade,
                    issues_found_count=len(all_issues),
                    ai_summary=readiness_score.status
                )
                db.add(history_record)
                db.commit()
            db.close()
        except Exception as db_err:
            print(f"[SQLite History Save Error]: {db_err}")

        return audit_report

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing dataset: {str(e)}"
        )

@router.get("/report/{dataset_id}", response_model=AuditReport)
async def get_cached_report(dataset_id: str):
    if dataset_id not in audit_reports_cache:
        file_path = settings.UPLOAD_FOLDER / f"{dataset_id}.csv"
        if file_path.exists():
            return await analyze_dataset(dataset_id)
        raise HTTPException(
            status_code=404,
            detail=f"Audit report for dataset '{dataset_id}' not found."
        )
    return audit_reports_cache[dataset_id]

@router.post("/analyze-ai/{dataset_id}", response_model=AIAnalysisResponse)
async def analyze_dataset_ai(dataset_id: str):
    if dataset_id in audit_reports_cache:
        report = audit_reports_cache[dataset_id]
    else:
        file_path = settings.UPLOAD_FOLDER / f"{dataset_id}.csv"
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_id}' not found."
            )
        report = await analyze_dataset(dataset_id)

    try:
        ai_response = run_ai_reasoning_service(report)

        # Update SQLite record with AI summary
        try:
            db = SessionLocal()
            history_record = db.query(AuditHistoryModel).filter_by(dataset_id=dataset_id).first()
            if history_record:
                history_record.ai_summary = ai_response.health_summary
                db.commit()
            db.close()
        except Exception as db_err:
            print(f"[SQLite History Update Error]: {db_err}")

        return ai_response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI Reasoning Service Error: {str(e)}"
        )
