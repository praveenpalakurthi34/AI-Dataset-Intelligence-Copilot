from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.config import settings
from backend.engines.auto_fix import (
    apply_auto_fix_from_file,
    get_download_information,
)

from backend.api.analyze import audit_reports_cache

router = APIRouter(
    prefix="/api",
    tags=["Auto Fix"],
)
@router.post("/autofix/{dataset_id}")
async def auto_fix_dataset(dataset_id: str):

    # -----------------------------------------
    # Check dataset exists
    # -----------------------------------------

    file_path = settings.UPLOAD_FOLDER / f"{dataset_id}.csv"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset_id}' not found.",
        )

    # -----------------------------------------
    # Check audit exists
    # -----------------------------------------

    if dataset_id not in audit_reports_cache:
        raise HTTPException(
            status_code=404,
            detail="Run dataset analysis before Auto Fix.",
        )

    report = audit_reports_cache[dataset_id]
        # -----------------------------------------
    # Run Auto Fix
    # -----------------------------------------

    try:

        result = apply_auto_fix_from_file(
            file_path=str(file_path),
            report=report,
            output_directory=str(settings.OUTPUT_FOLDER),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Auto Fix failed: {str(e)}",
        )

    # -----------------------------------------
    # Verify result
    # -----------------------------------------

    if not result.success:

        raise HTTPException(
            status_code=500,
            detail=result.message,
        )

    response = get_download_information(result)
        # -----------------------------------------
    # Response
    # -----------------------------------------

    return {

        "success": response["success"],

        "message": response["message"],

        "dataset_id": dataset_id,

        "download_file": Path(
            response["download_file"]
        ).name,

        "statistics": response["statistics"],

    }
    # ==========================================================
# DOWNLOAD CLEANED DATASET
# ==========================================================

@router.get("/download-cleaned/{filename}")
async def download_cleaned_dataset(filename: str):

    file_path = Path(settings.OUTPUT_FOLDER) / filename

    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Cleaned dataset not found.",

        )

    return FileResponse(

        path=str(file_path),

        media_type="text/csv",

        filename=filename,

    )
    # ==========================================================
# AUTO FIX STATUS
# ==========================================================

@router.get("/autofix/status/{dataset_id}")
async def auto_fix_status(dataset_id: str):

    output_file = (
        Path(settings.OUTPUT_FOLDER)
        / f"{dataset_id}_cleaned.csv"
    )

    return {

        "dataset_id": dataset_id,

        "available": output_file.exists(),

        "filename": output_file.name if output_file.exists() else None,

        "download_url": (
            f"/api/download-cleaned/{output_file.name}"
            if output_file.exists()
            else None
        ),

    }


# ==========================================================
# AUTO FIX HEALTH
# ==========================================================

@router.get("/autofix/health")
async def autofix_health():

    output_dir = Path(settings.OUTPUT_FOLDER)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    cleaned_files = list(
        output_dir.glob("*_cleaned.csv")
    )

    return {

        "status": "healthy",

        "output_directory": str(output_dir),

        "generated_files": len(cleaned_files),

    }


# ==========================================================
# END OF ROUTER
# ==========================================================