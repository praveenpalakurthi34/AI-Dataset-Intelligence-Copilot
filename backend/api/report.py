from fastapi import APIRouter, HTTPException, Response
from backend.api.analyze import audit_reports_cache, analyze_dataset
from backend.engines.ai_engine import run_ai_reasoning_service
from backend.engines.report import generate_pdf_report
from backend.config import settings

router = APIRouter(prefix="/api", tags=["Report Engine"])

@router.get("/dataset/{dataset_id}/export-pdf")
async def export_pdf(dataset_id: str):
    # Fetch report
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

    # Run AI reasoning for inclusion in report
    try:
        ai_analysis = run_ai_reasoning_service(report)
    except Exception:
        ai_analysis = None

    pdf_bytes = generate_pdf_report(report, ai_analysis)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=audit_report_{dataset_id[:8]}.pdf"
        }
    )
